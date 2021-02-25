# django imports
from rest_framework import serializers

from mtrade.domain.market.models import Market

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
