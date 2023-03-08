from invenio_records.dumpers import \
    SearchDumper as InvenioElasticsearchDumper


class OaipmhRecordDumper(InvenioElasticsearchDumper):
    """OaipmhRecordRecord elasticsearch dumper."""