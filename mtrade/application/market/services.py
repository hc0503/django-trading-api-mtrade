# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.market.services import MarketServices as ms
from mtrade.domain.market.models import Market, ISIN, MarketFactory


class MarketAppServices():
    @staticmethod
    def list_markets(user) -> QuerySet:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return ms.get_market_repo().all()

    @staticmethod
    def create_market_from_dict(user, data: dict) -> Market:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        isin = ISIN(data["isin"])
        is_open = data["open"]

        market = MarketFactory.build_entity_with_id(isin, is_open)
        market.save()
        return market

    @staticmethod
    def update_market_from_dict(user, instance: Market, data: dict) -> Market:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        # get market by id

        data_isin = data.get('isin', None)
        data_is_open = data.get('open', None)

        isin = None
        if data_isin:
            isin = ISIN(data['isin'])

        instance.update_entity(isin, data_is_open)
        instance.save()
        return instance
