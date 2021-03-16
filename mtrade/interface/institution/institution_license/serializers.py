from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.institution.models import InstitutionLicense
from mtrade.application.institution.services import InstitutionAppServices

from rest_framework import serializers


class InstitutionLicenseSerializer(ApplicationModelSerializer):
    class Meta:
        model = InstitutionLicense
        fields = '__all__'
