import logging
import uuid

from dataclasses import dataclass

from django.db import models
from datetime import datetime
from lib.django import custom_models

from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import ArrayField

from lib.data_manipulation.daydiff import daydiff


logger = logging.getLogger(__name__)


class SecurityIssuer(custom_models.DatedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)

    def update_entity(self):
        # TODO: implement this method
        pass


class SecurityIssuerFactory():
    @staticmethod
    def build_entity(**kwargs) -> SecurityIssuer:
        security_issuer = SecurityIssuer(**kwargs)
        security_issuer.full_clean()
        return security_issuer


class Security(custom_models.DatedModel):

    class Meta:
        verbose_name_plural = "Securities"
        ordering = ['id']

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

    def clean(self):
        # validate amortization_scheme_data
        amortization_scheme = dict(self.amortization_scheme)

        # checar estructura de lo que see envió y de paso convertir a integer las keys
        dict_with_int_keys = dict()
        for key, val in amortization_scheme.items():
            try:
                int_key = int(key)

            except Exception:
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
        This method must be validated. Returns Security's remaining tenor as specified in spreadsheet
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

    def update_entity(self):
        # TODO: discuss if and how we should implement this method
        pass


class SecurityFactory():
    @staticmethod
    def build_entity(**kwargs) -> Security:
        security = Security(**kwargs)
        security.full_clean()
        return security
