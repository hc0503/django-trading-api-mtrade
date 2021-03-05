# django imports
from drf_spectacular.utils import extend_schema, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

user_list_extension=extend_schema(
    parameters = [
        default_cursor_param
    ]
)

group_list_extension=extend_schema(
    parameters = [
        default_cursor_param
    ]
)
