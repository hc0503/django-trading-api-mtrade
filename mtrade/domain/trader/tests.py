import uuid

from django.db.models.manager import Manager
from django.test import TestCase

from . import test_helper as th
from .models import InstitutionID, TraderFactory, TraderID
from .license.models import TraderLicenseFactory, TraderLicenseMetadata
# from .services import TraderServices


class TraderTests(TestCase):

    @classmethod
    def setUp(cls):
        tl_md = TraderLicenseMetadata(
            "Dummy License", "The greatest license in the world")
        cls.trader_license_01 = TraderLicenseFactory.build_entity_with_id(
            tl_md)

    def test_build_trader_id(self):
        try:
            TraderID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_institution_id(self):
        try:
            InstitutionID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_trader(self):
        try:
            TraderFactory.build_entity_with_id(
                self.trader_license_01,
                InstitutionID(uuid.uuid4()))
        except Exception:
            self.fail("Unexpected exception")

    # def test_build_traders(self):
    #    mkts = th.generate_random_traders(5)
    #    self.assertEqual(len(mkts), 5)


# class TraderServicesTests(TestCase):
#    def test_get_trader_repo(self):
#        repo = TraderServices.get_trader_repo()
#        self.assertEqual(Manager, type(repo))
#
#    def test_get_trader_factory(self):
#        factory = TraderServices.get_trader_factory()
#        self.assertEqual(TraderFactory, factory)
