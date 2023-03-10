from collections import defaultdict
import traceback
import click

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig, OAIHarvestRun, OAIHarvestRunBatch, HarvestStatus
from oarepo_oaipmh_harvester.oaipmh_config.records.api import OaipmhConfigRecord
from oarepo_oaipmh_harvester.proxies import current_harvester
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from oarepo_oaipmh_harvester.oaipmh_config.proxies import current_service as config_service
from oarepo_oaipmh_harvester.oaipmh_run.proxies import current_service as run_service
from oarepo_oaipmh_harvester.oaipmh_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oaipmh_record.proxies import current_service as record_service
@click.group(name='oaiharvester')
def oaiharvester():
    """Classifier commands."""

# @oaiharvester.command()
# @with_appcontext
# def t_comm():
#     print('jej')


@oaiharvester.command()
@click.option('-a', '--all-records', default=False, is_flag=True,
              help="Re-harvest all records, not from the last timestamp")
@click.option('--background', default=False, is_flag=True,
              help="Harvest on background via celery task")
@click.option('--dump-to',
              help="Do not import records, just dump (cache) them to this directory (mostly for debugging)")
@click.option('--load-from',
              help="Do not contact oai-pmh server but load the records from this directory (created by dump-to option)")
@click.argument('harvester_code')
@click.argument('identifiers', nargs=-1)
@with_appcontext
def harvest(harvester_code, all_records, background, dump_to, load_from, identifiers):
    _harvest(harvester_code, all_records, background, dump_to, load_from, identifiers)
    # current_harvester.run(harvester_code, all_records=all_records, on_background=background,
    #                       load_from=load_from, dump_to=dump_to, identifiers=identifiers)

def _harvest(harvester_code, all_records, background, dump_to, load_from, identifiers):
    current_harvester.run(harvester_code, all_records=all_records, on_background=background,
                          load_from=load_from, dump_to=dump_to, identifiers=identifiers)

@oaiharvester.command()
@click.option('--code', help="OAI server code", required=True)
@click.option('--name', help="OAI server name", required=True)
@click.option('--url', help="OAI base url", required=True)
@click.option('--set', help="OAI set", required=True)
@click.option('--prefix', help="OAI metadata prefix", required=True)
@click.option('--parser', help="OAI metadata parser", required=False)
@click.option('--transformer', help="Transformer class", required=True)
@with_appcontext
def add(code, name, url, set, prefix, parser, transformer):
    _add(code, name, url, set, prefix, parser, transformer)

def _add(code, name, url, set, prefix, parser, transformer):
    harvester = False
    harvesters = config_service.scan(system_identity, params={'facets': {'metadata_code': [code]}})

    if len(list(harvesters.hits)) > 0:
        harvester = True

    if harvester:
        print(f"Harvester with code {code} already exists")
        return
    metadata = {'code': code, 'name': name, 'baseurl': url, 'metadataprefix': prefix, 'setspecs': set,
                'transformer': transformer}
    if parser:
        metadata['parser'] = parser
    try:
        config_service.create(system_identity,
                          {'metadata': metadata})
    except Exception as e:
        print(e)
        raise e

    OaipmhConfigRecord.index.refresh()


