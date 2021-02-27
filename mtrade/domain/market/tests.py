# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    Market,
    MarketID,
    ISIN,
    MarketFactory
)
from .services import MarketServices
from . import test_helper as th


class MarketTests(TestCase):

    def test_build_market_id(self):
        try:
            m = MarketID
        except Exception:
            self.fail("Unexpected exception")

    def test_build_ISIN(self):
        try:
            pass
            m = ISIN("123456789012")
        except Exception:
            self.fail("Unexpected exception")

        with self.assertRaises(VOValidationExcpetion):
            m = ISIN("12345678901")

    def test_build_market(self):
        try:
            MarketFactory.build_entity_with_id(ISIN("123456789012"),True)
        except Exception:
            self.fail("Unexpected exception")

    def test_build_markets(self):
        mkts = th.generate_random_markets(5)
        self.assertEquals(len(mkts), 5)


class MarketServicesTests(TestCase):
    def test_get_market_repo(self):
        repo = MarketServices.get_market_repo()
        self.assertEquals(Manager, type(repo))
