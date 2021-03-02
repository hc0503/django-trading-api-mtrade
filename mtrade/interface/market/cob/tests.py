# python imports

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

class COBViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.cob_resource_view = views.COBViewSet.as_view(BASIC_RESOURCE_ACTIONS)
        self.cob_collection_view = views.COBViewSet.as_view(BASIC_COLLECTION_ACTIONS)

        self.market_id_01 = "MX0MGO0000H9"
        self.order_id = "0164509b-7925-485c-b4ec-3d8fb7b25b6f"

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

    def test_list_cob_dummy_data(self):
        request = self.factory.get('/api/v0/market/{}/cob'.format(self.market_id_01))
        force_authenticate(request, user=self.user_01)
        response = self.cob_collection_view(request, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)

        request = self.factory.get(
            '/api/v0/market/{}/cob'.format(self.market_id_01),
            {"direction":"buy"}
        )
        force_authenticate(request, user=self.user_01)
        response = self.cob_collection_view(request, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)

    def test_retrieve_cob_dummy_data(self):
        request = self.factory.get(
            '/api/v0/market/{}/cob/{}'.format(self.market_id_01, self.order_id)
        )
        force_authenticate(request, user=self.user_01)

        response = self.cob_resource_view(request, pk=self.order_id, market_pk=self.market_id_01)

        self.assertIs(response.status_code, 200)

    #def test_create_cob_dummy_data(self):
    #    payload = {
    #      "trader_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #      "isin": uuid4(),
    #      "submission": "2021-02-25T19:22:41.085Z",
    #      "expiration": "2021-02-25T19:22:41.085Z",
    #      "price": "0.0",
    #      "size": 0,
    #      "status": "active",
    #      "dirty_price": "0.0",
    #      "notional": "0.0",
    #      "spread": "0.0",
    #      "discount_margin": "0",
    #      "yield_value": "0.0",
    #      "direction": "buy",
    #      "parent": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #      "origin": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    #    }
    #    request = self.factory.post('/api/v0/market/{}/cob/'.format(self.market_id_01), payload)
    #    force_authenticate(request, user=self.user_01)

    #    response = self.cob_resource_view(request, market_pk=self.market_id_01)
    #    # TODO: response code should be changed to 201 when entity saving is implemented
    #    self.assertIs(response.status_code, 200, response.data)
