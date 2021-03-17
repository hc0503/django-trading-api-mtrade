# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase

# app imports


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


class RfqLockViewSetTest(APITestCase):
    # TODO: implement tests (see market examples)
    def setUp(self):
        self.factory = APIRequestFactory()
