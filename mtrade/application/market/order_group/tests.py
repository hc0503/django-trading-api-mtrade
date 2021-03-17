# python imports
from decimal import Decimal
from datetime import datetime
# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# app imoprts
from mtrade.domain.market.order_group.models import (OrderGroup,
                                                     ResponsesReceived,
                                                     WeightedAverageSpread,
                                                     WeightedAveragePrice,
                                                     WeightedAverageYield,
                                                     FX,
                                                     OrderGroupStatus,
                                                     AllocationProgress,
                                                     ResponsesReceived,
                                                     Priority)
from mtrade.domain.trader.services import TraderServices
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
            cls.fail('Could not perform setup for OrderGroupAppServicesTests')

    def test_list_order_groups(self):
        trader = TraderServices.get_trader_repo().all()[0]
        order_groups = ogas.list_order_groups(trader)
        self.assertEqual(type(order_groups), QuerySet)

    def test_retrieve_order_group(self):
        # TODO: implement this test
        pass

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

        new_data = dict(
            weighted_avg_price=WeightedAveragePrice(Decimal('100.1')),
            weighted_avg_yield=WeightedAverageYield(Decimal('0.08')),
            weighted_avg_spread=WeightedAverageSpread(Decimal('10.1')),
            fx=FX(Decimal('20.21')),
            group_status=OrderGroupStatus(OrderGroup.GROUP_STATUS_CANCELLED),
            allocation_progress=AllocationProgress(OrderGroup.ALLOCATION_STATUS_PARTIAL, Decimal('0.05')),
            resp_received=ResponsesReceived(3),
            # priority=Priority(datetime.now())
        )

        ogas.update_order_group_from_dict(None, order_group, new_data)

        order_group.refresh_from_db()
        self.assertEqual(order_group.weighted_avg_price,
                         new_data['weighted_avg_price'].value)
        self.assertEqual(order_group.weighted_avg_yield,
                         new_data['weighted_avg_yield'].value)
        self.assertEqual(order_group.weighted_avg_spread,
                         new_data['weighted_avg_spread'].value)
        self.assertEqual(order_group.fx,
                         new_data['fx'].value)
        self.assertEqual(order_group.group_status,
                         new_data['group_status'].value)
        self.assertEqual(order_group.allocation_pct,
                         new_data['allocation_progress'].percentage),
        self.assertEqual(order_group.allocation_status,
                         new_data['allocation_progress'].status),
        self.assertEqual(order_group.resp_received,
                         new_data['resp_received'].value)

        # self.assertEqual(order_group.priority,
        #                  new_data['priority'].value)

        self.assertEqual(order_group.created_at, pre_update_created_at)
        self.assertNotEqual(order_group.modified_at, pre_update_modified_at)
