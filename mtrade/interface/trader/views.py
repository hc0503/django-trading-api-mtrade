# python imports

# django imports
from rest_framework import permissions
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet

# TODO: Remove app zero
from mtrade.domain.trader.models import Trader
from app_zero.services import DefaultAppZeroServices
from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer


TRADER_ZERO_SERVICES = DefaultAppZeroServices(Trader)
TRADER_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(
    Trader, TRADER_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.trader_list_extension,
)
class TraderViewSet(CreateListUpdateRetrieveViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TRADER_ZERO_SERIALIZER
    ordering = ['-created_at']

    def get_queryset(self):
        return TRADER_ZERO_SERVICES.list_resources(self.request.user)
