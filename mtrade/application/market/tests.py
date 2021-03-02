# python imports

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# app imoprts
from mtrade.domain.market.models import Market
from mtrade.domain.market.services import MarketServices as ms

# local imports
from .services import MarketAppServices as mas

class MarketAppServicesTests(TestCase):

    def test_list_markets(self):
        mqs = mas.list_markets(None)
        self.assertEqual(type(mqs), QuerySet)

    def test_create_market(self):
        data = {
            "isin":"123456789012",
            "open":True
        }
        mkt = mas.create_market_from_dict(None, data)
        self.assertEqual(type(mkt), Market)

        # Test market was stored
        stored_market = ms.get_market_repo().get(id=mkt.id)
        self.assertEqual(type(stored_market), Market)

    def test_update_market(self):
        data = {
            "isin":"123456789012",
            "open":True
        }
        mkt = mas.create_market_from_dict(None, data)

        pre_update_created_at = mkt.created_at
        pre_update_modified_at = mkt.modified_at

        updated_data = {
            "isin":"123456789012",
            "open":False
        }

        mas.update_market_from_dict(None, mkt, updated_data)

        mkt.refresh_from_db()
        self.assertEqual(mkt.open, False)

        self.assertEqual(mkt.created_at, pre_update_created_at)
        self.assertNotEqual(mkt.modified_at, pre_update_modified_at)
