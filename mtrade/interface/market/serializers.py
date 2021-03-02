from lib.django.custom_serializers import ApplicationModelSerializer
from mtrade.domain.market.models import Market
from mtrade.application.market.services import MarketAppServices


class MarketSerializer(ApplicationModelSerializer):

    def create_from_app_service(self, validated_data):
        # this method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        user = self.get_user()
        return MarketAppServices.create_market_from_dict(user, validated_data)

    def update_from_app_service(self, instance, validated_data):
        # This method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        user = self.get_user()
        return MarketAppServices.update_market(user, instance, validated_data)

    class Meta:
        model = Market
        fields = '__all__'
