from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["institution rfq lock"]

rfq_lock_list_extension=extend_schema(
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

rfq_lock_retrieve_extension=extend_schema(
    tags=group_tags,
)

rfq_lock_create_extension=extend_schema(
    tags=group_tags,
)

rfq_lock_update_extension=extend_schema(
    tags=group_tags,
)

rfq_lock_partial_update_extension=extend_schema(
    tags=group_tags,
)

rfq_lock_destroy_extension=extend_schema(
    tags=group_tags,
)
