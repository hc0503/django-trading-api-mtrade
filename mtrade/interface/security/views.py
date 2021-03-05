# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports

# TODO: Remove app zero
from app_zero.models import Security
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer


SECURITY_ZERO_SERVICES = DefaultAppZeroServices(Security)
SECURITY_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(Security, SECURITY_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.security_list_extension,
)
class SecurityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SECURITY_ZERO_SERIALIZER
    ordering = ['-created_at']


    def get_queryset(self):
        return SECURITY_ZERO_SERVICES.list_resources(self.request.user)
