# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import NotificationSettingFactory
from .models import NotificationSetting


class NotificationSettingServices():

    @staticmethod
    def get_notification_setting_factory() -> Type[NotificationSettingFactory]:
        return NotificationSettingFactory

    @staticmethod
    def get_notification_setting_repo() -> Type[Manager]:
        # We expose the whole repository as a service to avoid making a service for each repo action. If some repo action is used constantly in multiple places consider exposing it as a service.
        return NotificationSetting.objects
