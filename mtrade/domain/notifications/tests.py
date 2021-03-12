# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices

# local imports
from .models import (
    Notification,
    NotificationID,
    Payload,
    NotificationFactory
)
from .services import NotificationServices
from . import tests_helper as th


class NotificationTests(TestCase):
    def setUp(self):
        self.u_data_01 = UserPersonalData(
            username = 'Teser',
            first_name = 'Testerman',
            last_name = 'Testerson',
            email = "testerman@example.com"
        )
        self.u_permissions_01 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )
        self.user_01 = UserAppServices.create_user(self.u_data_01, self.u_permissions_01)

    def test_build_notification_id(self):
        try:
            m = NotificationID
        except Exception:
            self.fail("Unexpected exception")

    def test_build_Payload(self):
        try:
            Payload({"message": "A new project is created", "period": 30})
        except Exception:
            self.fail("Unexpected exception")

    def test_build_notification(self):
        try:
            NotificationFactory.build_entity_with_id("c13cce88-42e3-40a1-9402-abf7e2f0a297", 1, Payload({"message": "A new project is created", "period": 30}), 1, 'ur')
        except Exception:
            self.fail("Unexpected exception")

    def test_build_notifications(self):
        mkts = th.generate_random_notifications(self.user_01, 5)
        self.assertEquals(len(mkts), 5)


class NotificationServicesTests(TestCase):
    def test_get_notification_repo(self):
        repo = NotificationServices.get_notification_repo()
        self.assertEquals(Manager, type(repo))
