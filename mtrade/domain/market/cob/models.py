from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid

from django.db import models

from lib.ddd.exceptions import VOValidationExcpetion
from lib.django import custom_models
from mtrade.domain.market.order_group.models import OrderGroup
from mtrade.domain.market.exceptions import InvalidMarketOperationException


@dataclass(frozen=True)
class COBOrderID():
    """
    A value object used to generate and pass the COBOrderID to the
    COBOrderFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class TraderID():
    """
    A value object used to generate and pass the TraderID to the
    COBOrderFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class SecurityID():
    """
    A value object used to generate and pass the SecurityID to the
    COBOrderFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class BaseCOBOrderParams():
    priority: datetime
    expiration: datetime
    price: Decimal
    size: int
    direction: str

    def __post_init__(self):
        self.validate_dates()
        self.validate_price()
        self.validate_size()
        self.validate_direction()

    def validate_dates(self):
        if self.priority >= self.expiration:
            raise VOValidationExcpetion(
                "BaseCobOrderParams",
                "Order should have an expiration date that is greater than its priority date. Received - priority: {}, expiration:{}".format(
                    self.priority,
                    self.expiration))

    def validate_price(self):
        if self.price < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Price must be positive. Received - price: {}".format(self.price))

    def validate_size(self):
        if self.size < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Size must be positive. Received - size: {}".format(self.size))

    def validate_direction(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.direction,
                COBOrder.DIRECTION_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Invalid direction. Received - direction: {}".format(self.direction))


@dataclass(frozen=True)
class COBOrderStatus():
    value: str

    def __post_init__(self):
        self.validate_status_value()

    def validate_status_value(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.value,
                COBOrder.STATUS_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "COBOrderStatus", "Invalid status. Received - status: {}".format(self.value))


@dataclass(frozen=True)
class ExtendeCOBOrderParams():
    dirty_price: Decimal
    notional: Decimal
    spread: Decimal
    discount_margin: Decimal
    yield_value: Decimal
    # TODO: Add class validators


class COBOrder(custom_models.DatedModel):

    STATUS_NEW = 'new'
    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUS_QUEUED = 'queued'
    STATUS_REPLACED = 'replaced'
    STATUS_FULLY_ALLOCATED = 'fully-allocated'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_QUEUED, 'Queued'),
        (STATUS_REPLACED, 'Replaced'),
        (STATUS_FULLY_ALLOCATED, 'Fully Allocated')
    ]

    STATUS_TRANSITIONS = {}
    STATUS_TRANSITIONS[STATUS_NEW] = (
        STATUS_QUEUED,
        STATUS_ACTIVE,
        STATUS_REPLACED,
        STATUS_FULLY_ALLOCATED
    )

    STATUS_TRANSITIONS[STATUS_ACTIVE] = (
        STATUS_CANCELLED,
        STATUS_EXPIRED,
        STATUS_REPLACED,
        STATUS_FULLY_ALLOCATED
    )

    STATUS_TRANSITIONS[STATUS_QUEUED] = (
        STATUS_ACTIVE,
        STATUS_REPLACED,
        STATUS_FULLY_ALLOCATED
    )

    STATUS_TRANSITIONS[STATUS_CANCELLED] = ()
    STATUS_TRANSITIONS[STATUS_EXPIRED] = ()
    STATUS_TRANSITIONS[STATUS_REPLACED] = ()
    STATUS_TRANSITIONS[STATUS_FULLY_ALLOCATED] = ()

    # TODO: Redundancy check: the sum of active, cancelled, and fully-allocated
    # orders at any point in time should be equal to the value of the original
    # order in the group

    DIRECTION_BID = 'bid'
    DIRECTION_ASK = 'ask'
    DIRECTION_CHOICES = [
        (DIRECTION_BID, 'Bid'),
        (DIRECTION_ASK, 'Ask')
    ]

    # TODO: Evaluate if institution field should be added here, this would
    # speed up queries
    id = models.UUIDField(primary_key=True, editable=False)
    trader_id = models.UUIDField()
    security_id = models.UUIDField()

    # NOTE: priority is preserved when a CobOrder's  size is increased.
    # Increasing an order means replacing an order with one with a higher
    # value
    priority = models.DateTimeField()
    expiration = models.DateTimeField()
    price = models.DecimalField(max_digits=40, decimal_places=20)
    size = models.IntegerField()
    direction = models.CharField(
        max_length=150, choices=DIRECTION_CHOICES)

    status = models.CharField(max_length=150, choices=STATUS_CHOICES)

    dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    discount_margin = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    yield_value = models.DecimalField(max_digits=40, decimal_places=20)

    order_group = models.ForeignKey(
        OrderGroup, on_delete=models.PROTECT, null=False)

    def update_entity(
            self,
            status: COBOrderStatus):
        """
        Updates a COBOrder. Only status updates are allowed. Any other
        operation should be performed through an order replacement.
        """
        if status is None:
            raise InvalidMarketOperationException(
                "update_entity", "status cannot be None")

        # Verifies transition is valid
        if status.value not in self.STATUS_TRANSITIONS[self.status]:
            raise InvalidMarketOperationException(
                "update_entity",
                "Invalid transition. Current status: {}, received status: {}".format(
                    self.status,
                    status.value))

        self.status = status.value


class COBOrderFactory():
    @staticmethod
    def build_entity(
            order_id: COBOrderID,
            trader_id: TraderID,
            security_id: SecurityID,
            base_params: BaseCOBOrderParams,
            status: COBOrderStatus,
            extended_params: ExtendeCOBOrderParams,
            order_group: OrderGroup):

        return COBOrder(
            id=order_id.value,
            trader_id=trader_id.value,
            security_id=security_id.value,
            priority=base_params.priority,
            expiration=base_params.expiration,
            price=base_params.price,
            size=base_params.size,
            direction=base_params.direction,
            status=status.value,
            dirty_price=extended_params.dirty_price,
            notional=extended_params.notional,
            spread=extended_params.spread,
            discount_margin=extended_params.discount_margin,
            yield_value=extended_params.yield_value,
            order_group=order_group
        )

    @classmethod
    def build_entity_with_id(
            cls,
            trader_id: TraderID,
            security_id: SecurityID,
            base_params: BaseCOBOrderParams,
            status: COBOrderStatus,
            extended_params: ExtendeCOBOrderParams,
            order_group: OrderGroup):

        order_id = COBOrderID(uuid.uuid4())
        return cls.build_entity(
            order_id,
            trader_id,
            security_id,
            base_params,
            status,
            extended_params,
            order_group)
