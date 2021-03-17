# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import RfqResponse
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api

RFQ_RESPONSE_ZERO_SERVICES = DefaultAppZeroServices(RfqResponse)
RFQ_RESPONSE_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(
    RfqResponse, RFQ_RESPONSE_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.rfq_response_list_extension,
    retrieve=open_api.rfq_response_retrieve_extension,
    create=open_api.rfq_response_create_extension,
    update=open_api.rfq_response_update_extension,
    partial_update=open_api.rfq_response_partial_update_extension
)
class RfqResponseViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform RfqResponse operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQ_RESPONSE_ZERO_SERIALIZER
    #filterset_fields = ('trader',)
    ordering = ['-created_at']

    # TODO: add missing filetr fields: 'institution'

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by market path
        return RFQ_RESPONSE_ZERO_SERVICES.list_resources(self.request.user)
