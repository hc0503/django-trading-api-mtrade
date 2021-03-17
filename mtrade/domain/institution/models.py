import logging
import uuid

from dataclasses import dataclass

from django.db import models
from datetime import datetime
from lib.django import custom_models

from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import ArrayField

from lib.data_manipulation.daydiff import daydiff


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InstitutionManagerID():
    """
    This is a value object that should be used to generate and pass the InstitutionManagerID to the InstitutionManagerFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class InstitutionLicenseID():
    """
    This is a value object that should be used to generate and pass the InstitutionLicenseID to the InstitutionLicenseFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class InstitutionID():
    """
    This is a value object that should be used to generate and pass the InstitutionID to the InstitutionFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class SettlementInstructionID():
    """
    This is a value object that should be used to generate and pass the SettlementInstructionID to the SettlementInstructionFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class RfqLockID():
    """
    This is a value object that should be used to generate and pass the RfqLockID to the RfqLockFactory
    """
    value: uuid.UUID


class InstitutionManager(custom_models.DatedModel):
    """
    Represents an Institution Manager
    """
    class Meta:
        ordering = ['id']

    # InstitutionManger.id must be the same as the id of the user it relates to
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)


class InstitutionLicense(custom_models.DatedModel):
    """
    Represents an Institution License.

    TRADING_LICENSE = 'trading'
    VIEW_ONLY_LICENSE = 'data'
    """
    class Meta:
        ordering = ['id']

    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=500)


class Institution(custom_models.DatedModel):
    """
    Represents an Institution
    """
    class Meta:
        ordering = ['id']

    ENABLED_STATUS = 'enabled'
    DISABLED_STATUS = 'disabled'
    STATUS_CHOICES = [
        (ENABLED_STATUS, 'enabled'),
        (DISABLED_STATUS, 'disabled')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250, unique=True)
    # contract: ref to File
    contract_id = models.UUIDField()
    rfc = models.CharField(max_length=350, unique=True)
    # logo: ref to File
    logo_id = models.UUIDField()
    manager = models.ForeignKey(
        InstitutionManager, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    license_type = models.ForeignKey(
        InstitutionLicense, on_delete=models.SET_NULL,  null=True)

    demo_licenses = models.PositiveIntegerField()
    trade_licenses = models.PositiveIntegerField()
    data_licenses = models.PositiveIntegerField()
    curp = models.CharField(max_length=50, unique=True)
    # ref to ComplianceOfficer
    compliance_officer_id = models.UUIDField()
    # ref to Address
    address = models.UUIDField()


class SettlementInstruction(custom_models.DatedModel):
    """
    Represents a Settlement Instruction
    """

    class Meta:
        ordering = ['id']

    # these clearing valiues ust be in sync with securities'
    INDEVAL_CLEARING = 'indeval'
    DTC_CLEARING = 'dtc'
    EUROCLEAR_CLEARING = 'euroclear'
    CLEARSTREAM_CLEARING = 'clearstream'
    CLEARING_CHOICES = (
        (INDEVAL_CLEARING, 'Indeval'),
        (DTC_CLEARING, 'DTC'),
        (EUROCLEAR_CLEARING, 'Euroclear'),
        (CLEARSTREAM_CLEARING, 'Clearstream')
    )

    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]

    name = models.CharField(max_length=250)
    # ref to File
    document_id = models.UUIDField()
    clearing_house = models.CharField(max_length=250, choices=CLEARING_CHOICES)
    account = models.CharField(max_length=250)
    bic_code = models.CharField(max_length=250)
    custodian = models.CharField(max_length=250)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    # ref to Trader
    trader_id = models.UUIDField()
    status = models.CharField(max_length=250, choices=STATUS_CHOICES)
    deactivated_at = models.DateTimeField(null=True, blank=True)


class RfqLock(custom_models.DatedModel):
    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    # ref to Trader
    trader_id = models.UUIDField()
    # ref to Institution
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)


class InstitutionManagerFactory():
    @staticmethod
    def build_entity(institution_manager_id: InstitutionManagerID, **kwargs) -> InstitutionManager:
        institution_manager = InstitutionManager(
            id=institution_manager_id.value, **kwargs)
        institution_manager.full_clean()
        return institution_manager

    @classmethod
    def build_entity_with_id(cls,  **kwargs):
        institution_manager_id = InstitutionManagerID(uuid.uuid4())
        return cls.build_entity(institution_manager_id=institution_manager_id, **kwargs)


class InstitutionLicenseFactory():
    @staticmethod
    def build_entity(institution_license_id: InstitutionLicenseID, **kwargs) -> InstitutionLicense:
        institution_license = InstitutionLicense(
            id=institution_license_id.value, **kwargs)
        institution_license.full_clean()
        return institution_license

    @classmethod
    def build_entity_with_id(cls,  **kwargs):
        institution_license_id = InstitutionLicenseID(uuid.uuid4())
        return cls.build_entity(institution_license_id=institution_license_id, **kwargs)


class InstitutionFactory():
    @staticmethod
    def build_entity(institution_id: InstitutionID, **kwargs) -> Institution:
        institution = Institution(
            id=institution_id.value, **kwargs)
        institution.full_clean()
        return institution

    @classmethod
    def build_entity_with_id(cls,  **kwargs):
        institution_id = InstitutionID(uuid.uuid4())
        return cls.build_entity(institution_id=institution_id, **kwargs)


class SettlementInstructionFactory():
    @staticmethod
    def build_entity(settlement_instruction_id: SettlementInstructionID, **kwargs) -> SettlementInstruction:
        settlement_instruction = SettlementInstruction(
            id=settlement_instruction_id.value, **kwargs)
        settlement_instruction.full_clean()
        return settlement_instruction

    @classmethod
    def build_entity_with_id(cls,  **kwargs):
        settlement_instruction_id = SettlementInstructionID(uuid.uuid4())
        return cls.build_entity(settlement_instruction_id=settlement_instruction_id, **kwargs)


class RfqLockFactory():
    @staticmethod
    def build_entity(rfq_lock_id: RfqLockID, **kwargs) -> RfqLock:
        rfq_lock = RfqLock(
            id=rfq_lock_id.value, **kwargs)
        rfq_lock.full_clean()
        return rfq_lock

    @classmethod
    def build_entity_with_id(cls,  **kwargs):
        rfq_lock_id = RfqLockID(uuid.uuid4())
        return cls.build_entity(rfq_lock_id=rfq_lock_id, **kwargs)
