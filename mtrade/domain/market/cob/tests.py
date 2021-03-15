from datetime import datetime, timedelta
import factory
import pytz
from decimal import Decimal

from django.db.models.manager import Manager
from django.test import TestCase

from lib.ddd.exceptions import VOValidationExcpetion
from mtrade.domain.market.order_group.models import OrderGroupFactory
from scripts.db_content_manager import populate_db as pdb
from lib.data_manipulation.date_generators import date_linear_generator
from lib.data_manipulation.number_generators import num_linear_generator

from . import test_helper as th
from .models import COBOrder, COBOrderFactory, COBOrderStatus
from .services import COBServices


class COBOrderTests(TestCase):

    def test_build_cob_order_id(self):
        try:
            th.COBOrderIDFactory.build()
        except Exception:
            self.fail("Unexpected exception")

    def test_build_trader_id(self):
        try:
            th.TraderIDFactory.build()
        except Exception:
            self.fail("Unexpected exception")

    def test_build_security_id(self):
        try:
            th.SecurityIDFactory.build()
        except Exception:
            self.fail("Unexpected exception")

    def test_build_base_cob_order_params(self):
        base_priority = datetime(2021, 3, 15)
        base_expiration = datetime(2021, 3, 16)

        # Tests success on bid
        try:
            th.BaseCOBOrderParamsFactory.build(
                direction=COBOrder.DIRECTION_BID
            )
        except Exception:
            self.fail("Unexpected exception")

        # Tests success on ask
        try:
            th.BaseCOBOrderParamsFactory.build(
                direction=COBOrder.DIRECTION_ASK
            )
        except Exception:
            self.fail("Unexpected exception")

        # Tests failure when priority equals expiration
        with self.assertRaises(VOValidationExcpetion):
            th.BaseCOBOrderParamsFactory.build(
                priority=base_priority,
                expiration=base_priority,
            )

        # Tests failure when priority is greater than expiration
        with self.assertRaises(VOValidationExcpetion):
            th.BaseCOBOrderParamsFactory.build(
                priority=base_expiration + timedelta(seconds=1),
                expiration=base_expiration,
            )

        # Tests failure when price is negative
        with self.assertRaises(VOValidationExcpetion):
            th.BaseCOBOrderParamsFactory.build(
                price=Decimal("-100.25"),
            )

        # Tests failure when size is negative
        with self.assertRaises(VOValidationExcpetion):
            th.BaseCOBOrderParamsFactory.build(
                size=-100
            )

        # Tests failure when direction is invalid
        with self.assertRaises(VOValidationExcpetion):
            th.BaseCOBOrderParamsFactory.build(
                direction='north'
            )

    def test_build_cob_order_status(self):
        valid_statuses = [x[0] for x in COBOrder.STATUS_CHOICES]

        for status in valid_statuses:
            try:
                COBOrderStatus(
                    value=status
                )
            except Exception:
                self.fail("Unexpected exception")

        # Tests failure when status is invalid
        with self.assertRaises(VOValidationExcpetion):
            COBOrderStatus(
                value='unexpectedstatus'
            )

    def test_build_extended_cob_order_params(self):
        try:
            th.ExtendedCOBOrderParamsFactory.build()
        except Exception:
            self.fail("Unexpected exception")

    def test_build_cob_order(self):
        og_data = pdb.create_order_group_data(test=True)
        order_group = OrderGroupFactory.build_entity_with_id(**og_data)

        try:
            COBOrderFactory.build_entity_with_id(
                trader_id=th.TraderIDFactory.build(),
                security_id=th.SecurityIDFactory.build(),
                base_params=th.BaseCOBOrderParamsFactory.build(),
                status=th.COBOrderStatusFactory.build(),
                extended_params=th.ExtendedCOBOrderParamsFactory.build(),
                order_group=order_group
            )
        except Exception:
            self.fail("Unexpected exception")


class COBServicesTests(TestCase):

    def test_cob_order_repo(self):
        repo = COBServices.get_cob_order_repo()
        self.assertEqual(Manager, type(repo))

    def test_get_market_factory(self):
        factory = COBServices.get_cob_order_factory()
        self.assertEqual(COBOrderFactory, factory)

    def test_get_queued_orders(self):
        dategen = date_linear_generator(
                datetime(2020, 3, 15, tzinfo=pytz.UTC),
                timedelta(microseconds=1))

        th.MultiCOBOrderFactory.create_test_orders(
            2,
            statusParams={"value":COBOrder.STATUS_NEW},
            baseParams={"priority": factory.LazyFunction(lambda: next(dategen))}
            )

        th.MultiCOBOrderFactory.create_test_orders(
            3,
            statusParams={"value":COBOrder.STATUS_QUEUED},
            baseParams={"priority": factory.LazyFunction(lambda: next(dategen))}
            )


        queued_orders = COBServices.get_queued_orders()
        num_of_orders = len(queued_orders)

        # Tests the correct number of queued orders is received
        self.assertEqual(num_of_orders , 3)

        # Tests only orders with status=queued are received
        for order in queued_orders:
            self.assertEqual(order.status, COBOrder.STATUS_QUEUED)

        # Tests queued elements are received in descending priority order
        for i in range(1, num_of_orders):
            self.assertTrue(queued_orders[i].priority > queued_orders[i-1].priority)

    def test_get_queued_orders_2(self):
        numgen = num_linear_generator(100,10)

        th.MultiCOBOrderFactory.create_test_orders(
            3,
            statusParams={"value":COBOrder.STATUS_QUEUED},
            baseParams={"size": factory.LazyFunction(lambda: next(numgen))}
            )

        # Tests queued elements with same date are received in descending size order
        queued_orders = COBServices.get_queued_orders()
        num_of_orders = len(queued_orders)
        for i in range(1, num_of_orders):
            self.assertTrue(queued_orders[i].size < queued_orders[i-1].size)

    def test_get_queued_orders_3(self):
        th.MultiCOBOrderFactory.create_test_orders(
            3,
            statusParams={"value":COBOrder.STATUS_QUEUED},
            baseParams={"size": 100}
            )

        # Tests queued elements with same date and size are received in ascending id order
        queued_orders = COBServices.get_queued_orders()
        num_of_orders = len(queued_orders)
        for i in range(1, num_of_orders):
            self.assertTrue(queued_orders[i].id > queued_orders[i-1].id)
