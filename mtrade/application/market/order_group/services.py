# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.market.order_group.services import OrderGroupServices as ogs

from mtrade.domain.market.order_group.models import OrderGroup, OrderGroupFactory

from mtrade.domain.trader.services import TraderServices


class OrderGroupAppServices():
    @staticmethod
    def list_order_groups(user) -> QuerySet:
        """returns a list of order groups where requesting user's id is trader_id If user does not have a trader profile, propagate exception."""
        # FIXME: what happens if user id does not correspond to a trader id. Handle this.
        # check user is trader
        trader_id = user.id
        trader = TraderServices.get_trader_repo().get(id=trader_id)
        # TODO: when licenses are defined, check trader has correct license
        traders_order_groups = ogs.get_order_group_repo().filter(trader_id=trader_id)
        return traders_order_groups

    @staticmethod
    def retrieve_order_group(user, order_group_id) -> OrderGroup:
        """Returns requested"""
        # FIXME: what happens if user tries to access id does not correspond to a trader id. Handle this.
        pass

    @staticmethod
    def create_order_group_from_dict(user, data: dict) -> OrderGroup:
        # TODO: Check user or trader has permission to perform this action
        order_group = OrderGroupFactory.build_entity_with_id(**data)
        order_group.save()
        return order_group

    @staticmethod
    def update_order_group_from_dict(user, instance: OrderGroup, data: dict) -> OrderGroup:
        # Only certain fields may be updated
        # TODO: Check user or trader has permissions on this object
        instance.update_entity(**data)
        instance.save()
        return instance
