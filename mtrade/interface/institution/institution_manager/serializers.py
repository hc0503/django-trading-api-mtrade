from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.institution.models import InstitutionManager
from mtrade.application.institution.services import InstitutionAppServices

from rest_framework import serializers


class InstitutionManagerSerializer(ApplicationModelSerializer):
    class Meta:
        model = InstitutionManager
        fields = '__all__'
