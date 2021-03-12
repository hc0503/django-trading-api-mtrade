# python imports
from typing import List

from mtrade.domain.users.models import User

class TestData:
    def __init__(self, id, payload):
        self.id = id
        self.payload = payload

def test_populator(user: User) -> List[TestData]:
    data : List[TestData] = []
    data.append(TestData(1, 'Inital message testing 1'))
    data.append(TestData(2, 'Inital message testing 2'))
    return data