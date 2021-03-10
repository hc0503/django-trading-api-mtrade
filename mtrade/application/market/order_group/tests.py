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
        pdb.create_trader_licenses()
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
        data = pdb.create_order_group_data()
        order_group = ogas.create_order_group_from_dict(None, data)
        self.assertEqual(type(order_group), OrderGroup)

        # Test order group was stored
        stored_order_group = ogs.get_order_group_repo().get(id=order_group.id)
        self.assertEqual(type(stored_order_group), OrderGroup)

    def test_update_order_group(self):
        data = pdb.create_order_group_data()
        order_group = ogas.create_order_group_from_dict(None, data)

        pre_update_created_at = order_group.created_at
        pre_update_modified_at = order_group.modified_at

        updated_data = pdb.create_order_group_data()

        ogas.update_order_group_from_dict(None, order_group, updated_data)

        order_group.refresh_from_db()
        self.assertEqual(order_group.resp_received,
                         updated_data['resp_received'])
        self.assertEqual(order_group.weighted_avg_price,
                         updated_data['weighted_avg_price'])
        self.assertEqual(order_group.weighted_avg_yield,
                         updated_data['weighted_avg_yield'])
        self.assertEqual(order_group.status, updated_data['status'])
        self.assertEqual(order_group.allocation_pct,
                         updated_data['allocation_pct'])

        self.assertEqual(order_group.created_at, pre_update_created_at)
        self.assertNotEqual(order_group.modified_at, pre_update_modified_at)
