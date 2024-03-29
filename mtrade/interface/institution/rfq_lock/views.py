# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.institution.services import InstitutionAppServices

# local imports
from . import open_api
from .serializers import RfqLockSerializer


@extend_schema_view(
    list=open_api.rfq_lock_list_extension,
    retrieve=open_api.rfq_lock_retrieve_extension,
    create=open_api.rfq_lock_create_extension,
    update=open_api.rfq_lock_update_extension,
    partial_update=open_api.rfq_lock_partial_update_extension,
)
class RfqLockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with Rfq Locks
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RfqLockSerializer
    filterset_fields = ()
    ordering = ['-created_at']

    def get_queryset(self):
        order_by_string = self.request.query_params.get('order_by', 'id')
        return InstitutionAppServices.list_rfq_locks().order_by(order_by_string)
