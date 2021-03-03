# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports

# TODO: Remove app zero
from app_zero.models import InstitutionLead
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

INST_LEAD_ZERO_SERVICES = DefaultAppZeroServices(InstitutionLead)
INST_LEAD_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(InstitutionLead, INST_LEAD_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.inst_lead_list_extension,
    retrieve=open_api.inst_lead_retrieve_extension
)
class InstitutionLeadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = INST_LEAD_ZERO_SERIALIZER

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        order_by_string=self.request.query_params.get('order_by', 'id')
        return INST_LEAD_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)
