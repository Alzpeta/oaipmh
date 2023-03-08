from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from ..records.api import NrThesesMetadataRecord
from .permissions import NrThesesMetadataPermissionPolicy
from .schema import NrThesesMetadataSchema
from .search import NrThesesMetadataSearchOptions


class NrThesesMetadataServiceConfig(InvenioRecordServiceConfig):
    """NrThesesMetadataRecord service config."""

    url_prefix = "/nr_theses_metadata/"

    permission_policy_cls = NrThesesMetadataPermissionPolicy
    schema = NrThesesMetadataSchema
    search = NrThesesMetadataSearchOptions
    record_cls = NrThesesMetadataRecord

    components = [*InvenioRecordServiceConfig.components]

    model = "nr_theses_metadata"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
