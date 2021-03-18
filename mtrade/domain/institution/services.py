# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import (SettlementInstruction,
                     SettlementInstructionFactory,

                     Institution,
                     InstitutionFactory,

                     InstitutionLicense,
                     InstitutionLicenseFactory,

                     InstitutionManager,
                     InstitutionManagerFactory,

                     RfqLock,
                     RfqLockFactory)


class InstitutionServices():
    # INSTITUTIONS
    @staticmethod
    def get_institution_factory() -> Type[InstitutionFactory]:
        return InstitutionFactory

    @staticmethod
    def get_institution_repo() -> Type[Manager]:
        return Institution.objects

    # INSTITUTION LICENSES

    @staticmethod
    def get_institution_license_factory() -> Type[InstitutionLicenseFactory]:
        return InstitutionLicenseFactory

    @staticmethod
    def get_institution_license_repo() -> Type[Manager]:
        return InstitutionLicense.objects

    # INSTITUTION MANAGERS
    @staticmethod
    def get_institution_manager_factory() -> Type[InstitutionManagerFactory]:
        return InstitutionManagerFactory

    @staticmethod
    def get_institution_manager_repo() -> Type[Manager]:
        return InstitutionManager.objects

    # SETTLEMENT INSTRUCTIONS
    @staticmethod
    def get_settlement_instruction_factory() -> Type[SettlementInstructionFactory]:
        return SettlementInstructionFactory

    @staticmethod
    def get_settlement_instruction_repo() -> Type[Manager]:
        return SettlementInstruction.objects

    # RFQ LOCKS
    @staticmethod
    def get_rfq_lock_factory() -> Type[RfqLockFactory]:
        return RfqLockFactory

    @staticmethod
    def get_rfq_lock_repo() -> Type[Manager]:
        return RfqLock.objects
