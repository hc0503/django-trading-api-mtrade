# django imports
from django.db.models.query import QuerySet

# app imports
from lib.django.custom_models import ModelDates
from mtrade.domain.market.services import MarketServices as ms
from mtrade.domain.market.models import Market, MarketID, ISIN, MarketFactory

class MarketAppServices():
    @staticmethod
    def list_markets(user) -> QuerySet:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return ms.get_market_repo().all()

    def create_market_from_dict(user, data: dict) -> Market:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        isin = ISIN(data["isin"])
        is_open = data["open"]

        market = MarketFactory.build_entity_with_id(isin, is_open)
        market.save()
        return market

    def update_market_from_dict(user, instance: Market, data: dict) -> Market:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        # get market by id

        # This is an update so we expect to fail if any of the required fields is not present.
        isin = ISIN(data['isin'])
        open = data['open']

        instance.update_entity(isin, open)
        instance.save()
        return instance
