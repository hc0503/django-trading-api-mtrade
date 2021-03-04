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
    create=open_api.rfq_create_extension
)
class RfqViewSet(CreateListRetrieveViewSet):
    """
    Allows clients to perform order operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQ_ZERO_SERIALIZER
    filterset_fields = ('direction', 'security__isin',
                        'trader', 'status', 'order_group')
    # TODO: add missing filetr fields: 'institution'

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by market path
        order_by_string = self.request.query_params.get('order_by', 'id')
        return RFQ_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)

    # TODO: Remove this method once model is implemented
    # def retrieve(self, request, pk=None, market_pk=None):
    #    serializer = COBSerializer(self.get_queryset().get(id=pk))
    #    return Response(serializer.data)

    # TODO: Replace with call to service
    # TODO: Ensure only resources of current market path are allowed
    # def create(self, request, market_pk=None):
    #    serializer = COBSerializer(data=request.data)
    #    if not serializer.is_valid():
    #        raise BadRequest(serializer.errors)
    #    return Response(serializer.data)
