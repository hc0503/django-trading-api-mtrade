# python imports

# django imports
from rest_framework import viewsets

# app imports
from mtrade.domain.market.models import Market

# local imports
from .serializers import MarketSerializer


class MarketViewSet(viewsets.ModelViewSet):
    """
    Allows clients to perform CRUD operations on markets
    """
    serializer_class = MarketSerializer
    queryset = Market.objects.all()
