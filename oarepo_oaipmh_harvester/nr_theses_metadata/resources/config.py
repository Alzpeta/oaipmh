from invenio_records_resources.resources import (
    RecordResourceConfig as InvenioRecordResourceConfig,
)


class NrThesesMetadataResourceConfig(InvenioRecordResourceConfig):
    """NrThesesMetadataRecord resource config."""

    blueprint_name = "NrThesesMetadata"
    url_prefix = "/nr_theses_metadata/"
