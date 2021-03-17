from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.market.order_group.models import OrderGroup
# DISCUSS: is it ok to fetch services from domain or should it only be application in this case?
from mtrade.application.security.services import SecurityAppServices
from mtrade.application.users.services import UserAppServices
from mtrade.application.institution.services import InstitutionAppServices
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
        security = SecurityAppServices.get_security_by_id(
            security_id=obj.security_id)
        return security.name

    def get_security_isin(self, obj):
        security = SecurityAppServices.get_security_by_id(
            security_id=obj.security_id)
        return security.isin

    def get_trader(self, obj):
        """Returns the user's name (that is associated to a given trader)"""
        trader_id = obj.trader_id
        user = UserAppServices.get_user_by_id(user_id=trader_id)
        user_full_name = user.get_full_name()
        return user_full_name

    def get_requestor_institution(self, obj: OrderGroup):
        """Returns anonymous if requestor type is anonymous. Else, returns institution name"""
        if obj.requestor_type == obj.REQUESTOR_TYPE_ANONYMOUS:
            return obj.REQUESTOR_TYPE_ANONYMOUS[1]

        institution_id = obj.requestor_institution_id
        institution = InstitutionAppServices.get_institution_by_id(
            institution_id=institution_id)
        return institution.name
