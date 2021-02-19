# django imports
from django.test import TestCase

from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase, APIClient

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices

# local imports
from . import views


DEFAULT_ACTIONS = {
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

class UserViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_view_set = views.UserViewSet.as_view(DEFAULT_ACTIONS)

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

    def test_get_user(self):
        request = self.factory.get('/api/v0/users/{}'.format(self.user_01.id))
        force_authenticate(request, user=self.user_01)
        response = self.user_view_set(request, pk=self.user_01.id)

        self.assertIs(response.status_code, 200)

    def test_create_user(self):
        post_params = {
            'username': '123',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'first@example.com'
        }
        request = self.factory.post('/api/v0/users/', post_params)
        force_authenticate(request, user=self.user_01)
        response = self.user_view_set(request)

        self.assertIs(response.status_code, 201)

    def test_create_user_bad_email(self):
        # test bad params
        post_params = {
            'username': '123',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'dasdsa' #TODO: check why this validation is not triggering an exception
        }
        request = self.factory.post('/api/v0/users/', post_params)
        force_authenticate(request, user=self.user_01)

        response = self.user_view_set(request)
