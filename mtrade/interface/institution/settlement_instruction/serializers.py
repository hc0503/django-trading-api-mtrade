from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.institution.models import SettlementInstruction
from mtrade.application.institution.services import InstitutionAppServices

from rest_framework import serializers


class SettlementInstructionSerializer(ApplicationModelSerializer):
    class Meta:
        model = SettlementInstruction
        fields = '__all__'
