from drf_spectacular.utils import OpenApiParameter

default_cursor_param = OpenApiParameter(
    name='cursor',
    type=str, # This is important, drf-spectacular incorrectly sets this as an int by default
    location=OpenApiParameter.QUERY,
    description="The pagination cursor value.",
)
