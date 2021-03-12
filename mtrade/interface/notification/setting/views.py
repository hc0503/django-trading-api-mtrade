# python imports

# django imports
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.notifications.setting.services import NotificationSettingAppServices as nsas

# local imports
from . import open_api
from .serializers import NotificationSettingSerializer

@extend_schema_view(
    list=open_api.notification_setting_list_extension,
)
class NotificationSettingViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list NotificationSettings
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSettingSerializer
    ordering = ['-created_at']

    def get_queryset(self):
        return nsas.list_notification_settings(self.request.user)
