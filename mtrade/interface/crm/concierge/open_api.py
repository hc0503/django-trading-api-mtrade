from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

base_tags=["crm concierge"]

concierge_list_extension=extend_schema(
    tags=base_tags,
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)

concierge_retrieve_extension=extend_schema(
    tags=base_tags,
)

concierge_create_extension=extend_schema(
    tags=base_tags,
)

concierge_update_extension=extend_schema(
    tags=base_tags,
)

concierge_partial_update_extension=extend_schema(
    tags=base_tags,
)
