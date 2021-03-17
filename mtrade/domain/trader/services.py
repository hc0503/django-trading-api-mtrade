# python imports
from typing import Type

# django imports
from django.db.models.manager import BaseManager

# local imports
from .models import Trader, TraderFactory, TraderLicense


class TraderServices():

    @staticmethod
    def get_trader_factory() -> Type[TraderFactory]:
        return TraderFactory

    @staticmethod
    def get_trader_repo() -> BaseManager[Trader]:
        return Trader.objects

    @staticmethod
    def get_trader_by_id(trader_id) -> Type[Trader]:
        return Trader.objects.get(id=trader_id)

    @staticmethod
    def get_trader_license_repo() -> BaseManager[TraderLicense]:
        return TraderLicense.objects
