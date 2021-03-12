# python imports

# django imports
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.notifications.services import NotificationAppServices as nas

# local imports
from . import open_api
from .serializers import NotificationSerializer

@extend_schema_view(
    list=open_api.notification_list_extension,
)
class NotificationViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list Notifications
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    ordering = ['-created_at']

    def get_queryset(self):
        return nas.list_notifications(self.request.user)
