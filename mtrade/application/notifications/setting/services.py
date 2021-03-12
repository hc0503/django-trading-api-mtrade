# python imports
import json
from pathlib import Path

# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.notifications.setting.services import NotificationSettingServices as nss
from mtrade.domain.notifications.setting.models import NotificationSetting, NotificationSettingFactory

class NotificationSettingAppServices():
    @staticmethod
    def list_notification_settings(user) -> QuerySet:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return nss.get_notification_setting_repo().all()

    def create_notification_setting_from_dict(user, data: dict) -> NotificationSetting:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        module_name = data["module_name"]
        email_enabled = data["email_enabled"]
        ws_enabled = data["ws_enabled"]

        notification_setting = NotificationSettingFactory.build_entity_with_id(module_name, email_enabled, ws_enabled)
        notification_setting.save()
        return notification_setting

    def update_notification_setting_from_dict(user, instance: NotificationSetting, data: dict) -> NotificationSetting:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        # get notification by id

        module_name = data.get("module_name", None)
        email_enabled = data.get("email_enabled", None)
        ws_enabled = data.get("ws_enabled", None)

        instance.update_entity(module_name, email_enabled, ws_enabled)
        instance.save()
        return instance
