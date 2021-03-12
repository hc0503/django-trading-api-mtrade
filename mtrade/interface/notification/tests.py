# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.notifications.services import NotificationAppServices as nas

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

class NotificationViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.notification_resource_view = views.NotificationViewSet.as_view(RESOURCE_ACTIONS)
        self.notification_collection_view = views.NotificationViewSet.as_view(COLLECTION_ACTIONS)

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

        # Create a test notification  "c13cce88-42e3-40a1-9402-abf7e2f0a297", 1, Payload({"message": "A new project is created", "period": 30}), 1, 'ur'
        data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": {"message": "A new probject is created", "period": 30},
            "priority": 1,
            "status": 'ur'
        }
        self.mkt = nas.create_notification_from_dict(self.user_01, data)

    def test_create_notifications(self):
        data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": '{"message": "A new probject is created", "period": 30}',
            "priority": 1,
            "status": 'ur'
        }
        request = self.factory.post('/api/v0/notification/', data)
        force_authenticate(request, user=self.user_01)
        response = self.notification_collection_view(request)

        self.assertIs(response.status_code, 201)

    def test_update_notifications(self):
        data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": '{"message": "A new probject is created", "period": 30}',
            "priority": 1,
            "status": 'rd'
        }
        request = self.factory.put(
            '/api/v0/notification/{}'.format(self.mkt.id),
            data
        )
        force_authenticate(request, user=self.user_01)
        response = self.notification_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)

    def test_list_notifications(self):
        request = self.factory.get('/api/v0/notification/')
        force_authenticate(request, user=self.user_01)
        response = self.notification_collection_view(request)

        self.assertIs(response.status_code, 200)

    def test_retrieve_notification_dummy_data(self):
        request = self.factory.get('/api/v0/notification/{}'.format(self.mkt.id))
        force_authenticate(request, user=self.user_01)

        response = self.notification_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)
