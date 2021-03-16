from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

group_tags = ["institution - institution license"]

common_params = []

inst_license_list_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]

)

inst_license_retrieve_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_license_create_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_license_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

inst_license_partial_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)
