from lib.django.custom_serializers import ApplicationModelSerializer

# TODO: remove app_zero
from app_zero.models import Rfq
from mtrade.domain.market.order_group.models import OrderGroup


class OrderGroupSerializer(ApplicationModelSerializer):
    # TODO: revise serializer
    class Meta:
        model = OrderGroup
        fields = '__all__'

    def create_from_app_service(self, user, validated_data):
        # this method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return MarketAppServices.create_market_from_dict(user, validated_data)

    def update_from_app_service(self, user, instance, validated_data):
        # This method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return MarketAppServices.update_market_from_dict(user, instance, validated_data)
