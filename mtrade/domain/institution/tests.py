import uuid

# django imports
from django.test import TestCase
from django.db.models.manager import Manager

# app imports
from lib.ddd.exceptions import VOValidationExcpetion

# local imports
from .models import (
    InstitutionID,
    Institution,
    InstitutionFactory,

    InstitutionLicenseID,
    InstitutionLicense,
    InstitutionLicenseFactory,

    InstitutionManagerID,
    InstitutionManager,
    InstitutionManagerFactory,

    SettlementInstructionID,
    SettlementInstruction,
    SettlementInstructionFactory,

    RfqLockID,
    RfqLock,
    RfqLockFactory
)
from .services import InstitutionServices
from scripts.db_content_manager import populate_db as pdb


class InstitutionTests(TestCase):
    # TODO: implement tests
    pass


class InstitutionManagerTests(TestCase):
    # TODO: implement tests
    pass


class InstitutionLicenseTests(TestCase):
    # TODO: implement tests
    pass


class SettlementInstructionTests(TestCase):
    # TODO: implement tests
    pass


class RfqLockTests(TestCase):
    # TODO: implement tests
    pass
