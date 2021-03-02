# django imports
from django.db.models.query import QuerySet
from django.db.models.manager import Manager

# local imports
from .models import MarketFactory
from .models import Market


class MarketServices():

    @staticmethod
    def get_market_factory() -> MarketFactory:
        return MarketFactory

    @staticmethod
    def get_market_repo() -> Manager:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return Market.objects
