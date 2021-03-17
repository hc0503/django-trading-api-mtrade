# python imports
import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from django.db import models

from lib.django import custom_models
from lib.ddd.exceptions import VOValidationExcpetion


@dataclass(frozen=True)
class OrderGroupID():
    """
    This is a value object that should be used to generate and pass the OrderGroupID to the OrderGroupFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class SecurityID():
    """
    This is a value object that should be used to generate and pass the SecurityID to the OrderGroupFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class RequestorInstitutionID():
    """
    This is a value object that should be used to generate and pass the RequestorInstitutionID (Institution) to the OrderGroupFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class TraderID():
    """
    This is a value object that should be used to generate and pass the TraderID to the OrderGroupFactory
    """
    value: uuid.UUID


@dataclass(frozen=True)
class OrderGroupBaseParams():
    orderbook_type: str
    order_type: str
    direction: str
    size: int
    notional: Decimal
    submission: datetime
    expiration: datetime
    response_type: str
    settlement_currency: str
    requestor_type: str

    def __post_init__(self):
        self.validate_dates()
        self.validate_orderbook_type()
        self.validate_order_type()
        self.validate_direction()
        self.validate_size()
        self.validate_notional()
        self.validate_response_type()
        self.validate_settlement_currency()
        self.validate_requestor_type()

    def validate_dates(self):
        if self.submission >= self.expiration:
            raise VOValidationExcpetion(
                "BaseOrderGroupParams",
                "OrderGroup should have an expiration date that is greater than its submission date. Received - submission: {}, expiration:{}".format(
                    self.submission,
                    self.expiration))

    def validate_orderbook_type(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.orderbook_type,
                OrderGroup.ORDERBOOK_TYPE_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid orderbook type. Received - orderbook_type: {}".format(self.orderbook_type))

    def validate_order_type(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.order_type,
                OrderGroup.ORDER_TYPE_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid order type. Received - order_type: {}".format(self.order_type))

    def validate_direction(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.direction,
                OrderGroup.DIRECTION_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid direction. Received - direction: {}".format(self.direction))

    def validate_size(self):
        if self.size < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Size must be positive. Received - size: {}".format(self.size))

    def validate_notional(self):
        if self.notional < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Notional must be positive. Received - notional: {}".format(self.notional))

    def validate_response_type(self):
        if self.orderbook_type == OrderGroup.ORDERBOOK_TYPE_RFQ:
            valid_choice = next(
                filter(
                    lambda x: x[0] == self.response_type,
                    OrderGroup.RESPONSE_TYPE_CHOICES),
                None)
            if not valid_choice:
                raise VOValidationExcpetion(
                    "OrderGroupParams", "Invalid response type. Received - response_type: {}".format(self.direction))

    def validate_settlement_currency(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.settlement_currency,
                OrderGroup.SETTLEMENT_CURRENCY_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid settlement currency. Received - settlement_currency: {}".format(self.settlement_currency))

    def validate_requestor_type(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.requestor_type,
                OrderGroup.REQUESTOR_TYPE_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid requestor type. Received - requestor_type: {}".format(self.requestor_type))


@dataclass(frozen=True)
class Priority():
    value: datetime


@dataclass(frozen=True)
class ResponsesReceived():
    value: int

    def __post_init__(self):
        self.validate_resp_received()

    def validate_resp_received(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Received responses must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class AllocationPercentage():
    value: Decimal

    def __post_init__(self):
        self.validate_allocation_percentage()

    def validate_allocation_percentage(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Allocation percentage must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class OrderGroupStatus():
    value: str

    def __post_init__(self):
        self.validate_status_value()

    def validate_status_value(self):
        valid_choice = next(
            filter(
                lambda x: x[0] == self.value,
                OrderGroup.STATUS_CHOICES),
            None)
        if not valid_choice:
            raise VOValidationExcpetion(
                "OrderGroupParams", "Invalid status. Received - status: {}".format(self.value))


@dataclass(frozen=True)
class WeightedAveragePrice():
    value:  Decimal

    def __post_init__(self):
        self.validate_weighted_avg_price_value()

    def validate_weighted_avg_price_value(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Weighted average price must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class WeightedAverageYield():
    value:  Decimal

    def __post_init__(self):
        self.validate_weighted_avg_yield_value()

    def validate_weighted_avg_yield_value(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Weighted average yield must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class WeightedAverageSpread():
    value:  Decimal

    def __post_init__(self):
        self.validate_weighted_avg_spread_value()

    def validate_weighted_avg_spread_value(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Weighted average spread must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class FX():
    value:  Decimal

    def __post_init__(self):
        self.validate_fx_value()

    def validate_fx_value(self):
        if self.value < 0:
            raise VOValidationExcpetion(
                "BaseCobOrderParams", "Foreign Currency exchange rate must be positive. Received - value: {}".format(self.value))


@dataclass(frozen=True)
class OrderGroupExtendedParams():
    weighted_avg_price: WeightedAveragePrice
    weighted_avg_spread: WeightedAverageSpread
    weighted_avg_yield: WeightedAverageYield
    fx: FX


class OrderGroup(custom_models.DatedModel):
    """
    Represents an overview of all trades related to a Cob origin order or an Rfq
    """

    class Meta:
        ordering = ['id']

    ORDERBOOK_TYPE_COB = 'cob'
    ORDERBOOK_TYPE_RFQ = 'rfq'
    ORDERBOOK_TYPE_CHOICES = [
        (ORDERBOOK_TYPE_COB, 'COB'),
        (ORDERBOOK_TYPE_RFQ, 'RFQ')
    ]
    # TODO: order types are the union of Rfq and Cob order types
    ORDER_TYPE_STREAM = 'stream'
    ORDER_TYPE_CHOICES = [
        (ORDER_TYPE_STREAM, 'Stream')
    ]

    DIRECTION_BUY = 'buy'
    DIRECTION_SELL = 'sell'
    DIRECTION_MARKET = 'market'
    DIRECTION_CHOICES = [
        (DIRECTION_BUY, 'Buy'),
        (DIRECTION_SELL, 'Sell'),
        (DIRECTION_MARKET, 'Market')
    ]

    ACTIVE_STATUS = 'active'
    CANCELLED_STATUS = 'cancelled'
    EXPIRED_STATUS = 'expired'
    PENDING_STATUS = 'pending'
    FULL_ALLOCATION_STATUS = 'full-allocation'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (CANCELLED_STATUS, 'Cancelled'),
        (EXPIRED_STATUS, 'Expired'),
        (PENDING_STATUS, 'Pending'),
        (FULL_ALLOCATION_STATUS, 'Full Allocation')
    ]
    RESPONSE_TYPE_AUTORESPONDER = 'autoresponder'
    RESPONSE_TYPE_MANUAL = 'manual'

    RESPONSE_TYPE_CHOICES = [
        (RESPONSE_TYPE_AUTORESPONDER, 'Autoresponder'),
        (RESPONSE_TYPE_MANUAL, 'Manual'),

    ]

    SETTLEMENT_CURRENCY_USD = 'usd'
    SETTLEMENT_CURRENCY_MXN = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (SETTLEMENT_CURRENCY_USD, 'US Dollars'),
        (SETTLEMENT_CURRENCY_MXN, 'Mexican Peso')
    ]

    REQUESTOR_TYPE_ANONYMOUS = 'anonymous'
    REQUESTOR_TYPE_NOT_ANONYMOUS = 'not-anonymous'
    REQUESTOR_TYPE_CHOICES = [
        (REQUESTOR_TYPE_ANONYMOUS, 'Anonymous'),
        (REQUESTOR_TYPE_NOT_ANONYMOUS, 'Not Anonymous')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Security
    security_id = models.UUIDField()
    orderbook_type = models.CharField(
        max_length=150, choices=ORDERBOOK_TYPE_CHOICES)
    order_type = models.CharField(
        max_length=150, choices=ORDER_TYPE_CHOICES)
    direction = models.CharField(max_length=150, choices=DIRECTION_CHOICES)
    size = models.PositiveIntegerField()
    notional = models.DecimalField(
        max_digits=40, decimal_places=20)

    weighted_avg_price = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    weighted_avg_yield = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    weighted_avg_spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    fx = models.DecimalField(max_digits=40, decimal_places=20, null=True)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    allocation_pct = models.DecimalField(max_digits=40, decimal_places=20)
    submission = models.DateTimeField()
    priority = models.DateTimeField()
    expiration = models.DateTimeField()
    response_type = models.CharField(
        max_length=150, choices=RESPONSE_TYPE_CHOICES)
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    # NOTE: queries must take into account that, if requestor_typ is anonymous, counterparties must not know who requestor is
    requestor_type = models.CharField(
        max_length=150, choices=REQUESTOR_TYPE_CHOICES)
    resp_received = models.PositiveIntegerField()
    # ref to Institution
    requestor_institution_id = models.UUIDField()
    # ref to Trader
    trader_id = models.UUIDField()

    def update_entity(self,
                      weighted_avg_price: WeightedAveragePrice = None,
                      weighted_avg_yield: WeightedAverageYield = None,
                      weighted_avg_spread: WeightedAverageSpread = None,
                      fx: FX = None,
                      status: OrderGroupStatus = None,
                      allocation_pct: AllocationPercentage = None,
                      resp_received: ResponsesReceived = None,
                      priority: Priority = None, **kwargs):
        """Updates and entity. Only fields in arguments may be updated"""
        if weighted_avg_price is not None:
            self.weighted_avg_price = weighted_avg_price.value
        if weighted_avg_yield is not None:
            self.weighted_avg_yield = weighted_avg_yield.value
        if weighted_avg_spread is not None:
            self.weighted_avg_spread = weighted_avg_spread.value
        if fx is not None:
            self.fx = fx.value
        if status is not None:
            self.status = status.value
        if allocation_pct is not None:
            self.allocation_pct = allocation_pct.value
        if resp_received is not None:
            self.resp_received = resp_received.value
        if priority is not None:
            self.priority = priority.value


class OrderGroupFactory():
    @staticmethod
    def build_entity(order_group_id: OrderGroupID,
                     security_id: SecurityID,
                     requestor_institution_id: RequestorInstitutionID,
                     trader_id: TraderID,
                     priority: Priority,
                     resp_received: ResponsesReceived,
                     allocation_pct: AllocationPercentage,
                     status: OrderGroupStatus,
                     base_params: OrderGroupBaseParams,
                     extended_params: OrderGroupExtendedParams) -> OrderGroup:
        order_group = OrderGroup(
            id=order_group_id.value,
            security_id=security_id.value,
            requestor_institution_id=requestor_institution_id.value,
            trader_id=trader_id.value,
            orderbook_type=base_params.orderbook_type,
            direction=base_params.direction,
            size=base_params.size,
            notional=base_params.notional,
            weighted_avg_price=extended_params.weighted_avg_price.value,
            weighted_avg_yield=extended_params.weighted_avg_yield.value,
            weighted_avg_spread=extended_params.weighted_avg_spread.value,
            fx=extended_params.fx.value,
            status=status,
            allocation_pct=allocation_pct.value,
            submission=base_params.submission,
            priority=priority.value,
            expiration=base_params.expiration,
            response_type=base_params.response_type,
            settlement_currency=base_params.settlement_currency,
            requestor_type=base_params.requestor_type,
            resp_received=resp_received.value,
        )
        # order_group.full_clean()
        return order_group

    @classmethod
    def build_entity_with_id(cls,
                             security_id: SecurityID,
                             requestor_institution_id: RequestorInstitutionID,
                             trader_id: TraderID,
                             priority: Priority,
                             resp_received: ResponsesReceived,
                             allocation_pct: AllocationPercentage,
                             status: OrderGroupStatus,
                             base_params: OrderGroupBaseParams,
                             extended_params: OrderGroupExtendedParams) -> OrderGroup:
        order_group_id = OrderGroupID(uuid.uuid4())

        return cls.build_entity(order_group_id=order_group_id,
                                security_id=security_id,
                                requestor_institution_id=requestor_institution_id,
                                trader_id=trader_id,
                                priority=priority,
                                resp_received=resp_received,
                                allocation_pct=allocation_pct,
                                status=status,
                                base_params=base_params,
                                extended_params=extended_params
                                )
