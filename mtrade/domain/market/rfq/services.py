# django imports
from .models import Rfq
from django.db.models.manager import Manager


from .models import Rfq


class RfqServices():

    @staticmethod
    def get_rfq_repo() -> Manager:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return Rfq.objects
