from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

base_tags = ["market rfq"]

common_params = [
    OpenApiParameter(
        name='market_pk',
        type=str,
        location=OpenApiParameter.PATH,
        description="An ISIN string identifying the market",
        examples=[
            OpenApiExample(
                'Market ISIN example',
                value='MX0MGO0000H9'
            ),
        ],
    )
]

rfq_list_extension = extend_schema(
    tags=base_tags,
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        ),
        *common_params
    ]
)

rfq_retrieve_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)

rfq_create_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)

rfq_partial_update_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)
