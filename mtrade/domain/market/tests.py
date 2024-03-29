# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    MarketID,
    ISIN,
    MarketFactory
)
from .services import MarketServices
from . import test_helper as th


class MarketTests(TestCase):

    def test_build_market_id(self):
        try:
            MarketID
        except Exception:
            self.fail("Unexpected exception")

    def test_build_isin(self):
        try:
            ISIN("123456789012")
        except Exception:
            self.fail("Unexpected exception")

        with self.assertRaises(VOValidationExcpetion):
            ISIN("12345678901")

    def test_build_market(self):
        try:
            MarketFactory.build_entity_with_id(ISIN("123456789012"),True)
        except Exception:
            self.fail("Unexpected exception")

    def test_build_markets(self):
        mkts = th.generate_random_markets(5)
        self.assertEqual(len(mkts), 5)


class MarketServicesTests(TestCase):
    def test_get_market_repo(self):
        repo = MarketServices.get_market_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_market_factory(self):
        factory = MarketServices.get_market_factory()
        self.assertEqual(MarketFactory, factory)
