# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.market.order_group.services import OrderGroupAppServices

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


class MarketViewSetTest(APITestCase):
    # TODO: implement tests (see market examples)
    def setUp(self):
        self.factory = APIRequestFactory()
