# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework import filters
import django_filters

# app imports
from lib.django.custom_views import CreateListRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import CobOrder
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

COB_ZERO_SERVICES = DefaultAppZeroServices(CobOrder)
COB_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(
    CobOrder, COB_ZERO_SERVICES)

@extend_schema_view(
    list=open_api.cob_list_extension,
    retrieve=open_api.cob_retrieve_extension,
    create=open_api.cob_create_extension,
)
class COBViewSet(CreateListRetrieveViewSet):
    """
    Allows clients to perform order operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = COB_ZERO_SERIALIZER
    filterset_fields = ('direction', 'security__isin', 'trader', 'order_group')
    ordering = ['-created_at']
    # TODO: add missing filetr fields: 'institution'

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by market path
        return COB_ZERO_SERVICES.list_resources(self.request.user)
