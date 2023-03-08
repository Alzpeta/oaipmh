from invenio_records.dumpers import \
    SearchDumper as InvenioElasticsearchDumper


class OaipmhRunDumper(InvenioElasticsearchDumper):
    """OaipmhRunRecord elasticsearch dumper."""