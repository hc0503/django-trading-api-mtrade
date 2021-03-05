# python imports

# django imports
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.market.services import MarketAppServices as mas

# local imports
from . import open_api
from .serializers import MarketSerializer

@extend_schema_view(
    list=open_api.market_list_extension,
)
class MarketViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list Markets
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarketSerializer
    ordering = ['-created_at']

    def get_queryset(self):
        return mas.list_markets(self.request.user)
