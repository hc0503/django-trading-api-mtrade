from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

base_tags = ["trader - watchlist"]

watchlist_list_extension=extend_schema(
    tags = base_tags,
    parameters = [
        default_cursor_param
    ]
)

watchlist_retrieve_extension=extend_schema(
    tags = base_tags,
)

watchlist_create_extension=extend_schema(
    tags = base_tags,
)

watchlist_update_extension=extend_schema(
    tags = base_tags,
)

watchlist_partial_update_extension=extend_schema(
    tags = base_tags,
)

watchlist_destroy_extension=extend_schema(
    tags = base_tags,
)
