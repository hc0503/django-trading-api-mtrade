# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    OrderGroupID, OrderGroup
)
from .services import OrderGroupServices


class OrderGroupTests(TestCase):
    # TODO: implement tests
    pass


class OrderGroupServicesTests(TestCase):
    # TODO: implement tests
    pass
