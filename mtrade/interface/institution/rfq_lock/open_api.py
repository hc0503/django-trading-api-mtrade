from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

group_tags = ["institution - rfq lock"]

common_params = []

rfq_lock_list_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

rfq_lock_retrieve_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

rfq_lock_create_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

rfq_lock_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

rfq_lock_partial_update_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)

rfq_lock_destroy_extension = extend_schema(
    tags=group_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)
