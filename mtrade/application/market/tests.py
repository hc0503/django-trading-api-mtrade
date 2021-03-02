# python imports
from time import sleep

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# local imports

from .services import MarketAppServices as mas
from mtrade.domain.market.models import Market, MarketID, ISIN
from mtrade.domain.market.services import MarketServices as ms

class MarketAppServicesTests(TestCase):

    def test_list_markets(self):
        mq = mas.list_markets(None)
        self.assertEquals(type(mq), QuerySet)

    def test_create_market(self):
        data = {
            "isin":"123456789012",
            "open":True
        }
        m = mas.create_market_from_dict(None, data)
        self.assertEquals(type(m), Market)

        # Test market was stored
        stored_market = ms.get_market_repo().get(id=m.id)
        self.assertEquals(type(stored_market), Market)

    def test_update_market(self):
        data = {
            "isin":"123456789012",
            "open":True
        }
        m = mas.create_market_from_dict(None, data)

        pre_update_created_at = m.created_at
        pre_update_modified_at = m.modified_at

        updated_data = {
            "isin":"123456789012",
            "open":False
        }

        mu = mas.update_market_from_dict(None, m, updated_data)

        m.refresh_from_db()
        self.assertEquals(m.open, False)

        self.assertEquals(m.created_at, pre_update_created_at)
        self.assertNotEqual(m.modified_at, pre_update_modified_at)
