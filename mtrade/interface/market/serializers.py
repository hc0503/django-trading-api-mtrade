from mtrade.interface.lib import custom_serializers
from mtrade.domain.market.models import Market, ISIN
from mtrade.application.market.services import MarketAppServices


class MarketSerializer(custom_serializers.ApplicationModelSerializer):

    def create_from_app_service(self, validated_data):
        # this method links the interface layer with the application layer
        isin = ISIN(validated_data["isin"])
        is_open = validated_data["open"]
        user = self.get_user()
        # The returned instance comes from the application layer, not the
        # domain layer
        return MarketAppServices.create_market(user, isin, is_open)

    def update_from_app_service(self, instance, validated_data):
        # this method links the interface layer with the application layer
        isin = ISIN(validated_data["isin"])
        is_open = validated_data["open"]
        user = self.get_user()
        # The returned instance comes from the application layer, not the
        # domain layer
        return MarketAppServices.update_market(user, instance, isin, is_open)

    class Meta:
        model = Market
        fields = '__all__'
