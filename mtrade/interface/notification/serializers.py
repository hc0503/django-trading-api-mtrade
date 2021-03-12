from lib.django.custom_serializers import ApplicationModelSerializer
from mtrade.domain.notifications.models import Notification
from mtrade.application.notifications.services import NotificationAppServices


class NotificationSerializer(ApplicationModelSerializer):

    def create_from_app_service(self, user, validated_data):
        # this method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return NotificationAppServices.create_notification_from_dict(user, validated_data)

    def update_from_app_service(self, user, instance, validated_data):
        # This method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return NotificationAppServices.update_notification_from_dict(user, instance, validated_data)

    class Meta:
        model = Notification
        fields = '__all__'
