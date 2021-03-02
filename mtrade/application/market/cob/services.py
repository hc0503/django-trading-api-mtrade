# python imports
import json
from pathlib import Path

# django imports
from django_mock_queries.query import MockSet, MockModel

class COBAppServices():

    dummy_orders = None

    path = Path(__file__).parent / "dummy_data/coborder.json"
    with path.open(mode='r') as data_file:
        dummy_orders = json.load(data_file)

    mock_models = []
    for order in dummy_orders:
        order["mock_name"] = order["id"]
        mock = MockModel(order)
        mock_models.append(mock)
        #print(m)

    mock_cob_queryset = MockSet(*mock_models)

    @classmethod
    def list_cob_orders(cls, user, market_id):
        # TODO:
        # Fetch trader by user id
        # If trader does not exist propagate or handle exception
        return cls.mock_cob_queryset.filter(isin=market_id)
