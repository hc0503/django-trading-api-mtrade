## django imports
#from rest_framework import serializers
#
#from mtrade.domain.market.models import Market
#
#class MarketSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Market
#        fields = '__all__'
#
from mtrade.interface.lib import custom_serializers
from mtrade.domain.market.models import Market, ISIN
from mtrade.application.market.services import MarketAppServices


class MarketSerializer(custom_serializers.ApplicationModelSerializer):

    def build_instance(self, validated_data):
        # this method links the interface layer with the application layer
        isin = ISIN(validated_data["isin"])
        is_open = validated_data["open"]
        user = self.get_user()
        # The returned instance should come from the application layer, not the
        # domain layer
        return MarketAppServices.create_market(user, isin, is_open)

    class Meta:
        model = Market
        fields = '__all__'