@oaiharvester.command()
@click.argument('code', required=True)
@click.option('--run-id', required=False)
@click.option('--details', default=False, is_flag=True)
@with_appcontext
def warnings(code, run_id=None, details=False):
    cfg = config_service.scan(system_identity, params={'facets': {'metadata_code': [code]}})
    try:
        cfg = list(cfg.hits)[0]
    except:
        print(f"Harvester with code {code} does not exist")
        return

    # cfg = OAIHarvesterConfig.query.filter_by(code=code).one()
    if run_id is not None:
        run_query = run_service.scan(system_identity, {'facets': {'_id': [run_id]}})

        run_query = list(run_query.hits)

        # run_query = OAIHarvestRun.query.filter_by(id=run_id, harvester_id=cfg.id)
    else:
        # run_query = OAIHarvestRun.query.filter_by(harvester_id=cfg.id).order_by(OAIHarvestRun.started.desc())
        run_query = run_service.scan(system_identity, params={'facets': {'metadata_harvester_id': [cfg['id']]}})
        run_query = list(run_query.hits)

    try:
        run = run_query[0]
        print(str(run))
    except:
        print(f"No runs with harvester code {code}")
        return

    # batches = OAIHarvestRunBatch.query.filter_by(run_id=run.id, status=HarvestStatus.FAILED)
    batches_query = batch_service.scan(system_identity, params={'facets': {'metadata_run_id': [run['id']]}})
    batches_query = list(batches_query.hits)
    print('b query', str(batches_query))
    batches = []
    for batch in batches_query:
        if batch['metadata']['status'] == 'W':
            batches.append(batch)

    by_message = defaultdict(list)
    print('b', str(batches))
    for batch in batches:
        record_query = record_service.scan(system_identity, params={'facets': {'metadata_batch_id': [batch['id']]}})
        record_query = list(record_query.hits)
        for record in record_query:
            if record['metadata']['status'] == 'W':
                if details:
                    by_message[record['metadata']['warning']].append(k)
                else:
                    by_message[record['metadata']['warning'][:80].replace('\n', ' ')].append(k)

    for msg, records in sorted(list(by_message.items()), key=lambda x: -len(x[1])):
        if details:
            print(f'{msg:80s} || {", ".join(records)}')
        else:
            print(f'{msg:80s} || {len(records):10d} || {", ".join(records[:3])}')




@oaiharvester.command()
@click.argument('code', required=True)
@click.option('--run-id', required=False)
@click.option('--details', default=False, is_flag=True)
@with_appcontext
def errors(code, run_id=None, details=False):
    cfg = config_service.scan(system_identity, params={'facets': {'metadata_code': [code]}})
    try:
        cfg = list(cfg.hits)[0]
    except:
        print(f"Harvester with code {code} does not exist")
        return

    # cfg = OAIHarvesterConfig.query.filter_by(code=code).one()
    if run_id is not None:
        run_query = run_service.scan(system_identity, {'facets': {'_id': [run_id]}} )

        run_query = list(run_query.hits)

        # run_query = OAIHarvestRun.query.filter_by(id=run_id, harvester_id=cfg.id)
    else:
        # run_query = OAIHarvestRun.query.filter_by(harvester_id=cfg.id).order_by(OAIHarvestRun.started.desc())
        run_query = run_service.scan(system_identity, params={'facets': {'metadata_harvester_id': [cfg['id']]}})
        run_query = list(run_query.hits)

    try:
        run = run_query[0]
        print(str(run))
    except:
        print(f"No runs with harvester code {code}")
        return

    # batches = OAIHarvestRunBatch.query.filter_by(run_id=run.id, status=HarvestStatus.FAILED)
    batches_query = batch_service.scan(system_identity,params = {'facets': {'metadata_run_id': [run['id']]}})
    batches_query = list(batches_query.hits)
    print('b query', str(batches_query))
    batches = []
    for batch in batches_query:
        if batch['metadata']['status'] == 'E':
            batches.append(batch)

    by_message = defaultdict(list)
    print('b', str(batches))
    for batch in batches:
        record_query = record_service.scan(system_identity, params={'facets': {'metadata_batch_id': [batch['id']]}})
        record_query = list(record_query.hits)
        for record in record_query:
            if record['metadata']['status'] == 'E':
                if details:
                    by_message[record['metadata']['error']].append(k)
                else:
                    by_message[record['metadata']['error'][:80].replace('\n', ' ')].append(k)

    for msg, records in sorted(list(by_message.items()), key=lambda x: -len(x[1])):
        if details:
            print(f'{msg:80s} || {", ".join(records)}')
        else:
            print(f'{msg:80s} || {len(records):10d} || {", ".join(records[:3])}')
