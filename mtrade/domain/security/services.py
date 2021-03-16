# python imports
from typing import Type

# django imports
from django.db.models.manager import Manager

# local imports
from .models import Security, SecurityFactory, SecurityIssuer, SecurityIssuerFactory


class SecurityServices():

    @staticmethod
    def get_security_factory() -> Type[SecurityFactory]:
        return SecurityFactory

    @staticmethod
    def get_security_repo() -> Type[Manager]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return Security.objects

    @staticmethod
    def get_security_by_id(security_id) -> Security:
        return Security.objects.get(id=security_id)

    @staticmethod
    def get_security_issuer_factory() -> Type[SecurityIssuerFactory]:
        return SecurityIssuerFactory

    @staticmethod
    def get_security_issuer_repo() -> Type[Manager]:
        # We expose the whole repository as a service to avoid making a service
        # for each repo action. If some repo action is used constantly in
        # multiple places consider exposing it as a service.
        return SecurityIssuer.objects
