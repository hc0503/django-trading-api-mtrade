# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    OrderGroupID, OrderGroup, OrderGroupFactory
)
from .services import OrderGroupServices


class OrderGroupTests(TestCase):
    # TODO: implement tests. May be redundant, since they are forcefully tested in application tests
    pass


class OrderGroupServicesTests(TestCase):
    def test_order_group_repo(self):
        repo = OrderGroupServices.get_order_group_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_order_group_factory(self):
        factory = OrderGroupServices.get_order_group_factory()
        self.assertEqual(OrderGroupFactory, factory)
