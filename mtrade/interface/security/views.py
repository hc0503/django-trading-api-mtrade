# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from mtrade.application.security.services import SecurityAppServices

# local imports
from . import open_api
from .serializers import SecuritySerializer


@extend_schema_view(
    list=open_api.security_list_extension,
)
class SecurityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SecuritySerializer
    filterset_fields = []
    ordering = ['-created_at']

    def get_queryset(self):
        order_by_string = self.request.query_params.get('order_by', 'id')
        return SecurityAppServices.list_securities().order_by(order_by_string)
