from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

settlement_instruction_list_extension = extend_schema(
    tags=["institution settlement instruction"],
    parameters=[
        OpenApiParameter(
            name='order_by',
            type=str,
            location=OpenApiParameter.QUERY,
            description='A string that sets the output ordering.',
        )
    ]
)

settlement_instruction_create_extension = extend_schema(
    tags=["institution settlement instruction"])

settlement_instruction_retrieve_extension = extend_schema(
    tags=["institution settlement instruction"],
)
