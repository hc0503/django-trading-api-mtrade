from datetime import datetime, timedelta
from typing import Generator


def date_linear_generator(
    initial_date: datetime,
    delta: timedelta
) -> Generator:
    """
    Generates dates with 'delta' difference from last generated date
    """
    next_date = initial_date
    while True:
        yield next_date
        next_date += delta
