from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.institution.models import Institution
from mtrade.application.institution.services import InstitutionAppServices

from rest_framework import serializers


class InstitutionSerializer(ApplicationModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
