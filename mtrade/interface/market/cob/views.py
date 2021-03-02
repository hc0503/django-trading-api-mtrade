# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response

# app imports
from lib.django.custom_views import CreateListRetrieveViewSet
from mtrade.application.market.cob.services import COBAppServices

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
        for q_param, val in params:
            if q_param == 'page':
                continue
            filtered_qs = filtered_qs.filter(**{q_param:val[0]})
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
