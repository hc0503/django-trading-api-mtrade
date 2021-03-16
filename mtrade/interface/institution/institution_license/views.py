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
from .serializers import InstitutionLicenseSerializer


@extend_schema_view(
    list=open_api.inst_license_list_extension,
    retrieve=open_api.inst_license_retrieve_extension,
    create=open_api.inst_license_create_extension,
    update=open_api.inst_license_update_extension,
    partial_update=open_api.inst_license_partial_update_extension,
)
class InstitutionLicenseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with Institution Managers
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstitutionLicenseSerializer
    filterset_fields = ()
    ordering = ['-created_at']

    def get_queryset(self):
        order_by_string = self.request.query_params.get('order_by', 'id')
        return InstitutionAppServices.list_institution_licenses().order_by(order_by_string)
