from time import sleep

from oarepo_oaipmh_harvester.cli import add
from oarepo_oaipmh_harvester.cli import _add, _harvest
from oarepo_oaipmh_harvester.oaipmh_record.proxies import current_service as record_service
from oarepo_oaipmh_harvester.nr_theses_metadata.proxies import current_service as theses_service
# from oarepo_oaipmh_harvester.oaipmh_config.proxies import current_service as config_service
from invenio_access.permissions import system_identity
# from ..nusl_oai.tran
# from oarepo_oaipmh_harvester.nusl_oai import NuslTransformer
from nr_vocabularies.proxies import current_service as nrvoc_service

def test_create_vocabularies(identity):
    item = nrvoc_service.create(identity, {'level': '2', 'id': 'bachelor', 'title': {'cs': 'Bakalářská práce', 'en': 'Bachelor thesis'}, 'coarType': 'bachelor thesis', 'relatedURI': {'COAR': 'http://purl.org/coar/resource_type/c_7a1f'}, 'dataCiteType': 'Dissertation', 'type': 'resourceType'})
def test_create_from_service(config_service,config_data, identity):

    harvester = config_service.create(identity, {'metadata': config_data})
    print(harvester)

def test_cmd(cli_runner, db, es):


    #shoud not be possible to make two harvesters with the same code
    #
    # result = cli_runner(add, 'nusl', '--code', 'nusl', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #                         '--set', 'global', '--prefix', 'marcxml', '--transformer',
    #                         'nusl_oai.transformer.NuslTransformer')
    result = _add(code='nusl', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml',
                  parser=None,
                  transformer='nusl_oai.transformer.NuslTransformer')
    print("1",result)
    # assert result.exit_code == 0
    # db.session.commit()
    # db.session.expunge_all()
    # db.session.close()
    #
    # with db.session.begin():
    # result = cli_runner(add, 'nusl', '--code', 'nusl2', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #                     '--set', 'global', '--prefix', 'marcxml', '--transformer',
    #                     'nusl_oai.transformer.NuslTransformer')
    # assert result.exit_code == 0
    result = _add(code='nusl2', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml', parser = None,
                  transformer='nusl_oai.transformer.NuslTransformer')

    result = cli_runner(add, 'nusl', '--code', 'nusl2', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
                        '--set', 'global', '--prefix', 'marcxml', '--transformer',
                        'nusl_oai.transformer.NuslTransformer')
    print("2",result)
    assert result.exit_code == 0


def test_harvest(cli_runner, app, db, es):
    from oarepo_oaipmh_harvester.oaipmh_record.records.api import OaipmhRecordRecord
    OaipmhRecordRecord.index.refresh()
    result = _add(code='nusl', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml',
                  parser=None,
                  # transformer=False
                  transformer='oarepo_oaipmh_harvester.nusl_oai.transformer.NuslTransformer'
                  )
    # db.session.expunge_all()
    # cli_runner(add, 'nusl', '--code', 'nusl', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #            '--set', 'global', '--prefix', 'marcxml', '--transformer', 'nusl_oai.transformer.NuslTransformer')

    # db.session.commit()


    # db.se
    # ssion.expunge_all()
    #ident = 'oai:invenio.nusl.cz:456299'
    result = _harvest(identifiers=['oai:invenio.nusl.cz:257457'], harvester_code='nusl', all_records=False, background=False, dump_to=None, load_from=None)
    # result = _harvest(identifiers=None, harvester_code='nusl', all_records=False, background=False, dump_to=None, load_from=None)

    # result = cli_runner(harvest, 'nusl', 'nusl', 'oai:invenio.nusl.cz:456299')

    OaipmhRecordRecord.index.refresh()
    sleep(2)
    records = record_service.scan(system_identity)
    hits_rec = list(records.hits)
    print(hits_rec)
    # assert len(hits_rec) == 1
    # assert hits_rec[0]['metadata']['status'] == 'O'
    theses = theses_service.scan(system_identity, params={'facets': {}})
    hits_thes = list(theses.hits)
    print(hits_thes)
    print('jej')
    # for tbl in reversed(db.meta.sorted_tables):
    #     db.get_engine().execute(tbl.delete())
    # # assert result.exit_code == 0
def test_moderids(cli_runner, app, db, es):
    _add(code='nusl', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml',
                  parser=None,
                  transformer='oarepo_oaipmh_harvester.nusl_oai.transformer.NuslTransformer'
                  )
    from .identifiers import identifiers
    _harvest(identifiers=identifiers, harvester_code='nusl', all_records=False,
                      background=False, dump_to=None, load_from=None)

    from oarepo_oaipmh_harvester.oaipmh_record.records.api import OaipmhRecordRecord
    OaipmhRecordRecord.index.refresh()
    sleep(2)
    records = record_service.scan(system_identity)
    hits = list(records.hits)
    print(hits)
    assert len(hits) == 200
    assert hits[0]['metadata']['status'] == 'O'
    theses = theses_service.scan(system_identity, params={'facets': {}})
    hits = list(theses.hits)
    print(hits)
def test_identifiers():
    root = 'oai:invenio.nusl.cz:456299'
    root_num = 299
    identifiers = []
    identifiers.append(root)
    size = len(root)
    for x in range(1,200):
        new_id = root[:size - 3]
        new_id = new_id + str(root_num-x)
        identifiers.append(new_id)
    print(identifiers)


