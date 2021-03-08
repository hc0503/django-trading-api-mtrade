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


logger = logging.getLogger(__name__)

"""
NOTES ON DEVELOPMENT
* created_at fields in each model should be auto_add_now=True, editable=False. Check every case, since this is not yet completely implemented (for data generation purposes)
* check unique constraints for each model field
* manage test dafault fields -> they are used for creating dummy data easily
* all ForeignKey on_delete are set to models.SET_NULL -> check if this is OK in every case
"""


class Address(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    address = models.CharField(max_length=250, default='Test street 9-9')
    country = models.CharField(max_length=250, default='Test country')
    state = models.CharField(max_length=250, default='Test state')
    municipality = models.CharField(
        max_length=250, default='Test municipality')
    zip_code = models.CharField(max_length=250, default='Test zip code')
    created_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    """
    Represents a File
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    location = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class UserSettings(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    timezone = models.CharField(max_length=250)
    date_format = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    theme_preferences = models.JSONField()


class User(models.Model):
    # username, first_name, last_name, email are inherited from AbstractUser
    STATUS_ENABLED = 'enabled'
    STATUS_DISABLED = 'disabled'
    STATUS_CHOICES = (
        (STATUS_ENABLED, 'Enabled'),
        (STATUS_DISABLED, 'Disabled'),
    )

    EMAIL_MFA_METHOD = 'email'
    DUO_MFA_METHOD = 'duo'
    MFA_METHOD_CHOICES = [
        (EMAIL_MFA_METHOD, 'Email authentication'),
        (DUO_MFA_METHOD, 'DUO authentication')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    first_name = models.CharField(max_length=250, blank=True, null=True)
    second_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=250, blank=True, null=True)
    image = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    telephone = models.CharField(max_length=250, blank=True, null=True)
    cell_phone = models.CharField(max_length=250, blank=True, null=True)
    rfc = models.CharField(max_length=250, unique=True)
    curp = models.CharField(max_length=250, unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES)
    mfa_method = models.CharField(max_length=250, choices=MFA_METHOD_CHOICES)
    locked = models.BooleanField(default=False)
    settings = models.ForeignKey(
        UserSettings, on_delete=models.SET_NULL, null=True)


class InstitutionManager(models.Model):
    """
    Represents an Institution Manager
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Controller(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class ComplianceOfficer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=250, default='Test first name')
    last_name = models.CharField(max_length=250, default='Test last name')
    telephone = models.CharField(max_length=250, default='Test 555555555')
    email = models.EmailField(max_length=250, default='test@mail.com')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class InstitutionLead(models.Model):
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
    contract = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, related_name='institution_lead_contract')
    rfc = models.CharField(max_length=250, default='Test RFC')
    logo = models.ForeignKey(File, on_delete=models.SET_NULL,
                             null=True, related_name='institution_lead_logo')
    contact_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    compliance_officer = models.ForeignKey(
        ComplianceOfficer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Institution(models.Model):

    TRADING_LICENSE = 'trading'
    VIEW_ONLY_LICENSE = 'data'
    LICENSE_TYPE_CHOICES = [
        (TRADING_LICENSE, 'Trading Licence'),
        (VIEW_ONLY_LICENSE, 'Data Licence')
    ]

    ENABLED_STATUS = 'enabled'
    DISABLED_STATUS = 'disabled'
    STATUS_CHOICES = [
        (ENABLED_STATUS, 'enabled'),
        (DISABLED_STATUS, 'disabled')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250, unique=True)
    contract = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, related_name='institution_contract')
    rfc = models.CharField(max_length=350, unique=True)
    logo = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, related_name='institution_logo')
    manager = models.ForeignKey(
        InstitutionManager, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    license_type = ArrayField(models.CharField(
        max_length=150, choices=LICENSE_TYPE_CHOICES))
    demo_licenses = models.PositiveIntegerField()
    trade_licenses = models.PositiveIntegerField()
    data_licenses = models.PositiveIntegerField()
    curp = models.CharField(max_length=50, unique=True)
    compliance_officer = models.ForeignKey(
        ComplianceOfficer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Trader(models.Model):
    """
    Repredents a Trader 
    """
    TRADER_LICENSE = 'trader'
    ANALYST_LICENSE = 'analyst'
    DEMO_LICENSE = 'demo'
    LICENSE_CHOICES = [
        (TRADER_LICENSE, 'Trader License'),
        (ANALYST_LICENSE, 'Analyst License'),
        (DEMO_LICENSE, 'Demo License')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    license_type = ArrayField(models.CharField(
        max_length=150, choices=LICENSE_CHOICES))
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class ContactPerson(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=250, default='Test first name')
    last_name = models.CharField(max_length=250, default='Test last name')
    telephone = models.CharField(max_length=250, default='Test 555555555')
    email = models.EmailField(max_length=250, default='test@mail.com')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    institution_lead = models.ForeignKey(
        InstitutionLead, on_delete=models.SET_NULL, null=True)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    contact_person = models.ForeignKey(
        ContactPerson, on_delete=models.SET_NULL, null=True)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Concierge(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    leads = models.ManyToManyField(Lead)
    institutions = models.ManyToManyField(Institution)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class SecurityIssuer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)


class Security(models.Model):

    class Meta:
        verbose_name_plural = "Securities"

    REG_CNBV = 'cnbv'
    REG_144A = '144a'
    REG_REG_S = 'reg-s'
    REG_SEC_REG = 'sec-reg'
    REG_MEX_PP = 'mex-pp'
    REG_SOV = 'sov'
    REG_SOV_GTEE = 'sov-gtee'
    REGISTRATION_CHOICES = [
        (REG_CNBV, 'CNBV'),
        (REG_144A, '144A'),
        (REG_REG_S, 'RegS'),
        (REG_SEC_REG, 'SEC-Reg'),
        (REG_MEX_PP, 'Mex PP'),
        (REG_SOV, 'Sov'),
        (REG_SOV_GTEE, 'Sov Gtee')
    ]

    TYPE_M_BONO = 'm-bono'
    TYPE_MEX_CORP_CEBUR = 'mex-corp-cebur'
    TYPE_MEX_CORP_ST_CEBUR_CP = 'mex-corp-st-cebur-cp'
    TYPE_ASSET_BACKEND_CEBUR_F = 'asset-backend-cebur-f'
    TYPE_CETE = 'cete'
    TYPE_BONDE = 'bonde'
    SECURITY_TYPE_CHOICES = [
        (TYPE_M_BONO, 'MBono'),
        (TYPE_MEX_CORP_CEBUR, 'Mex Corp (CEBUR)'),
        (TYPE_MEX_CORP_ST_CEBUR_CP, 'Mex Corp St (CEBUR CP)'),
        (TYPE_ASSET_BACKEND_CEBUR_F, 'Asset-Backed (CEBUR F)'),
        (TYPE_CETE, 'CETE'),
        (TYPE_BONDE, 'BONDE')
    ]

    SENIOR_SENIORITY = 'senior'
    SUBORDINATE_SENIORITY = 'subordinate'
    CONTINGENT_CAPITAL_AT1 = 'contingent-capital-at1'
    CONTINGENT_CAPITAL_T2 = 'contingent-capital-t2'
    SENIORITY_TYPE_CHOICES = [
        (SENIOR_SENIORITY, 'Senior'),
        (SUBORDINATE_SENIORITY, 'Subordinate'),
        (CONTINGENT_CAPITAL_AT1, 'Contingent Capital AT1'),
        (CONTINGENT_CAPITAL_T2, 'Contingent Capital T2')
    ]

    GUARANTEE_SECURED = 'secured'
    GUARANTEE_UNSECURED = 'unsecured'
    GUARANTEE_TYPE_CHOICES = [
        (GUARANTEE_SECURED, 'Secured'),
        (GUARANTEE_UNSECURED, 'Unsecured')
    ]

    AVERAGE_30_DAY = '30-day-avg'
    REDEMPTION_TYPE_CHOICES = [
        (AVERAGE_30_DAY, '30 day average')
    ]

    # NOTE: consider moving currency definition elsewhere
    USD_CURRENCY = 'usd'
    MXN_CURRENCY = 'mxn'
    UDI_CURRENCY = 'udi'
    CURRENCY_OF_PAYMENTS_CHOICES = [
        (USD_CURRENCY, 'US Dollars'),
        (MXN_CURRENCY, 'Mexican Peso')
    ]
    CURRENCY_RISK_CHOICES = (
        (USD_CURRENCY, 'US Dollar'),
        (MXN_CURRENCY, 'Mexican Peso'),
        (UDI_CURRENCY, 'UDI')
    )

    DAY_COUNT_CONVENTION_MX_ACT_360 = 'mx-act-360'
    DAY_COUNT_CONVENTION_US_30_360 = 'us-30-360'
    DAY_COUNT_CONVENTION_CHOICES = (
        (DAY_COUNT_CONVENTION_MX_ACT_360, 'MEX Conv (ACT/360)'),
        (DAY_COUNT_CONVENTION_US_30_360, 'US Conv (30/360)')
    )

    PERIOD_7_DAYS = '7d'
    PERIOD_28_DAYS = '28d'
    PERIOD_182_DAYS = '182d'
    PERIOD_360_DAYS = '360d'
    COUPON_PERIOD_CHOICES = (
        (PERIOD_7_DAYS, '7 days'),
        (PERIOD_28_DAYS, '28 days'),
        (PERIOD_182_DAYS, '182 days'),
        (PERIOD_360_DAYS, '360 days'),
    )

    BULLET = 'bullet'
    AMORTIZER = 'amortizer'
    SOFT_BULLET = 'soft-bullet'
    VARIABLE_AMORTIZER = 'variable-amortizer'
    AMORTIZATION_STRUCTURE_CHOICES = (
        (BULLET, 'Bullet'),
        (AMORTIZER, 'Amortizer'),
        (SOFT_BULLET, 'Soft bullet'),
        (VARIABLE_AMORTIZER, 'Variable amortizer'),
    )

    INDEVAL_CLEARING = 'indeval'
    DTC_CLEARING = 'dtc'
    EUROCLEAR_CLEARING = 'euroclear'
    CLEARSTREAM_CLEARING = 'clearstream'
    CLEARING_CHOICES = (
        (INDEVAL_CLEARING, 'Indeval'),
        (DTC_CLEARING, 'DTC'),
        (EUROCLEAR_CLEARING, 'Euroclear'),
        (CLEARSTREAM_CLEARING, 'Clearstream')
    )

    BMV_LISTING = 'bmv'
    LUX_LISTING = 'lux'
    STG_LISTING = 'stg'
    LISTING_CHOICES = [
        (BMV_LISTING, 'BMV'),
        (LUX_LISTING, 'LUX'),
        (STG_LISTING, 'STG'),
    ]

    CATEGORY_FIXED_RATE = 'fixed-rate'
    CATEGORY_CHOICES = [
        (CATEGORY_FIXED_RATE, 'Fixed Rate')
    ]

    SECURITY_REMAINING_TENOR_FILTER_CHOICES = (
        # NOTE: used for filtering remaining tenor
        # codes for remaining tenor are provided in days. Structure for code must be:
        # <lte>_<number_of_min_days>[_<gte>_<number_of_max_days>]
        ("lte_30", "< 1month"),
        ("gte_30__lte_90", "1-3 months"),
        ("gte_90__lte_180", "3-6 months"),
        ("gte_180__lte_365", "6-12 months"),
        ("gte_365__lte_1095", "1-3 years"),
        ("gte_1095__lte_1825", "3-5 years"),
        ("gte_1825__lte_2920", "5-8 years"),
        ("gte_2920__lte_4380", "8-12 years"),
        ("gte_4380__lte_7300",  "12-20 years"),
        ("gte_7300__lte_10950", "20-30 years")
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    isin = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    ticker = models.CharField(max_length=250)
    series = models.CharField(max_length=250, unique=True)
    issuer = models.ForeignKey(
        SecurityIssuer, on_delete=models.SET_NULL, null=True)
    registration = models.CharField(
        max_length=250, choices=REGISTRATION_CHOICES)
    classification_mx = models.CharField(max_length=250)
    # amortization_scheme must have following structure: {0:{ "date": "08/08/19", "amort": "0"}, 1:{"date": "06/02/20", "amort": "0"}, 2:{"date": "06/08/20", "amort": "1"}}
    amortization_scheme = models.JSONField(encoder=DjangoJSONEncoder)

    coupon_rate = models.DecimalField(max_digits=40, decimal_places=20)
    initial_margin = models.DecimalField(max_digits=40, decimal_places=20)
    issue_date = models.DateTimeField()
    first_coupon_date = models.DateTimeField()
    final_maturity_date = models.DateTimeField()
    nominal_value = models.DecimalField(max_digits=40, decimal_places=20)
    year_day_count = models.IntegerField()
    redemption_price = models.DecimalField(max_digits=40, decimal_places=20)
    security_notes = models.CharField(
        max_length=250)
    number_of_payments = models.PositiveIntegerField()
    issued_amount = models.DecimalField(max_digits=40, decimal_places=20)
    outstanding = models.DecimalField(max_digits=40, decimal_places=20)
    category = models.CharField(
        max_length=250, choices=CATEGORY_CHOICES)
    listing = ArrayField(models.CharField(
        max_length=150, choices=LISTING_CHOICES))
    clearing = ArrayField(models.CharField(
        max_length=150, choices=CLEARING_CHOICES))
    amortization_structure = models.CharField(
        max_length=150, choices=AMORTIZATION_STRUCTURE_CHOICES)
    redemption_type = models.CharField(
        max_length=150, choices=REDEMPTION_TYPE_CHOICES)
    coupon_period = models.CharField(
        max_length=150, choices=COUPON_PERIOD_CHOICES)
    day_count_convention = models.CharField(
        max_length=150, choices=DAY_COUNT_CONVENTION_CHOICES)
    currency_risk = models.CharField(
        max_length=150, choices=CURRENCY_RISK_CHOICES)
    currency_of_payments = models.CharField(
        max_length=150, choices=CURRENCY_OF_PAYMENTS_CHOICES)
    security_type = models.CharField(
        max_length=150, choices=SECURITY_TYPE_CHOICES)
    seniority = models.CharField(
        max_length=150, choices=SENIORITY_TYPE_CHOICES)
    guarantee = models.CharField(
        max_length=150, choices=GUARANTEE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # validate amortization_scheme_data
        amortization_scheme = self.amortization_scheme

        # checar estructura de lo que see envió y de paso convertir a integer las keys
        dict_with_int_keys = dict()
        for key, val in amortization_scheme.items():
            try:
                int_key = int(key)

            except Exception as e:
                raise ValidationError(
                    'Check amort scheme info for creating security')
            if "date" not in val.keys():
                raise ValidationError(
                    "All amort scheme rows must have a 'date' value")
            if "amort" not in val.keys():
                raise ValidationError(
                    "All amort scheme rows must have an 'amort' value")
            if "outstanding" not in val.keys():
                raise ValidationError(
                    "All amort scheme rows must have an 'outstanding' value")
            if "interest" not in val.keys():
                raise ValidationError(
                    "All amort scheme rows must have an 'interest' value")
            dict_with_int_keys[int_key] = val

        return

    def get_remaining_tenor(self, settlement_date=datetime.now()):
        """
        Returns Security's remaining tenor as specified in spreadsheet
        """
        date_format = "%d/%m/%Y"
        year_day_count = self.year_day_count
        amortization_scheme = self.amortization_scheme

        amortization_dict = dict()
        # make sure keys are sorted chronologically
        for key, val in amortization_scheme.items():
            amortization_dict[int(key)] = {'amort': float(
                val['amort']), 'date': val['date']}

        for key in sorted(amortization_dict.keys()):
            date_t = datetime.strptime(
                amortization_dict[key]['date'], date_format)
            amortization_dict[key]['years'] = (
                daydiff(settlement_date, date_t, 'ACTUAL/365 FIXED')) / year_day_count
            amortization_dict[key]['weight'] = amortization_dict[key]['years'] * \
                amortization_dict[key]['amort'] if amortization_dict[key]['years'] > 0 else 0
        # compute remaining tenor (wal)
        remaining_tenor = sum([v['weight']
                               for k, v in amortization_dict.items()])
        # TODO: check if following expression is correct (should we multiply by something else other than 365?)
        return remaining_tenor * 365

    def get_outstanding_mxn(self):
        # get currency exchange rate (note that an additional outstanding filter is performed in this case since outstanding_mxn may be reduced to outstanding, provided we have the currency exchange rate)
        dolar_peso_exchange_rate = 20
        return float(self.outstanding) * float(dolar_peso_exchange_rate)

    # TODO: discuss
    def get_issued_amount_mxn(self):
        dolar_peso_exchange_rate = 20
        return float(self.issued_amount) * float(dolar_peso_exchange_rate)


class SettlementInstruction(models.Model):

    # these clearing valiues ust be in sync with securities'
    INDEVAL_CLEARING = 'indeval'
    DTC_CLEARING = 'dtc'
    EUROCLEAR_CLEARING = 'euroclear'
    CLEARSTREAM_CLEARING = 'clearstream'
    CLEARING_CHOICES = (
        (INDEVAL_CLEARING, 'Indeval'),
        (DTC_CLEARING, 'DTC'),
        (EUROCLEAR_CLEARING, 'Euroclear'),
        (CLEARSTREAM_CLEARING, 'Clearstream')
    )

    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]

    name = models.CharField(max_length=250)
    document = models.ForeignKey(
        File, null=True, on_delete=models.SET_NULL)
    clearing_house = models.CharField(max_length=250, choices=CLEARING_CHOICES)
    account = models.CharField(max_length=250)
    bic_code = models.CharField(max_length=250)
    custodian = models.CharField(max_length=250)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    trader = models.ForeignKey(Trader, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)


class Alarm(models.Model):

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
    security = models.ForeignKey(
        Security, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CobOrder(models.Model):

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
    trader = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL)
    security = models.ForeignKey(
        Security, null=True, on_delete=models.SET_NULL)
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
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: update order_group ref when in same module s OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group = models.UUIDField()


class CobAutoRefresher(models.Model):

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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class CobStream(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    # TODO: update order_group ref when in same module as OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group = models.UUIDField()


class Rfq(models.Model):

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
    security = models.ForeignKey(
        Security, null=True, on_delete=models.SET_NULL)
    trader = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL)
    anonymous = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    submission = models.DateTimeField()
    expiration = models.DateTimeField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    direction = models.CharField(
        max_length=150, choices=DIRECTION_CHOICES)
    volume = models.IntegerField()
    counterparties = models.ManyToManyField(Institution)
    settlement_currency = models.CharField(
        max_length=150, choices=SETTLEMENT_CURRENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # TODO: update order_group ref when in same module s OrderGroup
    # order_group = models.ForeignKey(
    #     OrderGroup, on_delete=models.SET_NULL, null=True)
    order_group = models.UUIDField()


class RfqResponse(models.Model):

    CANCELLED_STATUS = 'cancelled'
    EXPIRED_STATUS = 'expired'
    ACTIVE_STATUS = 'active'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (CANCELLED_STATUS, 'Cancelled'),
        (EXPIRED_STATUS, 'Expired')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    trader = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL)
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

    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class RfqAutoResponder(models.Model):

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
    security = models.ForeignKey(
        Security,  on_delete=models.SET_NULL, null=True)
    trader = models.ForeignKey(
        Trader, on_delete=models.SET_NULL, null=True)
    counterparties = models.ManyToManyField(Institution)
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

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)


class RfqLock(models.Model):
    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    trader = models.ForeignKey(Trader, on_delete=models.SET_NULL, null=True)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)

# class BaseTransaction(models.Model):
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
#     created_at = models.DateTimeField()


class CobTransaction(models.Model):
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
    buyer = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL, related_name='cob_transaction_buyer')
    seller = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL, related_name='cob_transaction_seller')
    security = models.ForeignKey(
        Security, null=True, on_delete=models.SET_NULL)
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
    created_at = models.DateTimeField()
    sell_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL, related_name='cob_sell_order')
    buy_order = models.ForeignKey(
        CobOrder, null=True, on_delete=models.SET_NULL, related_name='cob_buy_order')
    spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)


