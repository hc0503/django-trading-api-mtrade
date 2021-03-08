# python imports
import uuid
from dataclasses import dataclass

# django imports
from django.db import models

# app imports
from lib.django import custom_models
from lib.ddd.exceptions import VOValidationExcpetion

# local imports


@dataclass(frozen=True)
class OrderGroupID():
    """
    This is a value object that should be used to generate and pass the OrderGroupID to the OrderGroupFactory
    """
    value: uuid.UUID


class OrderGroup(custom_models.DatedModel):
    """
    Represents an overview of all trades related to a Cob origin order or an Rfq
    """
    # order history
    ORDERBOOK_COB = 'cob'
    ORDERBOOK_RFQ = 'rfq'
    ORDERBOOK_CHOICES = [
        (ORDERBOOK_COB, 'COB'),
        (ORDERBOOK_RFQ, 'RFQ')
    ]
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
    RESPONDED_BY_AUTORESPONDER = 'autoresponder'
    RESPONDED_BY_MANUAL = 'manual'
    RESPONDED_BY_NA = 'na'  # for cases where this category is not applicable
    RESPONDED_BY_CHOICES = [
        (RESPONDED_BY_AUTORESPONDER, 'Autoresponder'),
        (RESPONDED_BY_MANUAL, 'Manual'),
        (RESPONDED_BY_NA, 'N. A.')
    ]

    CURRENCY_USD = 'usd'
    CURRENCY_MXN = 'mxn'
    CURRENCY_CHOICES = [
        (CURRENCY_USD, 'US Dollars'),
        (CURRENCY_MXN, 'Mexican Peso')
    ]

    REQUESTOR_TYPE_ANONYMOUS = 'anonymous'
    REQUESTOR_TYPE_NOT_ANONYMOUS = 'not-anonymous'
    REQUESTOR_TYPE_CHOICES = [
        (REQUESTOR_TYPE_ANONYMOUS, 'Anonymous'),
        (REQUESTOR_TYPE_NOT_ANONYMOUS, 'Not Anonymous')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    orderbook = models.CharField(max_length=150, choices=ORDERBOOK_CHOICES)
    order_type = models.CharField(max_length=150, choices=ORDER_TYPE_CHOICES)
    direction = models.CharField(max_length=150, choices=DIRECTION_CHOICES)
    volume = models.PositiveIntegerField()
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    weighted_avg_price = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    weighted_avg_yield = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    weighted_avg_spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True)
    fx = models.DecimalField(max_digits=40, decimal_places=20)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    submission = models.DateTimeField()
    expiration = models.DateTimeField()
    responded_by = models.CharField(
        max_length=150, choices=RESPONDED_BY_CHOICES)
    settlement_currency = models.CharField(
        max_length=150, choices=CURRENCY_CHOICES)
    # NOTE: queries must take into account that, if requestor_typ is anonymous, counterparties must not know who requestor is
    requestor_type = models.CharField(
        max_length=150, choices=REQUESTOR_TYPE_CHOICES)

    resp_received = models.PositiveIntegerField()
    # TODO: when possible, make sure requestor makes reference to an Institution
    # requestor = models.ForeignKey(
    #     Institution, on_delete=models.SET_NULL, null=True)
    requestor = models.UUIDField()
    # TODO: when possible make sure trader makes reference to Trader
    # trader = models.ForeignKey(Trader, on_delete=models.SET_NULL, null=True)
    trader = models.UUIDField()
    # TODO: when possible, make sure security makes reference to Security
    # security = models.ForeignKey(
    #     Security, on_delete=models.SET_NULL, null=True)
    security = models.UUIDField()

    def update_entity(self):
        # TODO: implement this method (check MArket example)
        pass

    class Meta:
        ordering = ['id']


class OrderGroupFactory():
    @staticmethod
    # TODO: implement restrictions for entity building (check MArket Example)
    def build_entity(**kwargs) -> OrderGroup:
        return OrderGroup(**kwargs)
