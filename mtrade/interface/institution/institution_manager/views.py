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
from .serializers import InstitutionManagerSerializer


@extend_schema_view(
    list=open_api.inst_manager_list_extension
)
class InstitutionManagerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with Institution Managers
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstitutionManagerSerializer
    filterset_fields = ()
    ordering = ['-created_at']

    def get_queryset(self):
        order_by_string = self.request.query_params.get('order_by', 'id')
        return InstitutionAppServices.list_institution_managers().order_by(order_by_string)
