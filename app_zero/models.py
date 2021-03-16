import json
import random
import logging
import traceback
import uuid

from django.db import models
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

from django.contrib.auth.models import AbstractUser

from rest_framework.renderers import JSONRenderer

from lib.data_manipulation.daydiff import daydiff
from lib.django import custom_models


logger = logging.getLogger(__name__)

"""
NOTES ON DEVELOPMENT
* check unique constraints for each model field
* manage test dafault fields -> they are used for creating dummy data easily
* all ForeignKey on_delete are set to models.SET_NULL -> check if this is OK in every case
"""


class Address(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    address = models.CharField(max_length=250, default='Test street 9-9')
    country = models.CharField(max_length=250, default='Test country')
    state = models.CharField(max_length=250, default='Test state')
    municipality = models.CharField(
        max_length=250, default='Test municipality')
    zip_code = models.CharField(max_length=250, default='Test zip code')


class File(custom_models.DatedModel):
    """
    Represents a File
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    location = models.URLField(max_length=500)


class UserSettings(custom_models.DatedModel):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    timezone = models.CharField(max_length=250)
    date_format = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    theme_preferences = models.JSONField()


# class User(custom_models.DatedModel):
#     # username, first_name, last_name, email are inherited from AbstractUser
#     STATUS_ENABLED = 'enabled'
#     STATUS_DISABLED = 'disabled'
#     STATUS_CHOICES = (
#         (STATUS_ENABLED, 'Enabled'),
#         (STATUS_DISABLED, 'Disabled'),
#     )

#     EMAIL_MFA_METHOD = 'email'
#     DUO_MFA_METHOD = 'duo'
#     MFA_METHOD_CHOICES = [
#         (EMAIL_MFA_METHOD, 'Email authentication'),
#         (DUO_MFA_METHOD, 'DUO authentication')
#     ]
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

#     first_name = models.CharField(max_length=250, blank=True, null=True)
#     second_name = models.CharField(max_length=250, blank=True, null=True)
#     last_name = models.CharField(max_length=250, blank=True, null=True)
#     email = models.EmailField()
#     password = models.CharField(max_length=250, blank=True, null=True)
#     image = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
#     telephone = models.CharField(max_length=250, blank=True, null=True)
#     cell_phone = models.CharField(max_length=250, blank=True, null=True)
#     rfc = models.CharField(max_length=250, unique=True)
#     curp = models.CharField(max_length=250, unique=True)
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=250, choices=STATUS_CHOICES)
#     mfa_method = models.CharField(max_length=250, choices=MFA_METHOD_CHOICES)
#     locked = models.BooleanField(default=False)
#     settings = models.ForeignKey(
#         UserSettings, on_delete=models.SET_NULL, null=True)


# class InstitutionManager(custom_models.DatedModel):
#     """
#     Represents an Institution Manager
#     """
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     # ref to User
#     user = models.UUIDField()


class Controller(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to User
    user_id = models.UUIDField()


class ComplianceOfficer(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=250, default='Test first name')
    last_name = models.CharField(max_length=250, default='Test last name')
    telephone = models.CharField(max_length=250, default='Test 555555555')
    email = models.EmailField(max_length=250, default='test@mail.com')


class InstitutionLead(custom_models.DatedModel):
    """
    Represents an Institution Lead
    """
    VERIFIED_WITHOUT_CONTRACT_STATUS = 'verified-without-contract'
    NOT_VERIFIED = 'not-verified'
    VERIFIED = 'verified'
    STATUS_CHOICES = [
        (VERIFIED_WITHOUT_CONTRACT_STATUS, 'Verified Without Contract'),
        (NOT_VERIFIED, 'Not Verified'),
        (VERIFIED, 'Verified')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    contract_id = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, related_name='institution_lead_contract')
    rfc = models.CharField(max_length=250, default='Test RFC')
    logo_id = models.ForeignKey(File, on_delete=models.SET_NULL,
                                null=True, related_name='institution_lead_logo')
    # ref to User
    contact_user_id = models.UUIDField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    compliance_officer = models.ForeignKey(
        ComplianceOfficer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


# class Institution(custom_models.DatedModel):

#     TRADING_LICENSE = 'trading'
#     VIEW_ONLY_LICENSE = 'data'
#     LICENSE_TYPE_CHOICES = [
#         (TRADING_LICENSE, 'Trading Licence'),
#         (VIEW_ONLY_LICENSE, 'Data Licence')
#     ]

#     ENABLED_STATUS = 'enabled'
#     DISABLED_STATUS = 'disabled'
#     STATUS_CHOICES = [
#         (ENABLED_STATUS, 'enabled'),
#         (DISABLED_STATUS, 'disabled')
#     ]

#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     name = models.CharField(max_length=250, unique=True)
#     contract = models.ForeignKey(
#         File, on_delete=models.SET_NULL, null=True, related_name='institution_contract')
#     rfc = models.CharField(max_length=350, unique=True)
#     logo = models.ForeignKey(
#         File, on_delete=models.SET_NULL, null=True, related_name='institution_logo')
#     manager = models.ForeignKey(
#         InstitutionManager, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(
#         max_length=150, choices=STATUS_CHOICES)
#     license_type = ArrayField(models.CharField(
#         max_length=150, choices=LICENSE_TYPE_CHOICES))
#     demo_licenses = models.PositiveIntegerField()
#     trade_licenses = models.PositiveIntegerField()
#     data_licenses = models.PositiveIntegerField()
#     curp = models.CharField(max_length=50, unique=True)
#     compliance_officer = models.ForeignKey(
#         ComplianceOfficer, on_delete=models.SET_NULL, null=True)
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


# class Trader(custom_models.DatedModel):
#     """
#     Represents a Trader
#     """
#     TRADER_LICENSE = 'trader'
#     ANALYST_LICENSE = 'analyst'
#     DEMO_LICENSE = 'demo'
#     LICENSE_CHOICES = [
#         (TRADER_LICENSE, 'Trader License'),
#         (ANALYST_LICENSE, 'Analyst License'),
#         (DEMO_LICENSE, 'Demo License')
#     ]

#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     # ref to User
#     user = models.UUIDField()
#     license_type = ArrayField(models.CharField(
#         max_length=150, choices=LICENSE_CHOICES))
#     institution = models.ForeignKey(
#         Institution, on_delete=models.SET_NULL, null=True)


class ContactPerson(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=250, default='Test first name')
    last_name = models.CharField(max_length=250, default='Test last name')
    telephone = models.CharField(max_length=250, default='Test 555555555')
    email = models.EmailField(max_length=250, default='test@mail.com')


class Lead(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    institution_lead = models.ForeignKey(
        InstitutionLead, on_delete=models.SET_NULL, null=True)
    # ref to Institution
    institution_id = models.UUIDField()
    contact_person = models.ForeignKey(
        ContactPerson, on_delete=models.SET_NULL, null=True)
    comments = models.TextField()


class Concierge(custom_models.DatedModel):
    # must have the same id as the user it refers to
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    leads = models.ManyToManyField(Lead)
    # ref to Institution (list of)
    institution_ids = ArrayField(models.UUIDField())


class Alarm(custom_models.DatedModel):

    YIELD_TYPE = 'yield'
    PRICE_TYPE = 'price'
    SPREAD_TYPE = 'spread'
    TYPE_CHOICES = [
        (YIELD_TYPE, 'Yield'),
        (SPREAD_TYPE, 'Spread'),
        (PRICE_TYPE, 'Price')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    alarm_type = models.CharField(
        max_length=150, choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=40, decimal_places=20)
    # ref to Security
    security_id = models.UUIDField()


class CobOrder(custom_models.DatedModel):

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

    BUY_DIRECTION = 'buy'
    SELL_DIRECTION = 'sell'
    DIRECTION_CHOICES = [
        (BUY_DIRECTION, 'Buy'),
        (SELL_DIRECTION, 'Sell')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Trader
    trader = models.UUIDField()
    # ref to Security
    security = models.UUIDField()
    submission = models.DateTimeField()
    expiration = models.DateTimeField()
    volume = models.IntegerField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    price = models.DecimalField(max_digits=40, decimal_places=20)
    spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    discount_margin = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    yield_value = models.DecimalField(max_digits=40, decimal_places=20)
    direction = models.CharField(
        max_length=150, choices=DIRECTION_CHOICES)

    # TODO: update order_group ref when in same module s OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group = models.UUIDField()


class CobAutoRefresher(custom_models.DatedModel):

    TYPE_FIXED_PRICE = 'fixed-price'
    TYPE_FIXED_SPREAD = 'fixed-spread'
    TYPE_FIXED_ISPRED = 'fixed-ispread'
    TYPE_CHOICES = [
        (TYPE_FIXED_PRICE, 'Fixed Price'),
        (TYPE_FIXED_SPREAD, 'Fixed Spread'),
        (TYPE_FIXED_ISPRED, 'Fixed iSpread')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cob_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL)
    autorefresh_type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    interval = models.PositiveIntegerField()


class CobStream(custom_models.DatedModel):
    STATUS_ACTIVE = 'active'
    STATUS_DEACTIVATED = 'deactivated'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DEACTIVATED, 'Deactivated')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cob_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    # TODO: update order_group ref when in same module as OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group_id = models.UUIDField()


class Rfq(custom_models.DatedModel):

    BUY_DIRECTION = 'buy'
    SELL_DIRECTION = 'sell'
    MARKET_DIRECTION = 'market'
    DIRECTION_CHOICES = (
        (BUY_DIRECTION, 'Buy'),
        (SELL_DIRECTION, 'Sell'),
        (MARKET_DIRECTION, 'Market')
    )

    CANCELLED_STATUS = 'cancelled'
    EXPIRED_STATUS = 'expired'
    ACTIVE_STATUS = 'active'
    STATUS_CHOICES = (
        (CANCELLED_STATUS, 'Cancelled'),
        (EXPIRED_STATUS, 'Expired'),
        (ACTIVE_STATUS, 'Active'),
    )

    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (USD_CURRENCY, 'U.S. Dollar'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Security
    security_id = models.UUIDField()
    # ref to Trader
    trader_id = models.UUIDField()
    anonymous = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    submission = models.DateTimeField()
    expiration = models.DateTimeField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    direction = models.CharField(
        max_length=150, choices=DIRECTION_CHOICES)
    volume = models.IntegerField()
    # ref to Institution (list of)
    counterparty_ids = ArrayField(models.UUIDField())
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    # TODO: update order_group ref when in same module s OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group_id = models.UUIDField()


class RfqResponse(custom_models.DatedModel):

    CANCELLED_STATUS = 'cancelled'
    EXPIRED_STATUS = 'expired'
    ACTIVE_STATUS = 'active'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (CANCELLED_STATUS, 'Cancelled'),
        (EXPIRED_STATUS, 'Expired')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Trader
    trader_id = models.UUIDField()
    submission = models.DateTimeField()
    rfq = models.ForeignKey(
        Rfq, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    ask_price = models.DecimalField(max_digits=40, decimal_places=20)
    ask_yield = models.DecimalField(max_digits=40, decimal_places=20)
    ask_spread = models.DecimalField(max_digits=40, decimal_places=20)
    ask_volume = models.IntegerField()
    ask_discount_margin = models.DecimalField(max_digits=40, decimal_places=20)
    ask_fx = models.DecimalField(max_digits=40, decimal_places=20)
    ask_notional = models.DecimalField(max_digits=40, decimal_places=20)
    bid_price = models.DecimalField(max_digits=40, decimal_places=20)
    bid_yield = models.DecimalField(max_digits=40, decimal_places=20)
    bid_spread = models.DecimalField(max_digits=40, decimal_places=20)
    bid_notional = models.DecimalField(max_digits=40, decimal_places=20)
    bid_discount_margin = models.DecimalField(max_digits=40, decimal_places=20)
    bid_volume = models.IntegerField()
    bid_fx = models.DecimalField(max_digits=40, decimal_places=20)
    autoresponded = models.BooleanField()


class RfqAutoResponder(custom_models.DatedModel):

    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]

    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (USD_CURRENCY, 'U.S. Dollar'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Security
    security_id = models.UUIDField()
    # ref to Trader
    trader_id = models.UUIDField()
    # ref to Institution (list of)
    counterparty_ids = ArrayField(models.UUIDField())
    min_volume = models.PositiveIntegerField()
    max_volume = models.PositiveIntegerField()
    public = models.BooleanField()
    settlement_currency = models.CharField(
        max_length=250, choices=SETTLEMENT_CURRENCY_CHOICES)

    ask_price = models.DecimalField(max_digits=40, decimal_places=20)
    ask_spread = models.DecimalField(max_digits=40, decimal_places=20)
    ask_fx = models.DecimalField(max_digits=40, decimal_places=20)
    ask_notional = models.DecimalField(max_digits=40, decimal_places=20)
    bid_price = models.DecimalField(max_digits=40, decimal_places=20)
    bid_spread = models.DecimalField(max_digits=40, decimal_places=20)
    bid_notional = models.DecimalField(max_digits=40, decimal_places=20)
    bid_fx = models.DecimalField(max_digits=40, decimal_places=20)

    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    priority = models.DateTimeField()

    deactivated_at = models.DateTimeField(null=True, blank=True)


# class RfqLock(custom_models.DatedModel):
#     ACTIVE_STATUS = 'active'
#     DEACTIVATED_STATUS = 'deactivated'
#     STATUS_CHOICES = [
#         (ACTIVE_STATUS, 'Active'),
#         (DEACTIVATED_STATUS, 'Deactivated')
#     ]
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     status = models.CharField(max_length=150, choices=STATUS_CHOICES)
#     # ref to Trader
#     trader_id = models.UUIDField()
#     # ref to Institution
#     institution_id = models.UUIDField()
#     deactivated_at = models.DateTimeField(null=True, blank=True)

# class BaseTransaction(custom_models.DatedModel):
#     """
#     Base class used for CobTransaction and RfqTransaction
#     """
#     CLOSED_STATUS = 'closed'
#     BOOKED_STATUS = 'booked'
#     FAILED_STATUS = 'failed'
#     STATUS_CHOICES = (
#         (CLOSED_STATUS, 'Closed'),
#         (BOOKED_STATUS, 'Booked'),
#         (FAILED_STATUS, 'Failed')
#     )
#     USD_CURRENCY = 'usd'
#     MXN_CURRENCY = 'mxn'
#     SETTLEMENT_CURRENCY_CHOICES = [
#         (USD_CURRENCY, 'U.S. Dollar'),
#         (MXN_CURRENCY, 'Mexican Peso')
#     ]

#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     buyer = models.ForeignKey(
#         Trader, null=True, on_delete=models.SET_NULL, related_name='transaction_buyer')
#     seller = models.ForeignKey(
#         Trader, null=True, on_delete=models.SET_NULL, related_name='transaction_seller')
#     security = models.ForeignKey(
#         Security, null=True, on_delete=models.SET_NULL)
#     volume = models.IntegerField()
#     notional = models.DecimalField(max_digits=40, decimal_places=20)
#     accrued_interest = models.DecimalField(max_digits=40, decimal_places=20)
#     price = models.DecimalField(max_digits=40, decimal_places=20)
#     all_in_price = models.DecimalField(max_digits=40, decimal_places=20)
#     all_in_yield = models.DecimalField(max_digits=40, decimal_places=20)
#     discount_margin = models.DecimalField(
#         max_digits=40, decimal_places=20, null=True, blank=True)
#     yield_value = models.DecimalField(max_digits=40, decimal_places=20)
#     dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
#     status = models.CharField(
#         max_length=150, choices=STATUS_CHOICES)
#     fee_buyer = models.DecimalField(max_digits=40, decimal_places=20)
#     fee_seller = models.DecimalField(max_digits=40, decimal_places=20)
#     vat = models.DecimalField(max_digits=40, decimal_places=20)
#     total_cash = models.DecimalField(max_digits=40, decimal_places=20)
#     settlement_date = models.DateTimeField()
#     settlement_currency = models.CharField(
#         max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
#     fx = models.DecimalField(max_digits=40, decimal_places=20)


class CobTransaction(custom_models.DatedModel):
    CLOSED_STATUS = 'closed'
    BOOKED_STATUS = 'booked'
    FAILED_STATUS = 'failed'
    STATUS_CHOICES = (
        (CLOSED_STATUS, 'Closed'),
        (BOOKED_STATUS, 'Booked'),
        (FAILED_STATUS, 'Failed')
    )
    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (USD_CURRENCY, 'U.S. Dollar'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Trader (buyer)
    buyer = models.UUIDField()
    # ref to Trader (seller)
    seller = models.UUIDField()
    # ref to Security
    security = models.UUIDField()
    volume = models.IntegerField()
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    accrued_interest = models.DecimalField(max_digits=40, decimal_places=20)
    price = models.DecimalField(max_digits=40, decimal_places=20)
    all_in_price = models.DecimalField(max_digits=40, decimal_places=20)
    all_in_yield = models.DecimalField(max_digits=40, decimal_places=20)
    discount_margin = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    yield_value = models.DecimalField(max_digits=40, decimal_places=20)
    dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    fee_buyer = models.DecimalField(max_digits=40, decimal_places=20)
    fee_seller = models.DecimalField(max_digits=40, decimal_places=20)
    vat = models.DecimalField(max_digits=40, decimal_places=20)
    # cash_amount refers to volume * price
    cash_amount = models.DecimalField(max_digits=40, decimal_places=20)
    # total_cash refers to the total amount that will be paid by user (includes fees and vat)
    total_cash = models.DecimalField(max_digits=40, decimal_places=20)
    settlement_date = models.DateTimeField()
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    fx = models.DecimalField(max_digits=40, decimal_places=20)
    sell_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL, related_name='cob_sell_order')
    buy_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL, related_name='cob_buy_order')
    spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)


class RfqTransaction(custom_models.DatedModel):
    CLOSED_STATUS = 'closed'
    BOOKED_STATUS = 'booked'
    FAILED_STATUS = 'failed'
    STATUS_CHOICES = (
        (CLOSED_STATUS, 'Closed'),
        (BOOKED_STATUS, 'Booked'),
        (FAILED_STATUS, 'Failed')
    )
    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (USD_CURRENCY, 'U.S. Dollar'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Trader (buyer)
    buyer_id = models.UUIDField()
    # ref to Trader (seller)
    seller_id = models.UUIDField()
    # ref to Security
    security_id = models.UUIDField()
    volume = models.IntegerField()
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    accrued_interest = models.DecimalField(max_digits=40, decimal_places=20)
    price = models.DecimalField(max_digits=40, decimal_places=20)
    all_in_price = models.DecimalField(max_digits=40, decimal_places=20)
    all_in_yield = models.DecimalField(max_digits=40, decimal_places=20)
    discount_margin = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    yield_value = models.DecimalField(max_digits=40, decimal_places=20)
    dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    fee_buyer = models.DecimalField(max_digits=40, decimal_places=20)
    fee_seller = models.DecimalField(max_digits=40, decimal_places=20)
    vat = models.DecimalField(max_digits=40, decimal_places=20)
    # cash_amount refers to volume * price
    cash_amount = models.DecimalField(max_digits=40, decimal_places=20)
    # total_cash refers to the total amount that will be paid by user (includes fees and vat)
    total_cash = models.DecimalField(max_digits=40, decimal_places=20)
    settlement_date = models.DateTimeField()
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    fx = models.DecimalField(max_digits=40, decimal_places=20)
    rfq = models.ForeignKey(
        Rfq, null=True, on_delete=models.SET_NULL)
    rfq_response = models.ForeignKey(
        RfqResponse, null=True, on_delete=models.SET_NULL)


class Watchlist(custom_models.DatedModel):

    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Trader
    trader_id = models.UUIDField()
    name = models.CharField(max_length=250)
    # ref to Security
    security_ids = ArrayField(models.UUIDField(), null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    description = models.TextField(blank=True, default='')
    archived_at = models.DateTimeField(null=True, blank=True)


class TradeBlockSettlement(custom_models.DatedModel):

    FAILED_STATUS = 'failed'
    SETTLED_STATUS = 'settled'
    STATUS_CHOICES = [
        (FAILED_STATUS, 'Failed'),
        (SETTLED_STATUS, 'Settled')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to SettlementInstruction
    settlement_instruction_id = models.UUIDField()
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)


class TradeBlock(custom_models.DatedModel):
    # NOTE: NOT READY: define trandsactions and transaction_block_settlements
    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    SETTLEMENT_CURRENCY_CHOICES = [
        (USD_CURRENCY, 'U.S. Dollar'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]
    FAILED_STATUS = 'failed'
    PARTIALLY_SETTLED_STATUS = 'partially-settled'
    SETTLED_STATUS = 'settled'
    STATUS_CHOICES = [
        (FAILED_STATUS, 'Failed'),
        (PARTIALLY_SETTLED_STATUS, 'Partially Settled'),
        (SETTLED_STATUS, 'Settled')
    ]
    # transactions =
    # transaction_block_settlements
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to Security
    security_id = models.UUIDField()
    volume = models.IntegerField()
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    fx = models.DecimalField(max_digits=40, decimal_places=20)
    all_in_weighted_avg_price = models.DecimalField(
        max_digits=40, decimal_places=20)
    all_in_weighted_avg_yield = models.DecimalField(
        max_digits=40, decimal_places=20)
    # ref to Institution
    buyer_institution_id = models.UUIDField()
    # ref to Institution
    seller_institution_id = models.UUIDField()
    # ref to Trader (booked_by)
    booked_by_trader_id = models.UUIDField()


class Notification(custom_models.DatedModel):
    TYPE_RFQ_SUBMITTED = 'rfq-submitted'
    TYPE_RFQ_FULFILLED = 'rfq-fulfilled'
    TYPE_RFQ_EXPIRED = 'rfq-expired'
    TYPE_RFQ_ALLOCATED = 'rfq-allocated'
    TYPE_RFQ_CANCELLED = 'rfq-cancelled'
    TYPE_RFQ_RECEIVED = 'rfq-received'

    TYPE_RFQRESPONSE_SENT = 'rfqresponse-sent'
    TYPE_RFQRESPONSE_ALLOCATED = 'rfqresponse-allocated'
    TYPE_RFQRESPONSE_NOT_ALLOCATED = 'rfqresponse-not-allocated'
    TYPE_RFQRESPONSE_RECEIVED = 'rfqresponse-received'
    TYPE_RFQRESPONSE_CANCELLED = 'rfqresponse-cancelled'

    TYPE_AUTORESPONDER_ACTIVATED = 'autoresponder-activated'
    TYPE_AUTORESPONDER_UPDATED = 'autoresponder-updated'
    TYPE_AUTORESPONDER_STOPPED = 'autoresponder-stopped'
    TYPE_AUTORESPONDER_RESPONSE_SENT = 'autoresponder-response-sent'
    TYPE_AUTORESPONDER_RESPONSE_CANCELLED = 'autoresponder-response-cancelled'
    TYPE_AUTORESPONDER_RESPONSE_NOT_ALLOCATED = 'autoresponder-response-not-allocated'

    TYPE_ALARM_ACTIVATED = 'alarm-activated'
    TYPE_ALARM_DISABLED = 'alarm-disabled'
    TYPE_ALARM_TRIGGERED = 'alarm-triggered'
    TYPE_ALARM_UPDATED = 'alarm-updated'

    TYPE_TRADEBLOCK_BOOKED = 'tradeblock-booked'

    TYPE_COBSTREAM_ORDER_UPDATED = 'cobstream-order-updated'
    TYPE_COBSTREAM_ORDER_STOPPED = 'cobstream-order-stopped'

    TYPE_COBORDER_PLACED = 'cob-order-placed'
    TYPE_COBORDER_EXPIRED = 'cob-order-expired'
    TYPE_COBORDER_CANCELLED = 'cob-order-cancelled'
    TYPE_COBORDER_PARTIAL_ALLOCATION = 'cob-order-partial-allocation'
    TYPE_COBORDER_FULL_ALLOCATION = 'cob-order-full-allocation'
    TYPE_COBORDER_OUTSTANDING_MC = 'cob-order-outstanding-mc'
    TYPE_COBORDER_REFRESHED = 'cob-order-refreshed'

    TYPE_TRANSACTION_SETTLEMENT_CONFIRMED = 'transaction-settlement-confirmed'
    TYPE_TRANSACTION_SETTLEMENT_FAILED = 'transaction-settlement-failed'

    TYPE_CHOICES = [
        (TYPE_RFQ_SUBMITTED, ' Rfq Submitted'),
        (TYPE_RFQ_FULFILLED, 'Rfq Fulfilled'),
        (TYPE_RFQ_EXPIRED, 'Rfq Expired'),
        (TYPE_RFQ_ALLOCATED, 'Rfq Allocated'),
        (TYPE_RFQ_CANCELLED, 'Rfq Cancelled'),
        (TYPE_RFQ_RECEIVED, 'Rfq Received'),
        (TYPE_RFQRESPONSE_SENT, 'RfqResponse Sent'),
        (TYPE_RFQRESPONSE_ALLOCATED, 'RfqResponse Allocated'),
        (TYPE_RFQRESPONSE_NOT_ALLOCATED, 'RfqResponse Not Allocated'),
        (TYPE_RFQRESPONSE_RECEIVED, 'RfqResponse Received'),
        (TYPE_RFQRESPONSE_CANCELLED, 'RfqResponse Cancelled'),
        (TYPE_AUTORESPONDER_ACTIVATED, 'AutoResponder Activated'),
        (TYPE_AUTORESPONDER_UPDATED, 'AutoResponder Updated'),
        (TYPE_AUTORESPONDER_STOPPED, 'AutoResponder Stopped'),
        (TYPE_AUTORESPONDER_RESPONSE_SENT, 'AutoResponder Response Sent'),
        (TYPE_AUTORESPONDER_RESPONSE_CANCELLED,
         'AutoResponder Response Cancelled'),
        (TYPE_AUTORESPONDER_RESPONSE_NOT_ALLOCATED,
         ' AutoResponder Response Not Allocated'),
        (TYPE_ALARM_ACTIVATED, 'Alarm Activated'),
        (TYPE_ALARM_DISABLED, 'Alarm Disabled'),
        (TYPE_ALARM_TRIGGERED, 'Alarm Triggered'),
        (TYPE_ALARM_UPDATED, ' Alarm Updated'),
        (TYPE_TRADEBLOCK_BOOKED, 'TradeBlock Booked'),
        (TYPE_COBSTREAM_ORDER_UPDATED, 'CobStream Order Updated'),
        (TYPE_COBSTREAM_ORDER_STOPPED, 'CobStream Order Stopped'),
        (TYPE_COBORDER_PLACED, 'CobOrder Placed'),
        (TYPE_COBORDER_EXPIRED, 'CobOrder Expired'),
        (TYPE_COBORDER_CANCELLED, 'CobOrder Cancelled'),
        (TYPE_COBORDER_PARTIAL_ALLOCATION, 'CobOrder Partial Allocation'),
        (TYPE_COBORDER_FULL_ALLOCATION, 'CobOrder Full Allocation'),
        (TYPE_COBORDER_OUTSTANDING_MC, 'CobOrder Outstanding Market Close'),
        (TYPE_COBORDER_REFRESHED, 'CobOrder Refreshed'),
        (TYPE_TRANSACTION_SETTLEMENT_CONFIRMED,
         'Transaction Settlement Confirmed'),
        (TYPE_TRANSACTION_SETTLEMENT_FAILED, 'Transaction Settlement Failed'),
    ]

    STATUS_READ = 'read'
    STATUS_UNREAD = 'unread'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_READ, 'Read'),
        (STATUS_UNREAD, 'Unread'),
        (STATUS_ARCHIVED, 'Archived')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    notification_type = models.CharField(max_length=250, choices=TYPE_CHOICES)
    body = models.JSONField(encoder=DjangoJSONEncoder)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES)
    # ref to User
    user_id = models.UUIDField()


class NotificationSettings(custom_models.DatedModel):

    NOTIFY_AS_EMAIL = 'email'
    NOTIFY_AS_INBOX = 'inbox'
    NOTIFY_AS_TOAST = 'toast'
    NOTIFY_AS_ALARM = 'alarm'
    NOTIFY_AS_CHOICES = [
        (NOTIFY_AS_EMAIL, 'Notify as email'),
        (NOTIFY_AS_ALARM, 'Notify as alarm'),
        (NOTIFY_AS_TOAST, 'Notify as toast'),
        (NOTIFY_AS_INBOX, 'Notify as inbox'),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # ref to User
    user_id = models.UUIDField()
    notification_type = models.CharField(
        max_length=250, choices=Notification.TYPE_CHOICES)
    notify_as = ArrayField(models.CharField(
        max_length=250, choices=NOTIFY_AS_CHOICES))


model_list = [
    Address,
    File,
    UserSettings,
    # InstitutionManager,
    Controller,
    ComplianceOfficer,
    InstitutionLead,
    # Institution,
    ContactPerson,
    Lead,
    Concierge,
    # SettlementInstruction,
    Alarm,
    CobOrder,
    CobAutoRefresher,
    CobStream,
    Rfq,
    RfqResponse,
    RfqAutoResponder,
    # RfqLock,
    CobTransaction,
    RfqTransaction,
    Watchlist,
    # TradeBlock,
    TradeBlockSettlement,
    Notification,
    NotificationSettings
]
