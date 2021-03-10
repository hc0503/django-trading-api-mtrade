# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    SecurityIssuer, Security
)
from .services import SecurityServices


class SecurityTests(TestCase):
    # TODO: implement tests
    pass


class SecurityServicesTests(TestCase):
    # TODO: implement tests
    pass
