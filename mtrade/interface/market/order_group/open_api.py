from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from lib.open_api.custom_params import default_cursor_param


base_tags = ['market - order-group']

common_params = [
    # OpenApiParameter(
    #     name='market_pk',
    #     type=str,
    #     location=OpenApiParameter.PATH,
    #     description="An ISIN string identifying the market",
    #     examples=[
    #         OpenApiExample(
    #             'Market ISIN example',
    #             value='MX0MGO0000H9'
    #         ),
    #     ],
    # )
]

order_group_list_extension = extend_schema(
    tags=base_tags,
    parameters=[
        default_cursor_param,
        *common_params
    ]
)


order_group_retrieve_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)

order_group_create_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)

order_group_partial_update_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)

order_group_update_extension = extend_schema(
    tags=base_tags,
    parameters=[
        *common_params
    ]
)
