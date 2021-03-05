from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

group_tags = ["institution - institution manager"]

inst_manager_list_extension=extend_schema(
    tags=group_tags,
    parameters = [
        default_cursor_param
    ]
)

inst_manager_retrieve_extension=extend_schema(
    tags=group_tags,
)

inst_manager_create_extension=extend_schema(
    tags=group_tags,
)

inst_manager_update_extension=extend_schema(
    tags=group_tags,
)

inst_manager_partial_update_extension=extend_schema(
    tags=group_tags,
)
