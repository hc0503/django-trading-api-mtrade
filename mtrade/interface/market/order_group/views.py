# python imports

# django imports
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions
from rest_framework.response import Response

# app imports
from lib.django.custom_views import CreateListUpdateRetrieveViewSet

# TODO: Remove app zero
from mtrade.domain.market.order_group.models import OrderGroup
from .serializers import OrderGroupSerializer
from mtrade.application.market.order_group.services import OrderGroupAppServices
# from app_zero.services import DefaultAppZeroServices
# from app_zero.serializers import buildDefaultAppZeroSerializer

# local imports
from . import open_api
#from . serializers import COBSerializer

# ORDER_GROUP_ZERO_SERVICES = DefaultAppZeroServices(OrderGroup)
# ORDER_GROUP_ZERO_SERIALIZER = buildDefaultAppZeroSerializer(
#    OrderGroup, ORDER_GROUP_ZERO_SERVICES)


@extend_schema_view(
    list=open_api.order_group_list_extension,
    retrieve=open_api.order_group_retrieve_extension,
    create=open_api.order_group_create_extension,
    partial_update=open_api.order_group_partial_update_extension,
    update=open_api.order_group_update_extension,
)
class OrderGroupViewSet(CreateListUpdateRetrieveViewSet):
    """
    Allows clients to perform order operations
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderGroupSerializer
    filterset_fields = ('direction',  'trader')
    ordering = ('-created_at',)
    # TODO: add missing filetr fields: 'institution'
    # TODO: consider adding security__isin filter

    def get_queryset(self):
        # TODO: handle request path properly by filtering orders by market path
        order_by_string = self.request.query_params.get('order_by', 'id')
        return OrderGroupAppServices.list_order_groups(self.request.user).order_by(order_by_string)