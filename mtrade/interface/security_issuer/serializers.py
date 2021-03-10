from lib.django.custom_serializers import ApplicationModelSerializer
from mtrade.domain.security.models import SecurityIssuer


class SecurityIssuerSerializer(ApplicationModelSerializer):

    class Meta:
        model = SecurityIssuer
        fields = '__all__'
