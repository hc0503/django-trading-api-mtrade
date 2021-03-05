# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports

# TODO: Remove app zero
from app_zero.models import CobTransaction
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

COB_TRANSACTION_ZERO_SERVICES = DefaultAppZeroServices(CobTransaction)
COB_TRANSACTION_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(CobTransaction, COB_TRANSACTION_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.cob_transaction_list_extension,
    retrieve=open_api.cob_transaction_retrieve_extension,
)
class CobTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = COB_TRANSACTION_ZERO_SERIALIZER
    ordering = ['-created_at']

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        return COB_TRANSACTION_ZERO_SERVICES.list_resources(self.request.user)
