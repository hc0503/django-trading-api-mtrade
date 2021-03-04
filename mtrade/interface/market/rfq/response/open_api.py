from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


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

rfq_response_list_extension = extend_schema(
    tags=["market rfq response"],
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

rfq_response_retrieve_extension = extend_schema(
    tags=["market rfq response"],
    parameters=[
        *common_params
    ]
)

rfq_response_create_extension = extend_schema(
    tags=["market rfq response"],
    parameters=[
        *common_params
    ]
)
