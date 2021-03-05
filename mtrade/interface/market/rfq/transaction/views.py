# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# TODO: Remove app zero
from app_zero.models import RfqTransaction
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api


RFQ_TRANSACTION_ZERO_SERVICES = DefaultAppZeroServices(RfqTransaction)
RFQ_TRANSACTION_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(
    RfqTransaction, RFQ_TRANSACTION_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.rfq_transaction_list_extension,
    retrieve=open_api.rfq_transaction_retrieve_extension
)
class RfqTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RFQ_TRANSACTION_ZERO_SERIALIZER
    ordering = ['-created_at']


    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        return RFQ_TRANSACTION_ZERO_SERVICES.list_resources(self.request.user)
