from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["market rfq transaction"]

rfq_transaction_list_extension = extend_schema(
    tags=group_tags,
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)

rfq_transaction_retrieve_extension = extend_schema(
    tags=group_tags,
)
