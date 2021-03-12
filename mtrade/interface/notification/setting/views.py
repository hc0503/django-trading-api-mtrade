# python imports

# django imports
from rest_framework import permissions

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.notifications.setting.services import NotificationSettingAppServices as nsas

# local imports
from .serializers import NotificationSettingSerializer

class NotificationSettingViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list NotificationSettings
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSettingSerializer

    def get_queryset(self):
        return nsas.list_notification_settings(self.request.user)
