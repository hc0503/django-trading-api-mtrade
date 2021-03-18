from django_filters import rest_framework as filters
from mtrade.domain.market.order_group.models import OrderGroup


class OrderGroupFilterSet(filters.FilterSet):
    class Meta:
        model = OrderGroup
        fields = [
            'orderbook_type',
            'order_type',
            'direction',
            'group_status',
            'allocation_status',
            'response_type',
            'settlement_currency',
        ]
