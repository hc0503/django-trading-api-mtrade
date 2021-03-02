from lib.django.custom_serializers import ApplicationModelSerializer

# TODO: remove app_zero
from app_zero.models import Rfq
from mtrade.application.market.rfq.services import RFQ_ZERO_SERVICES


class RfqSerializer(ApplicationModelSerializer):

    def create_from_app_service(self, user, validated_data):
        # this method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return RFQ_ZERO_SERVICES.create_resource_from_dict(user, validated_data)

    def update_from_app_service(self, user, instance, validated_data):
        # This method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return RFQ_ZERO_SERVICES.update_resource_from_dict(user, instance, validated_data)

    class Meta:
        model = Rfq
        fields = '__all__'
