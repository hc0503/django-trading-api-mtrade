# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.trader.services import TraderServices as ts
from mtrade.domain.trader.models import Trader, TraderFactory, TraderID


class TraderAppServices():
    @staticmethod
    def list_traders() -> QuerySet:
        return ts.get_trader_repo().all()
