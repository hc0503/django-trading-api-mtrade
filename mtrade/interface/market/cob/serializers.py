# django imports
from rest_framework import serializers

from mtrade.domain.market.cob.models import COBOrder


class COBSerializer(serializers.ModelSerializer):
    class Meta:
        model = COBOrder
        fields = '__all__'
