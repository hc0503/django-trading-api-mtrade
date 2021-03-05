# python imports

# django imports
from rest_framework import permissions
#from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import ListUpdateRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import CobStream
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer


# local imports
from . import open_api
#from . serializers import COBSerializer

COBSTREAM_ZERO_SERVICES = DefaultAppZeroServices(CobStream)
COBSTREAM_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(CobStream, COBSTREAM_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.cobstream_list_extension,
    retrieve=open_api.cobstream_retrieve_extension,
    update=open_api.cobstream_update_extension,
    partial_update=open_api.cobstream_partial_update_extension,
)
class CobStreamViewSet(ListUpdateRetrieveViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = COBSTREAM_ZERO_SERIALIZER
    ordering = ['-created_at']

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        return COBSTREAM_ZERO_SERVICES.list_resources(self.request.user)
