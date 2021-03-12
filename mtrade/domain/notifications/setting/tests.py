# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    NotificationSetting,
    NotificationSettingID,
    NotificationSettingFactory
)
from .services import NotificationSettingServices
from . import test_helper as th


class NotificationSettingTests(TestCase):

    def test_build_notification_setting_id(self):
        try:
            m = NotificationSettingID
        except Exception:
            self.fail("Unexpected exception")

    def test_build_notification_setting(self):
        try:
            NotificationSettingFactory.build_entity_with_id("CRM", True, True)
        except Exception:
            self.fail("Unexpected exception")

    def test_build_notification_settings(self):
        noti_setting = th.generate_random_notification_settings(5)
        self.assertEquals(len(noti_setting), 5)


class NotificationSettingServicesTests(TestCase):
    def test_get_notification_setting_repo(self):
        repo = NotificationSettingServices.get_notification_setting_repo()
        self.assertEquals(Manager, type(repo))
