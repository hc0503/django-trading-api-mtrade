# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import OrderGroupFactory
from .models import OrderGroup


class OrderGroupServices():

    @staticmethod
    def get_order_group_factory() -> Type[OrderGroupFactory]:
        return OrderGroupFactory

    @staticmethod
    def get_order_group_repo() -> Type[Manager]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return OrderGroup.objects
