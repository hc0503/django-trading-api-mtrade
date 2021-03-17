from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.market.order_group.models import OrderGroup
# DISCUSS: is it ok to fetch services from domain or should it only be application in this case?
from mtrade.domain.security.services import SecurityServices
from mtrade.domain.users.services import UserServices
from mtrade.domain.institution.services import InstitutionServices
from rest_framework import serializers


class OrderGroupSerializer(ApplicationModelSerializer):
    """
    This serializer is intended for a blotter view
    """

    security_name = serializers.SerializerMethodField()
    security_isin = serializers.SerializerMethodField()
    trader = serializers.SerializerMethodField()
    requestor_institution = serializers.SerializerMethodField()

    class Meta:
        model = OrderGroup
        fields = '__all__'

    def get_security_name(self, obj):
        security = SecurityServices.get_security_by_id(
            security_id=obj.security_id)
        print(security)
        # search for security name in security domain services
        # conviene obtener el repo completo o ir directamente sobre la security?
        return security.name

    def get_security_isin(self, obj):
        security = SecurityServices.get_security_by_id(
            security_id=obj.security_id)
        print(security)
        return security.isin

    def get_trader(self, obj):
        """Returns the user's name (that is associated to a given trader)"""
        trader_id = obj.trader_id
        user = UserServices.get_user_by_id(user_id=trader_id)
        user_full_name = user.get_full_name()
        return user_full_name

    def get_requestor_institution(self, obj):
        institution_id = obj.requestor_institution_id
        institution = InstitutionServices.get_institution_by_id(
            institution_id=institution_id)
        return institution.name
