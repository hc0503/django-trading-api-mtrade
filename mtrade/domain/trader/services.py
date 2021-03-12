# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import Trader, TraderFactory, TraderLicense


class TraderServices():

    @staticmethod
    def get_trader_factory() -> Type[TraderFactory]:
        return TraderFactory

    @staticmethod
    def get_trader_repo() -> Type[Manager]:
        return Trader.objects

    @staticmethod
    def get_trader_license_repo() -> Type[Manager]:
        return TraderLicense.objects
