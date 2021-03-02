# django imports
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase, APIClient

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.market.services import MarketAppServices as mas
from mtrade.domain.market.models import ISIN

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

class MarketViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.market_resource_view = views.MarketViewSet.as_view(RESOURCE_ACTIONS)
        self.market_collection_view = views.MarketViewSet.as_view(COLLECTION_ACTIONS)

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

        # Create a test market
        data = {
            "isin":"123456789012",
            "open":True
        }
        self.mkt = mas.create_market_from_dict(None, data)

    def test_create_markets(self):
        request = self.factory.post('/api/v0/market/', {"isin":"123456789012345", "open": True})
        force_authenticate(request, user=self.user_01)
        response = self.market_collection_view(request)

        self.assertIs(response.status_code, 201)

    def test_update_markets(self):
        request = self.factory.put('/api/v0/market/{}'.format(self.mkt.id), {"isin":"123456789012", "open": False})
        force_authenticate(request, user=self.user_01)
        response = self.market_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)

    def test_list_markets(self):
        request = self.factory.get('/api/v0/market/')
        force_authenticate(request, user=self.user_01)
        response = self.market_collection_view(request)

        self.assertIs(response.status_code, 200)

    def test_retrieve_market_dummy_data(self):
        request = self.factory.get('/api/v0/market/{}'.format(self.mkt.id))
        force_authenticate(request, user=self.user_01)

        response = self.market_resource_view(request, pk=self.mkt.id)

        self.assertIs(response.status_code, 200)
