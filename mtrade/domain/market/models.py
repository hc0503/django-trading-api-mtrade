# python imports
import uuid
from dataclasses import dataclass, field

# django imports
from django.db import models

# app imports
#from lib.data_manipulation.type_conversion import asdict

# local imports


class Market(models.Model):
    """
    A Market represents the entrypoint for any type of trades of a given security
    """
    id = models.UUIDField(primary_key=True, editable=False)
    isin = models.CharField(max_length=24, unique=True)
    open = models.BooleanField()


@dataclass(frozen=True)
class MarketID():
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """
    value: uuid.UUID = field(init=False, default_factory=uuid.uuid4)

@dataclass(frozen=True)
class ISIN():
    value: str

    def __post_init__(self):
        self.validate_length()

    def validate_length(self):
        if len(self.value) < 12:
            raise ValueError("Invalid ISIN length")

class MarketFactory():
    @staticmethod
    def build_entity_with_id(isin: ISIN, open:bool) -> Market:
        return Market(id=MarketID().value, isin=isin.value, open=open)
