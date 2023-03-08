from invenio_records.dumpers import \
    SearchDumper as InvenioElasticsearchDumper


class OaipmhBatchDumper(InvenioElasticsearchDumper):
    """OaipmhBatchRecord elasticsearch dumper."""