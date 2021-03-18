from lib.django.custom_filters import extended_filter_overrides
from django.db import models
from django_filters import rest_framework as filters
from mtrade.domain.market.order_group.models import OrderGroup


class OrderGroupFilterSet(filters.FilterSet):

    class Meta:
        model = OrderGroup
        fields = [
            'orderbook_type',
            'order_type',
            'direction',
            'size',
            'notional',
            'weighted_avg_price',
            'weighted_avg_yield',
            'weighted_avg_spread',
            'fx',
            'group_status',
            'allocation_status',
            'allocation_pct',
            'priority',
            'expiration',
            'response_type',
            'settlement_currency',
            'requestor_type',
            'resp_received',
            'created_at'
        ]

        filter_overrides = extended_filter_overrides