class RfqTransaction(models.Model):
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
    buyer = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL, related_name='rfq_transaction_buyer')
    seller = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL, related_name='rfq_transaction_seller')
    security = models.ForeignKey(
        Security, null=True, on_delete=models.SET_NULL)
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
    created_at = models.DateTimeField()
    rfq = models.ForeignKey(
        Rfq, null=True, on_delete=models.SET_NULL)
    rfq_response = models.ForeignKey(
        RfqResponse, null=True, on_delete=models.SET_NULL)


class Watchlist(models.Model):

    ACTIVE_STATUS = 'active'
    DEACTIVATED_STATUS = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (DEACTIVATED_STATUS, 'Deactivated')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    trader = models.ForeignKey(
        Trader, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)
    securities = models.ManyToManyField(Security)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    archived_at = models.DateTimeField(null=True, blank=True)


class TradeBlockSettlement(models.Model):

    FAILED_STATUS = 'failed'
    SETTLED_STATUS = 'settled'
    STATUS_CHOICES = [
        (FAILED_STATUS, 'Failed'),
        (SETTLED_STATUS, 'Settled')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    settlement_instruction = models.ForeignKey(
        SettlementInstruction, on_delete=models.SET_NULL, null=True)
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class TradeBlock(models.Model):
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
    security = models.ForeignKey(
        Security, on_delete=models.SET_NULL, null=True)
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
    buyer = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, related_name='buyer_institution')
    seller = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, related_name='seller_institution')
    booked_by = models.ForeignKey(
        Trader, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Notification(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class NotificationSettings(models.Model):

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_type = models.CharField(
        max_length=250, choices=Notification.TYPE_CHOICES)
    notify_as = ArrayField(models.CharField(
        max_length=250, choices=NOTIFY_AS_CHOICES))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


model_list = [
    Address,
    File,
    UserSettings,
    User,
    InstitutionManager,
    Controller,
    ComplianceOfficer,
    InstitutionLead,
    Institution,
    Trader,
    ContactPerson,
    Lead,
    Concierge,
    SecurityIssuer,
    Security,
    SettlementInstruction,
    Alarm,
    CobOrder,
    CobAutoRefresher,
    CobStream,
    Rfq,
    RfqResponse,
    RfqAutoResponder,
    RfqLock,
    CobTransaction,
    RfqTransaction,
    Watchlist,
    # TradeBlock,
    TradeBlockSettlement,
    Notification,
    NotificationSettings
]
