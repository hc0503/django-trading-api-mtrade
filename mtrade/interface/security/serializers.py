from lib.django.custom_serializers import ApplicationModelSerializer
from mtrade.domain.security.models import Security


class SecuritySerializer(ApplicationModelSerializer):

    class Meta:
        model = Security
        fields = '__all__'
