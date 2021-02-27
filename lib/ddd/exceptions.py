from dataclasses import dataclass

class VOException(Exception):
    """
    Base class for value object exceptions
    """
    pass

@dataclass(frozen=True)
class VOValidationExcpetion(VOException):
    item: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.item, self.message)


