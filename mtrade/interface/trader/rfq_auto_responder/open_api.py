from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

group_tags = ["trader - rfq auto responder"]

rfq_auto_responder_list_extension=extend_schema(
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

rfq_auto_responder_retrieve_extension=extend_schema(
    tags=group_tags,
)

rfq_auto_responder_create_extension=extend_schema(
    tags=group_tags,
)

rfq_auto_responder_update_extension=extend_schema(
    tags=group_tags,
)

rfq_auto_responder_partial_update_extension=extend_schema(
    tags=group_tags,
)
