# python imports

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# app imoprts
from mtrade.domain.market.order_group.models import OrderGroup
# from mtrade.domain.market.models import Market
from mtrade.domain.market.order_group.services import OrderGroupServices as ogs
from scripts.db_content_manager import populate_db as pdb
# from mtrade.domain.market.services import MarketServices as ms

# local imports
from .services import OrderGroupAppServices as ogas
# from .services import MarketAppServices as mas


class OrderGroupAppServicesTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        pdb.create_addresses()
        pdb.create_files()
        pdb.create_user_settings()
        pdb.create_users()
        pdb.create_institution_managers()
        pdb.create_controllers()

        pdb.create_compliance_officers()
        pdb.create_institution_leads()
        pdb.create_institutions()
        pdb.create_traders()
        pdb.create_contact_persons()
        pdb.create_leads()
        pdb.create_concierges()
        pdb.create_security_issuers()
        pdb.create_securities()

        pdb.create_order_groups()

    def test_list_order_groups(self):
        order_groups = ogas.list_order_groups(None)
        self.assertEqual(type(order_groups), QuerySet)

    def test_create_order_group(self):

        pass

    def test_update_market(self):
        pass
