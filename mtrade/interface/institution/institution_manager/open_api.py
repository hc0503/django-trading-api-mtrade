from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["institution manager"]

inst_manager_list_extension=extend_schema(
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

inst_manager_retrieve_extension=extend_schema(
    tags=group_tags,
)

inst_manager_create_extension=extend_schema(
    tags=group_tags,
)

inst_manager_update_extension=extend_schema(
    tags=group_tags,
)

inst_manager_partial_update_extension=extend_schema(
    tags=group_tags,
)
