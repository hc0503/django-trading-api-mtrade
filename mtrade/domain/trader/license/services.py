# python imports
from typing import Type

# django imports
from django.db.models.manager import BaseManager

# local imports
from .models import TraderLicenseFactory
from .models import TraderLicense


class TraderLicenseServices():

    @staticmethod
    def get_license_factory() -> Type[TraderLicenseFactory]:
        return TraderLicenseFactory

    @staticmethod
    def get_license_repo() -> BaseManager[TraderLicense]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return TraderLicense.objects
