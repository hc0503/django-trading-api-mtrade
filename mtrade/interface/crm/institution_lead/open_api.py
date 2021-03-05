from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

base_tags=["crm - institution lead"],

inst_lead_list_extension=extend_schema(
    tags=base_tags,
    parameters = [
        default_cursor_param
    ]
)

inst_lead_retrieve_extension=extend_schema(
    tags=base_tags,
)

inst_lead_create_extension=extend_schema(
    tags=base_tags,
)

inst_lead_update_extension=extend_schema(
    tags=base_tags,
)

inst_lead_partial_update_extension=extend_schema(
    tags=base_tags,
)
