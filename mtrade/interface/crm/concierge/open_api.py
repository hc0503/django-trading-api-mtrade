from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

base_tags = ["crm - concierge"]

concierge_list_extension=extend_schema(
    tags = base_tags,
    parameters = [
        default_cursor_param
    ]
)

concierge_retrieve_extension=extend_schema(
    tags=base_tags,
)

concierge_create_extension=extend_schema(
    tags=base_tags,
)

concierge_update_extension=extend_schema(
    tags=base_tags,
)

concierge_partial_update_extension=extend_schema(
    tags=base_tags,
)
