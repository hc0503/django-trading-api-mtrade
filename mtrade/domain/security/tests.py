# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    SecurityIssuer, Security, SecurityFactory, SecurityIssuerFactory
)
from .services import SecurityServices
from scripts.db_content_manager import populate_db as pdb


class SecurityTests(TestCase):

    def test_create_securities(self):
        try:
            pdb.create_security_issuers()
            pdb.create_securities()
        except Exception:
            self.fail('Failed in creating securities')
        security = Security.objects.all()[0]
        self.assertEqual(Security, type(security))


class SecurityServicesTests(TestCase):
    def test_get_security_repo(self):
        repo = SecurityServices.get_security_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_security_factory(self):
        factory = SecurityServices.get_security_factory()
        self.assertEqual(SecurityFactory, factory)
