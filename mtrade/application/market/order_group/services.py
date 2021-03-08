# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.market.order_group.services import OrderGroupServices as ogs

from mtrade.domain.market.order_group.services import OrderGroup, OrderGroupFactory


class OrderGroupAppServices():
    @staticmethod
    def list_order_groups(user) -> QuerySet:
        # TODO: implement this method correctly
        # fetch users trader profile and then go to his order groups order groups. If trader does not exist, propagate or handle exception
        return ogs.get_order_group_repo().all()

    @staticmethod
    def create_order_group_from_dict(user, data: dict) -> OrderGroup:
        # TODO: implement this method. Check market example
        pass

    @staticmethod
    def update_order_group_from_dict(user, instance: OrderGroup, data: dict) -> OrderGroup:
        # TODO: implement this method. Check market example
        pass
