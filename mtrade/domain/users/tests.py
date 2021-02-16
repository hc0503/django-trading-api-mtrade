import uuid

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError

from .models import *
from .services import *
from .admin import *


class UserTests(TestCase):
    def test_create_personal_data(self):
        try:
            personal_data = UserPersonalData(
                username = "Tester",
                first_name = "Testerman",
                last_name = "Testerson",
                email = "testerman@example.com"
            )
        except Exception:
            self.fail("Unexpected exception")

        with self.assertRaises(ValidationError):
            personal_data = UserPersonalData(
                username = "Tester",
                first_name = "Testerman",
                last_name = "Testerson",
                email = "testermanexample.com"
            )

    def test_create_superuser(self):
        try:
            User.objects.create_superuser("Tester")
        except Exception:
            self.fail("Unexpected exception")


        with self.assertRaises(ValueError):
            User.objects.create_superuser("Tester", is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser("Tester", is_superuser=False)


class UserFactoryTests(TestCase):
    def test_build(self):
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
            user = UserFactory.build_entity_with_id(personal_data, base_permissions)
        except Exception:
            self.fail("Unexpected exception")


class UserServicesTests(TestCase):
    def test_get_user_repo(self):
        repo = UserServices.get_user_repo()
        self.assertEquals(UserManagerAutoID, type(repo))


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

request = MockRequest()
request.user = MockSuperUser()

class UserAdminTests(TestCase):

    @classmethod
    def setUp(self):
        self.site = AdminSite()

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
        self.user = UserFactory.build_entity_with_id(personal_data, base_permissions)

    def test_user_admin(self):
        admin = UserAdmin(User, self.site)

        try:
            admin.save_model(request, obj=self.user, form=None, change=None)
        except Exception:
            self.fail("Unexpected exception")
