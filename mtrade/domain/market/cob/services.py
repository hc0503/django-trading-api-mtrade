# django imports
from django.db.models.query import QuerySet
from django.db.models.manager import Manager

# local imports
from .models import COBOrderFactory
from .models import COBOrder


class COBServices():

    #@staticmethod
    #def get_cob_factory() -> COBOrderFactory:
    #    return COBOrderFactory

    @staticmethod
    def get_cob_repo() -> Manager:
        # We expose the whole repository as a service to avoid making a service for each repo action. If some repo action is used constantly in multiple places consider exposing it as a service.
        return COBOrder.objects
