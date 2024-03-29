from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

base_tags = ["institution - settlement instruction"]

common_params = []

settlement_instruction_list_extension = extend_schema(
    tags=base_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

settlement_instruction_create_extension = extend_schema(
    tags=base_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ])

settlement_instruction_retrieve_extension = extend_schema(
    tags=base_tags,

    parameters=[
        default_cursor_param,
        *common_params
    ]
)

settlement_instruction_update_extension = extend_schema(
    tags=base_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

settlement_instruction_partial_update_extension = extend_schema(
    tags=base_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)
