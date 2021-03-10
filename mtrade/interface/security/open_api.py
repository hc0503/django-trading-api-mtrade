from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

# Security extensions
security_list_extension = extend_schema(
    parameters=[
        default_cursor_param
    ]
)
