# django imports
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.domain.market.order_group.models import OrderGroup
from mtrade.application.users.services import UserAppServices
from mtrade.application.market.order_group.services import OrderGroupAppServices


from scripts.db_content_manager import populate_db as pdb

# local imports
from . import views

RESOURCE_ACTIONS = {
    'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
}

COLLECTION_ACTIONS = {
    # 'post': 'create',
    'get': 'list',
}


class OrderGroupViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        try:
            pdb.create_addresses()
            pdb.create_files()
            pdb.create_user_settings()
            pdb.create_users()
            pdb.create_institution_managers()
            pdb.create_controllers()

            pdb.create_compliance_officers()
            pdb.create_institution_leads()
            pdb.create_institution_licenses()
            pdb.create_institutions()
            pdb.create_trader_licenses()
            pdb.create_traders()
            pdb.create_contact_persons()
            pdb.create_leads()
            pdb.create_concierges()
            pdb.create_security_issuers()
            pdb.create_securities()

            pdb.create_order_groups()

        except Exception:
            cls.fail('Could not perform setupdata for OrderGroupViewSetTests')

    def setUp(self):
        try:
            self.factory = APIRequestFactory()
            self.order_group_resource_view = views.OrderGroupViewSet.as_view(
                RESOURCE_ACTIONS)
            self.order_group_collection_view = views.OrderGroupViewSet.as_view(
                COLLECTION_ACTIONS)
            self.user = get_user_model().objects.filter(is_superuser=False)[0]

        except Exception:
            self.fail('Could not pergorm setup for OrderGroupViewSetTests')

    def test_list_order_groups(self):
        request = self.factory.get('/v0/order-group/')
        force_authenticate(request, user=self.user)
        response = self.order_group_collection_view(request)
        self.assertIs(response.status_code, 200)

    def test_retrieve_order_group_by_id(self):
        # request = self.factory.get(f'/v0/order-group/{}')
        pass
