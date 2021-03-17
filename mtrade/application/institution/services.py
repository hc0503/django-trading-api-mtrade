# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.institution.services import InstitutionServices
from mtrade.domain.institution.models import (Institution,
                                              InstitutionFactory,
                                              InstitutionLicense,
                                              InstitutionLicenseFactory,
                                              InstitutionManager,
                                              InstitutionManagerFactory,
                                              SettlementInstruction,
                                              SettlementInstructionFactory)

from mtrade.domain.market.order_group.models import OrderGroup, OrderGroupFactory


class InstitutionAppServices():
    @staticmethod
    def list_institutions() -> QuerySet:
        insitutions = InstitutionServices.get_institution_repo()
        return insitutions

    @staticmethod
    def get_institution_by_id(institution_id) -> Institution:
        return InstitutionServices.get_institution_repo().get(id=institution_id)

    @staticmethod
    def list_institution_managers() -> QuerySet:
        institution_managers = InstitutionServices.get_institution_manager_repo()
        return institution_managers

    @staticmethod
    def list_institution_licenses() -> QuerySet:
        institution_licenses = InstitutionServices.get_institution_license_repo()
        return institution_licenses

    @staticmethod
    def list_settlement_instructions() -> QuerySet:
        settlement_instructions = InstitutionServices.get_settlement_instruction_repo()
        return settlement_instructions

    @staticmethod
    def list_rfq_locks() -> QuerySet:
        rfq_locks = InstitutionServices.get_rfq_lock_repo()
        return rfq_locks
