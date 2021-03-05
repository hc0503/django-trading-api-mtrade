from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param

base_tags = ["market - rfq transaction"]

rfq_transaction_list_extension = extend_schema(
    tags = base_tags,
    parameters = [
        default_cursor_param
    ]
)

rfq_transaction_retrieve_extension = extend_schema(
    tags = base_tags,
)
