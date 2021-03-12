# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import NotificationFactory
from .models import Notification


class NotificationServices():

    @staticmethod
    def get_notification_factory() -> Type[NotificationFactory]:
        return NotificationFactory

    @staticmethod
    def get_notification_repo() -> Type[Manager]:
        # We expose the whole repository as a service to avoid making a service for each repo action. If some repo action is used constantly in multiple places consider exposing it as a service.
        return Notification.objects
