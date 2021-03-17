# python imports

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# app imports

# from mtrade.domain.market.models import Market

from scripts.db_content_manager import populate_db as pdb
# from mtrade.domain.market.services import MarketServices as ms

# local imports

# from .services import MarketAppServices as mas


class InstitutionAppServicesTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        pass

    # TODO: implement tests
