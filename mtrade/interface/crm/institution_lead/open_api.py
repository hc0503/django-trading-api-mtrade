from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

inst_lead_list_extension=extend_schema(
    tags=["crm institution lead"],
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)

inst_lead_retrieve_extension=extend_schema(
    tags=["crm institution lead"],
)
