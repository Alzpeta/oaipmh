from flask import Blueprint


def create_blueprint_from_app(app):
    """Create  blueprint."""
    if app.config.get("NR_THESES_METADATA_REGISTER_BLUEPRINT", True):
        blueprint = app.extensions["nr_theses_metadata"].resource.as_blueprint()
    else:
        blueprint = Blueprint(
            "nr_theses_metadata", __name__, url_prefix="/empty/nr_theses_metadata"
        )
    blueprint.record_once(init)
    return blueprint


def init(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_theses_metadata"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="nr_theses_metadata")

    # Register indexer
    iregistry = app.extensions["invenio-indexer"].registry
    iregistry.register(ext.service.indexer, indexer_id="nr_theses_metadata")
