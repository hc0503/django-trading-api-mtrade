from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

inst_manager_list_extension=extend_schema(
    tags=["institution manager"],
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)

inst_manager_retrieve_extension=extend_schema(
    tags=["institution manager"],
)
