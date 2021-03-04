# python imports

# django imports
from rest_framework import permissions
#from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import Concierge
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

CONCIERGE_ZERO_SERVICES = DefaultAppZeroServices(Concierge)
CONCIERGE_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(Concierge, CONCIERGE_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.concierge_list_extension,
    retrieve=open_api.concierge_retrieve_extension,
    create=open_api.concierge_create_extension,
    update=open_api.concierge_update_extension,
    partial_update=open_api.concierge_partial_update_extension,
)
class ConciergeViewSet(CreateListUpdateRetrieveViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CONCIERGE_ZERO_SERIALIZER

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        order_by_string=self.request.query_params.get('order_by', 'id')
        return CONCIERGE_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)
