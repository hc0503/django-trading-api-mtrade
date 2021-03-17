from lib.django.custom_serializers import ApplicationModelSerializer

from mtrade.domain.institution.models import RfqLock
from mtrade.application.institution.services import InstitutionAppServices

from rest_framework import serializers


class RfqLockSerializer(ApplicationModelSerializer):
    class Meta:
        model = RfqLock
        fields = '__all__'
