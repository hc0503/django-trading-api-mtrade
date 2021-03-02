# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response

# app imports
from lib.django.custom_views import CreateListRetrieveViewSet

# TODO: Remove app zero
from mtrade.application.market.cob.services import COB_ZERO_SERVICES

# local imports
from . import open_api
from . serializers import COBSerializer


@extend_schema_view(
    list=open_api.cob_list_extension,
    retrieve=open_api.cob_retrieve_extension,
    create=open_api.cob_create_extension
)
class COBViewSet(CreateListRetrieveViewSet):
    """
    Allows clients to perform order operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = COBSerializer
    filterset_fields = ('direction','security__isin', 'trader', 'origin')
    # TODO: add missing filetr fields: 'institution'

    def get_queryset(self):
    # TODO: handle request path properly by filtering orders by market path
        order_by_string=self.request.query_params.get('order_by', 'id')
        return COB_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)

    ## TODO: Remove this method once model is implemented
    #def retrieve(self, request, pk=None, market_pk=None):
    #    serializer = COBSerializer(self.get_queryset().get(id=pk))
    #    return Response(serializer.data)

    ## TODO: Replace with call to service
    ## TODO: Ensure only resources of current market path are allowed
    #def create(self, request, market_pk=None):
    #    serializer = COBSerializer(data=request.data)
    #    if not serializer.is_valid():
    #        raise BadRequest(serializer.errors)
    #    return Response(serializer.data)
