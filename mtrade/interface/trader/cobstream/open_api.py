from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

base_tags = ["trader - cobstream"]

cobstream_list_extension=extend_schema(
    tags = base_tags,
    parameters = [
        default_cursor_param
    ]
)

cobstream_retrieve_extension=extend_schema(
    tags = base_tags,
)

cobstream_update_extension=extend_schema(
    tags = base_tags,
)

cobstream_partial_update_extension=extend_schema(
    tags = base_tags,
)
