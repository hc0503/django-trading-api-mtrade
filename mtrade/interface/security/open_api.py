from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

security_list_extension=extend_schema(
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)
