# python imports
import typing

# django imports
from django.utils.crypto import get_random_string

# app imports

# local imports
from .models import (
    ISIN,
    Market,
    MarketFactory
)

# TODO: set a constant random seed to get repeatable results
def generate_random_isin() -> ISIN:
    return ISIN(get_random_string(12))

def generate_random_market() -> Market:
    return MarketFactory.build_entity_with_id(generate_random_isin(), True)

def generate_random_markets(num_of_markets: int) -> typing.List[Market]:
    markets = []
    for _ in range(num_of_markets):
        markets.append(generate_random_market())
    return markets
