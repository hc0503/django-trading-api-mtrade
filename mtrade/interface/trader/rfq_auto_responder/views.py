# python imports

# django imports
from rest_framework import permissions
#from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet

# TODO: Remove app zero
from app_zero.models import RfqAutoResponder
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

RFQ_AUTO_RESPONDER_ZERO_SERVICES = DefaultAppZeroServices(RfqAutoResponder)
RFQ_AUTO_RESPONDER_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(RfqAutoResponder, RFQ_AUTO_RESPONDER_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.rfq_auto_responder_list_extension,
    retrieve=open_api.rfq_auto_responder_retrieve_extension,
    create=open_api.rfq_auto_responder_create_extension,
    update=open_api.rfq_auto_responder_update_extension,
    partial_update=open_api.rfq_auto_responder_partial_update_extension,
)
class RfqAutoResponderViewSet(CreateListUpdateRetrieveViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQ_AUTO_RESPONDER_ZERO_SERIALIZER
    ordering = ['-created_at']

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        return RFQ_AUTO_RESPONDER_ZERO_SERVICES.list_resources(self.request.user)
