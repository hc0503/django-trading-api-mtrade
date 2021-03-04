# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports

# TODO: Remove app zero
from app_zero.models import SecurityIssuer
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer


SECURITY_ISSUER_ZERO_SERVICES = DefaultAppZeroServices(SecurityIssuer)
SECURITY_ISSUER_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(SecurityIssuer, SECURITY_ISSUER_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.security_issuer_list_extension,
)
class SecurityIssuerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SECURITY_ISSUER_ZERO_SERIALIZER

    def get_queryset(self):
        order_by_string=self.request.query_params.get('order_by', 'id')
        return SECURITY_ISSUER_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)
