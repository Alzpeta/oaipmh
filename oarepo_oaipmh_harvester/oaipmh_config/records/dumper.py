from invenio_records.dumpers import \
    SearchDumper as InvenioElasticsearchDumper


class OaipmhConfigDumper(InvenioElasticsearchDumper):
    """OaipmhConfigRecord elasticsearch dumper."""