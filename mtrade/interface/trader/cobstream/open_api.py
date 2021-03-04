from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["trader - cobstream"]

cobstream_list_extension=extend_schema(
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

cobstream_retrieve_extension=extend_schema(
    tags=group_tags,
)

cobstream_update_extension=extend_schema(
    tags=group_tags,
)

cobstream_partial_update_extension=extend_schema(
    tags=group_tags,
)
