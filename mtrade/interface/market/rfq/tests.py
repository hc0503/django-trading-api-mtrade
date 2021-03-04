# python imports
from unittest import skip

# django imports
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate, APIRequestFactory

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

BASIC_RESOURCE_ACTIONS = {
    'get': 'retrieve',
    'post': 'create',
}

BASIC_COLLECTION_ACTIONS = {
    'get': 'list',
}


@skip("Skipping while app_zero:Rfq is in use")
class RfqViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.rfq_resource_view = views.RfqViewSet.as_view(
            BASIC_RESOURCE_ACTIONS)

        self.rfq_collection_view = views.RfqViewSet.as_view(
            BASIC_COLLECTION_ACTIONS)

        self.market_id_01 = "MX0MGO0000H9"
        self.order_id = "0164509b-7925-485c-b4ec-3d8fb7b25b6f"

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

    def test_list_rfq_dummy_data(self):
        request = self.factory.get(
            '/api/v0/market/{}/rfq'.format(self.market_id_01))
        force_authenticate(request, user=self.user_01)
        response = self.rfq_collection_view(
            request, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)

        request = self.factory.get(
            '/api/v0/market/{}/rfq'.format(self.market_id_01),
            {"direction": "buy"}
        )
        force_authenticate(request, user=self.user_01)
        response = self.rfq_collection_view(
            request, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)

    def test_retrieve_rfq_dummy_data(self):
        request = self.factory.get(
            '/api/v0/market/{}/rfq/{}'.format(self.market_id_01, self.order_id)
        )
        force_authenticate(request, user=self.user_01)

        response = self.rfq_resource_view(
            request, pk=self.order_id, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)
