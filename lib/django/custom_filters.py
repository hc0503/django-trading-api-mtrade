from django.db import models
from django_filters import rest_framework as filters

extended_filter_overrides = {
    models.CharField: {
        'filter_class': filters.CharFilter,
        'extra': lambda f: {
            'lookup_expr': 'icontains',
        },
    },
    models.DecimalField: {
        'filter_class': filters.RangeFilter
    },
    models.PositiveIntegerField:
    {
        'filter_class': filters.RangeFilter
    },
    models.IntegerField:
    {
        'filter_class': filters.RangeFilter
    },
    models.DateTimeField:
    {
        'filter_class': filters.DateTimeFromToRangeFilter
    },
    models.DateField:
    {
        'filter_class': filters.DateFromToRangeFilter
    },
}
