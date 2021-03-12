# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.notifications.setting.services import NotificationSettingAppServices as nsas

# local imports
from . import views

RESOURCE_ACTIONS = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
}

COLLECTION_ACTIONS = {
    'post': 'create',
    'get': 'list',
}

class NotificationSettingViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.notification_setting_resource_view = views.NotificationSettingViewSet.as_view(RESOURCE_ACTIONS)
        self.notification_setting_collection_view = views.NotificationSettingViewSet.as_view(COLLECTION_ACTIONS)

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

        # Create a test notification setting
        data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": True,
        }
        self.mkt = nsas.create_notification_setting_from_dict(None, data)

    def test_create_notification_settings(self):
        data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": True,
        }
        request = self.factory.post('/api/v0/notification/setting/', data)
        force_authenticate(request, user=self.user_01)
        response = self.notification_setting_collection_view(request)

        self.assertIs(response.status_code, 201)

    def test_update_notification_settings(self):
        data = {
            "module_name": "CRM",
            "email_enabled": True,
            "ws_enabled": False,
        }
        request = self.factory.put(
            '/api/v0/notification/setting/{}'.format(self.mkt.id),
            data
        )
        force_authenticate(request, user=self.user_01)
        response = self.notification_setting_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)

    def test_list_notification_settings(self):
        request = self.factory.get('/api/v0/notification/setting/')
        force_authenticate(request, user=self.user_01)
        response = self.notification_setting_collection_view(request)

        self.assertIs(response.status_code, 200)

    def test_retrieve_notification_setting_dummy_data(self):
        request = self.factory.get('/api/v0/notification/setting/{}'.format(self.mkt.id))
        force_authenticate(request, user=self.user_01)

        response = self.notification_setting_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)
