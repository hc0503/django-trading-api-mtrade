# python imports

# django imports
from rest_framework import permissions

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.notifications.services import NotificationAppServices as nas

# local imports
from .serializers import NotificationSerializer

class NotificationViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list Notifications
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return nas.list_notifications(self.request.user)
