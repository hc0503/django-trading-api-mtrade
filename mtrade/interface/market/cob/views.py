# python imports
import json
from pathlib import Path

# django imports
from rest_framework import viewsets
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view
from django_filters import rest_framework as filters
from rest_framework.response import Response

# app imports
from mtrade.interface.lib.open_api import paginate
from mtrade.interface.lib.base_responses import BadRequest
from mtrade.interface.lib.custom_views import CreateListRetrieveViewSet
from mtrade.application.market.services import COBAppServices
from mtrade.domain.market.models import Market
from mtrade.domain.market.cob.models import COBOrder

# local imports
from . import open_api
from . serializers import (
    COBSerializer
)


@extend_schema_view(
    list=open_api.cob_list_extension,
    retrieve=open_api.cob_retrieve_extension,
    create=open_api.cob_create_extension
)
class COBViewSet(CreateListRetrieveViewSet):
    """
    Allows clients to perform CRUD operations on markets
    """
    serializer_class = COBSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        base_queryset = COBAppServices.list_cob_orders(self.request.user, self.kwargs['market_pk'])
        # TODO: replace following block with django-filter
        filtered_qs = base_queryset
        params = self.request.query_params.lists()
        for qp, val in params:
            if qp == 'page':
                continue
            filtered_qs = filtered_qs.filter(**{qp:val[0]})
        return filtered_qs

    # TODO: Remove this method once model is implemented
    def retrieve(self, request, pk=None, market_pk=None):
        serializer = COBSerializer(self.get_queryset().get(id=pk))
        return Response(serializer.data)

    ## TODO: Replace with call to service
    #def create(self, request, market_pk=None):
    #    serializer = COBSerializer(data=request.data)
    #    if not serializer.is_valid():
    #        raise BadRequest(serializer.errors)
    #    return Response(serializer.data)
