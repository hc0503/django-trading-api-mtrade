from drf_spectacular.utils import extend_schema

from lib.open_api.custom_params import default_cursor_param

trader_list_extension=extend_schema(
    parameters = [
        default_cursor_param
    ]
)
