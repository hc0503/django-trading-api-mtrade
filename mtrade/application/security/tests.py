# python imports

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet

# local imports
from .services import SecurityAppServices as sas


class SecurityAppServicesTests(TestCase):

    def test_list_securities(self):
        securities = sas.list_securities()
        self.assertEqual(type(securities), QuerySet)
