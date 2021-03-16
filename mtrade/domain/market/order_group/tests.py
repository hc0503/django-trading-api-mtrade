import uuid

# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    OrderGroupID,
    OrderGroup,
    OrderGroupFactory,
    SecurityID,
    RequestorID,
    TraderID
)
from .services import OrderGroupServices
from scripts.db_content_manager import populate_db as pdb


class OrderGroupTests(TestCase):

    def test_build_trader_id(self):
        try:
            TraderID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_order_group_id(self):
        try:
            OrderGroupID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_security_id(self):
        try:
            SecurityID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_requestor_id(self):
        try:
            RequestorID(uuid.uuid4())
        except Exception:
            self.fail("Unexpected exception")

    def test_build_order_id(self):
        try:
            data = pdb.create_order_group_data(test=True)
            OrderGroupFactory.build_entity_with_id(**data)
        except Exception:
            self.fail("Unexpected exception")

    # TODO: implement tests for BaseOrderGroupParams related values


class OrderGroupServicesTests(TestCase):
    def test_order_group_repo(self):
        repo = OrderGroupServices.get_order_group_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_order_group_factory(self):
        factory = OrderGroupServices.get_order_group_factory()
        self.assertEqual(OrderGroupFactory, factory)
