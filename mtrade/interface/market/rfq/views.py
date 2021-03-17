# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response

# app imports
from lib.django.custom_views import CreateListRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import Rfq
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer


# local imports
from . import open_api
RFQ_ZERO_SERVICES = DefaultAppZeroServices(Rfq)
RFQ_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(Rfq, RFQ_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.rfq_list_extension,
    retrieve=open_api.rfq_retrieve_extension,
    create=open_api.rfq_create_extension,
)
class RfqViewSet(CreateListRetrieveViewSet):
    """
    Allows clients to perform order operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQ_ZERO_SERIALIZER
    #filterset_fields = ('direction', 'security',
    #                    'trader', 'status', 'order_group')
    ordering = ['-created_at']

    # TODO: add missing filetr fields: 'institution'
    # TODO: add filter based on security isin

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by market path
        return RFQ_ZERO_SERVICES.list_resources(self.request.user)
