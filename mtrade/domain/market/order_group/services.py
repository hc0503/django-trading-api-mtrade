from typing import Type

from django.db.models.manager import BaseManager

from .models import OrderGroup, OrderGroupFactory


class OrderGroupServices():

    @staticmethod
    def get_order_group_factory() -> Type[OrderGroupFactory]:
        return OrderGroupFactory

    @staticmethod
    def get_order_group_repo() -> BaseManager[OrderGroup]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return OrderGroup.objects
