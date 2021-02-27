# python imports
import json
from pathlib import Path

# django imports
from django_mock_queries.query import MockSet, MockModel

# app imports
from mtrade.domain.market.services import MarketServices as ms
from mtrade.domain.market.models import Market, ISIN, MarketFactory

class MarketAppServices():
    @staticmethod
    def list_markets(user):
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return ms.get_market_repo().all()

    def create_market(user, isin, is_open):
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return MarketFactory.build_entity_with_id(isin, is_open)


class COBAppServices():

    dummy_orders = None

    path = Path(__file__).parent / "dummy_data/coborder.json"
    with path.open(mode='r') as f:
        dummy_orders = json.load(f)

    mock_models = []
    for order in dummy_orders:
        order["mock_name"] = order["id"]
        m = MockModel(order)
        mock_models.append(m)
        #print(m)

    mock_cob_queryset = MockSet(*mock_models)

    @classmethod
    def list_cob_orders(cls, user, market_id):
        # TODO:
        # Fetch trader by user id
        # If trader does not exist propagate or handle exception
        return cls.mock_cob_queryset.filter(isin=market_id)
