# python imports

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# app imoprts
from mtrade.domain.notifications.setting.models import NotificationSetting
from mtrade.domain.notifications.setting.services import NotificationSettingServices as nss

# local imports
from .services import NotificationSettingAppServices as nsos

class NotificationSettingAppServicesTests(TestCase):

    def test_list_notification_settings(self):
        nqs = nsos.list_notification_settings(None)
        self.assertEqual(type(nqs), QuerySet)

    def test_create_notification_setting(self):
        data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": True,
        }
        ntc = nsos.create_notification_setting_from_dict(None, data)
        self.assertEqual(type(ntc), NotificationSetting)

        # Test notification was stored
        stored_notification_setting = nss.get_notification_setting_repo().get(id=ntc.id)
        self.assertEqual(type(stored_notification_setting), NotificationSetting)

    def test_update_notification_setting(self):
        data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": True,
        }
        ntc = nsos.create_notification_setting_from_dict(None, data)

        pre_update_created_at = ntc.created_at

        updated_data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": False,
        }

        nsos.update_notification_setting_from_dict(None, ntc, updated_data)

        ntc.refresh_from_db()
        self.assertEqual(ntc.ws_enabled, False)

        self.assertEqual(ntc.created_at, pre_update_created_at)
