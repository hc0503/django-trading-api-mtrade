# python imports

# django imports
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# app imports
from mtrade.application.market.services import MarketAppServices as mas

# local imports
from .serializers import MarketSerializer

class MarketViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows clients to perform retrieve and list Markets
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarketSerializer

    def get_queryset(self):
        return mas.list_markets(self.request.user)
