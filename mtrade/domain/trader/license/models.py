from dataclasses import dataclass
import uuid

from django.db import models

from lib.django import custom_models
from lib.ddd.exceptions import VOValidationExcpetion


class TraderLicense(custom_models.DatedModel):
    """
    Represents a Trader License.
    """
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=500)


@dataclass(frozen=True)
class TraderLicenseID():
    """
    This is a value object that should be used to generate and pass the
    TraderLicenseID to the TraderFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class TraderLicenseMetadata():
    """
    This is a value object that should be used to generate and pass the
    TraderLicenseMetadata to the TraderFactory
    """
    name: str
    short_description: str

    def __post_init__(self):
        self.validate_name()
        self.validate_short_description()

    def validate_name(self):
        if self.name == "":
            raise VOValidationExcpetion(
                "TraderLicenseMetadata name", "cannot be empty")
        if len(self.name) > 100:
            raise VOValidationExcpetion(
                "TraderLicenseMetadata name", "Invalid length")

    def validate_short_description(self):
        if len(self.short_description) > 250:
            raise VOValidationExcpetion(
                "TraderLicenseMetadata short_description",
                "Invalid length")


class TraderLicenseFactory():
    @staticmethod
    def build_entity(
            tl_id=TraderLicenseID,
            tl_md=TraderLicenseMetadata) -> TraderLicense:
        return TraderLicense(
            id=tl_id.value, name=tl_md.name,
            short_description=tl_md.short_description)

    @classmethod
    def build_entity_with_id(
            cls, tl_md=TraderLicenseMetadata) -> TraderLicense:
        tl_id = TraderLicenseID(uuid.uuid4())
        return cls.build_entity(tl_id, tl_md)
