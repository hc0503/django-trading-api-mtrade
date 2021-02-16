from django.test import TestCase

from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from .services import UserAppServices

class UserAppServicesTests(TestCase):
    def test_create_user(self):
        try:
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
            UserAppServices.create_user(personal_data, base_permissions)
        except Exception:
            self.fail("Unexpected exception")
