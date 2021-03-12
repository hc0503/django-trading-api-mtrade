from lib.django.custom_serializers import ApplicationModelSerializer
from mtrade.domain.notifications.setting.models import NotificationSetting
from mtrade.application.notifications.setting.services import NotificationSettingAppServices


class NotificationSettingSerializer(ApplicationModelSerializer):

    def create_from_app_service(self, user, validated_data):
        # this method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return NotificationSettingAppServices.create_notification_setting_from_dict(user, validated_data)

    def update_from_app_service(self, user, instance, validated_data):
        # This method links the interface layer with the application layer
        # The returned instance comes from the application layer, not the
        # domain layer
        return NotificationSettingAppServices.update_notification_setting_from_dict(user, instance, validated_data)

    class Meta:
        model = NotificationSetting
        fields = '__all__'
