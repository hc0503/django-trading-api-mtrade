# python imports

# django imports
from rest_framework import permissions

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet
from mtrade.application.market.services import MarketAppServices as mas

# local imports
from .serializers import MarketSerializer

class MarketViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform retrieve and list Markets
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarketSerializer

    def get_queryset(self):
        return mas.list_markets(self.request.user)
