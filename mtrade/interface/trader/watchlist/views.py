# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# TODO: Remove app zero
from app_zero.models import Watchlist
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

WATCHLIST_ZERO_SERVICES = DefaultAppZeroServices(Watchlist)
WATCHLIST_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(Watchlist, WATCHLIST_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.watchlist_list_extension,
    retrieve=open_api.watchlist_retrieve_extension,
    create=open_api.watchlist_create_extension,
    update=open_api.watchlist_update_extension,
    partial_update=open_api.watchlist_partial_update_extension,
    destroy=open_api.watchlist_destroy_extension,
)
class WatchlistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WATCHLIST_ZERO_SERIALIZER

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by institution path
        order_by_string=self.request.query_params.get('order_by', 'id')
        return WATCHLIST_ZERO_SERVICES.list_resources(self.request.user).order_by(order_by_string)
