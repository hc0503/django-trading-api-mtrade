# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.security.services import SecurityAppServices

from scripts.db_content_manager import populate_db as pdb

# local imports
from . import views

RESOURCE_ACTIONS = {
    'get': 'retrieve',
}

COLLECTION_ACTIONS = {

    'get': 'list',
}


class SecurityViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pdb.create_security_issuers()
        pdb.create_securities()

    def setUp(self):
        self.factory = APIRequestFactory()
        self.order_group_resource_view = views.SecurityViewSet.as_view(
            RESOURCE_ACTIONS)
        self.order_group_collection_view = views.SecurityViewSet.as_view(
            COLLECTION_ACTIONS)

        self.u_data_01 = UserPersonalData(
            username='Teser',
            first_name='Testerman',
            last_name='Testerson',
            email="testerman@example.com"
        )
        self.u_permissions_01 = UserBasePermissions(
            is_staff=False,
            is_active=False
        )
        self.user_01 = UserAppServices.create_user(
            self.u_data_01, self.u_permissions_01)

    def test_list_securities(self):
        request = self.factory.get('/api/v0/security/')
        force_authenticate(request, user=self.user_01)
        response = self.order_group_collection_view(request)

        self.assertIs(response.status_code, 200)

    def test_retrieve_security(self):
        # TODO: implement test when we have ISIN real data
        pass
