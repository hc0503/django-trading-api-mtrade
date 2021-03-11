import uuid

from django.db.models.manager import Manager
from django.test import TestCase

from lib.ddd.exceptions import VOValidationExcpetion

from . import test_helper as th
from .models import TraderLicenseFactory, TraderLicenseID, TraderLicenseMetadata
from .services import TraderLicenseServices


class TraderLicenseTests(TestCase):

    def test_build_license_id(self):
        try:
            TraderLicenseID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_license_metadata(self):
        try:
            TraderLicenseMetadata(
                name="license name",
                short_description="this is a test license"
            )
        except Exception:
            self.fail("Unexpected exception")

        # tests empty string can't be passed as license name
        with self.assertRaises(VOValidationExcpetion):
            TraderLicenseMetadata("", "a valid description")

        # tests name can't be longer than 100 chars
        with self.assertRaises(VOValidationExcpetion):
            TraderLicenseMetadata("x" * 101, "a valid description")

        # test description can't be longer than 251 chars
        with self.assertRaises(VOValidationExcpetion):
            TraderLicenseMetadata("a valid name", "x" * 251)

    def test_build_license(self):
        tlm = TraderLicenseMetadata(
            name="license name",
            short_description="this is a test license"
        )
        try:
            TraderLicenseFactory.build_entity_with_id(tlm)
        except Exception:
            self.fail("Unexpected exception")

    def test_build_trader_licenses(self):
        mkts = th.gen_rand_licenses(5)
        self.assertEqual(len(mkts), 5)


class TraderLicenseServicesTests(TestCase):
    def test_get_license_repo(self):
        repo = TraderLicenseServices.get_license_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_trader_license_factory(self):
        factory = TraderLicenseServices.get_license_factory()
        self.assertEqual(TraderLicenseFactory, factory)
