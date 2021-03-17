from datetime import datetime
from typing import List, Tuple

import factory
import factory.fuzzy
import factory.random
import pytz

from mtrade.domain.market.order_group.models import OrderGroupFactory
from mtrade.domain.market.order_group.models import OrderGroup
from scripts.db_content_manager import populate_db as pdb

from .models import (
    BaseCOBOrderParams,
    COBOrder,
    COBOrderFactory,
    COBOrderID,
    COBOrderStatus,
    ExtendeCOBOrderParams,
    SecurityID,
    TraderID,
    InstitutionID
)


# Sets initial random seed so all pseudorandom values are reproducible.
factory.random.reseed_random('cob_testhelper')

traderA_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})
traderB_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})

institutionA_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})
institutionB_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})

securityA_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})
securityB_ID = factory.Faker('uuid4').evaluate(None, None, {"locale": None})


class COBOrderIDFactory(factory.Factory):
    class Meta:
        model = COBOrderID

    value = factory.Faker('uuid4')


class TraderIDFactory(factory.Factory):
    class Meta:
        model = TraderID

    value = factory.Faker('uuid4')

    class Params:
        traderA = factory.Trait(
            value=traderA_ID
        )
        traderB = factory.Trait(
            value=traderB_ID
        )


class InstitutionIDFactory(factory.Factory):
    class Meta:
        model = InstitutionID

    value = factory.Faker('uuid4')

    class Params:
        institutionA = factory.Trait(
            value=institutionA_ID
        )
        intitutionB = factory.Trait(
            value=institutionB_ID
        )


class SecurityIDFactory(factory.Factory):
    class Meta:
        model = SecurityID

    value = factory.Faker('uuid4')

    class Params:
        securityA = factory.Trait(
            value=securityA_ID
        )
        securityB = factory.Trait(
            value=securityB_ID
        )


class BaseCOBOrderParamsFactory(factory.Factory):
    class Meta:
        model = BaseCOBOrderParams

    priority = datetime(2020, 3, 15, tzinfo=pytz.UTC)
    expiration = datetime(2020, 3, 16, tzinfo=pytz.UTC)
    price = factory.Faker('pydecimal', positive=True)
    size = factory.Faker('pyint', min_value=0, max_value=999999)
    direction = factory.fuzzy.FuzzyChoice(
        COBOrder.DIRECTION_CHOICES, getter=lambda c: c[0])

    class Params:
        is_bid = factory.Trait(
            direction=COBOrder.DIRECTION_BID
        )
        is_ask = factory.Trait(
            direction=COBOrder.DIRECTION_ASK
        )


class ExtendedCOBOrderParamsFactory(factory.Factory):
    class Meta:
        model = ExtendeCOBOrderParams

    dirty_price = factory.Faker('pydecimal', positive=True)
    notional = factory.Faker('pydecimal', positive=True)
    spread = factory.Faker('pydecimal', positive=True)
    discount_margin = factory.Faker('pydecimal', positive=True)
    yield_value = factory.Faker('pydecimal', positive=True)


class COBOrderStatusFactory(factory.Factory):
    class Meta:
        model = COBOrderStatus

    value = factory.fuzzy.FuzzyChoice(
        COBOrder.STATUS_CHOICES,
        getter=lambda c: c[0])


class MultiCOBOrderFactory():

    @staticmethod
    def build_test_orders(
        num_of_orders: int,
        traderParams: dict = {},
        institutionParams: dict = {},
        securityParams: dict = {},
        baseParams: dict = {},
        statusParams: dict = {},
        extendedParams: dict = {},
    ) -> Tuple[List[COBOrder], List[OrderGroup]]:

        orders = []
        order_groups = []
        for _ in range(num_of_orders):
            og_data = pdb.create_order_group_data(test=True)
            order_group = OrderGroupFactory.build_entity_with_id(**og_data)

            order = COBOrderFactory.build_entity(
                COBOrderIDFactory.build(),
                TraderIDFactory.build(**traderParams),
                InstitutionIDFactory.build(**institutionParams),
                SecurityIDFactory.build(**securityParams),
                BaseCOBOrderParamsFactory.build(**baseParams),
                COBOrderStatusFactory.build(**statusParams),
                ExtendedCOBOrderParamsFactory.build(**extendedParams),
                order_group
            )

            order_groups.append(order_group)
            orders.append(order)
        return orders, order_groups

    @classmethod
    def create_test_orders(cls,
                           num_of_orders: int,
                           traderParams: dict = {},
                           institutionParams: dict = {},
                           securityParams: dict = {},
                           baseParams: dict = {},
                           statusParams: dict = {},
                           extendedParams: dict = {},
                           ) -> Tuple[List[COBOrder], List[OrderGroup]]:

        orders, order_groups = cls.build_test_orders(
            num_of_orders, traderParams, institutionParams, securityParams,
            baseParams, statusParams, extendedParams)
        for og in order_groups:
            og.save()
        for order in orders:
            order.save()
        return orders, order_groups
