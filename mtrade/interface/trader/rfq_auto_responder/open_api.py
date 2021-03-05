from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

base_tags = ["trader - rfq auto responder"]

rfq_auto_responder_list_extension=extend_schema(
    tags = base_tags,
    parameters = [
        default_cursor_param
    ]
)

rfq_auto_responder_retrieve_extension=extend_schema(
    tags = base_tags,
)

rfq_auto_responder_create_extension=extend_schema(
    tags = base_tags,
)

rfq_auto_responder_update_extension=extend_schema(
    tags = base_tags,
)

rfq_auto_responder_partial_update_extension=extend_schema(
    tags = base_tags,
)
