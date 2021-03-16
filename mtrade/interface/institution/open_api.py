from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

group_tags = ["institution - institution "]

common_params = []

inst_list_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]

)

inst_retrieve_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_create_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_partial_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)
