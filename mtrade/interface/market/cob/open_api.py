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

cob_list_extension=extend_schema(
    tags=["market cob"],
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
#cob_list_extension=extend_schema(
#    tags=["market cob"],
#    parameters=[
#        OpenApiParameter(
#            name='direction',
#            type=str,
#            location=OpenApiParameter.QUERY,
#            description='A string identifying the order direction.',
#        ),
#        OpenApiParameter(
#            name='origin',
#            type=OpenApiTypes.UUID,
#            location=OpenApiParameter.QUERY,
#            description='A UUID string identifying the order origin.',
#        ),
#        OpenApiParameter(
#            name='trader_id',
#            # TODO: modify type from str to OpenApiTypes.UUID
#            type=str,
#            location=OpenApiParameter.QUERY,
#            description='A string identifying the trader.',
#        ),
#        OpenApiParameter(
#            name='institution',
#            type=OpenApiTypes.UUID,
#            location=OpenApiParameter.QUERY,
#            description='A UUID string identifying the institution. (Not implemented yer)',
#        ),
#        *common_params
#    ]
#)

cob_retrieve_extension=extend_schema(
    tags=["market cob"],
    parameters=[
        *common_params
    ]
)

cob_create_extension=extend_schema(
    tags=["market cob"],
    parameters=[
        *common_params
    ]
)
