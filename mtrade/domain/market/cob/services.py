from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from typing import Type

from .models import COBOrder, COBOrderFactory

class COBServices():

    @staticmethod
    def get_cob_order_factory() -> Type[COBOrderFactory]:
        return COBOrderFactory

    @staticmethod
    def get_cob_order_repo() -> BaseManager[COBOrder]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return COBOrder.objects

    @staticmethod
    def get_queued_orders() -> QuerySet[COBOrder]:
        # TODO: Add partial db index for queued orders
        return COBOrder.objects.filter(status=COBOrder.STATUS_QUEUED). order_by('priority', 'size', 'id')
