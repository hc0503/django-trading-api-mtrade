from dataclasses import dataclass
import uuid

from django.db import models

from lib.django import custom_models

from .license.models import TraderLicense


class Trader(custom_models.DatedModel):
    """
    Represents a Trader
    """
    # This id must be the same id as the user it relates to
    id = models.UUIDField(primary_key=True, editable=False)
    license = models.ForeignKey(
        TraderLicense,
        on_delete=models.SET_NULL,
        null=True)
    institution_id = models.UUIDField(null=True)


@dataclass(frozen=True)
class TraderID():
    """
    This is a value object that should be used to generate and pass the
    TraderID to the TraderFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class InstitutionID():
    """
    This is a value object that should be used to generate and pass the
    InstitutionID to the TraderFactory
    """
    value: uuid.UUID


class TraderFactory():
    @staticmethod
    def build_entity(
            trader_id: TraderID,
            trader_license: TraderLicense,
            institution_id: InstitutionID) -> Trader:
        return Trader(
            id=trader_id.value,
            license=trader_license,
            institution_id=institution_id)

    @classmethod
    def build_entity_with_id(
            cls,
            trader_license: TraderLicense,
            institution_id: InstitutionID) -> Trader:
        trader_id = TraderID(uuid.uuid4())
        return cls.build_entity(trader_id, trader_license, institution_id)
