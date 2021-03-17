from dataclasses import dataclass

class MarketException(Exception):
    """
    Base class for value object exceptions
    """
    pass

@dataclass(frozen=True)
class InvalidMarketOperationException(MarketException):
    item: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.item, self.message)
