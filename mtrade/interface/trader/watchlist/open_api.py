from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["trader - watchlist"]

watchlist_list_extension=extend_schema(
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

watchlist_retrieve_extension=extend_schema(
    tags=group_tags,
)

watchlist_create_extension=extend_schema(
    tags=group_tags,
)

watchlist_update_extension=extend_schema(
    tags=group_tags,
)

watchlist_partial_update_extension=extend_schema(
    tags=group_tags,
)

watchlist_destroy_extension=extend_schema(
    tags=group_tags,
)
