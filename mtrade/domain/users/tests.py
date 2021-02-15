import uuid

from django.test import TestCase
import django.dispatch

from .models import *


class UserFactoryTests(TestCase):
    def test_build(self):
        personal_data = UserPersonalData(
            username = "Tester",
            first_name = "Testerman",
            last_name = "Testerson",
            email = "testerman@example.com"
        )
        base_permissions = UserBasePermissions(
            is_staff = False,
            is_active = False
        )
        user = UserFactory.build_entity_with_id(personal_data, base_permissions)
