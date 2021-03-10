# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.security.services import SecurityServices as ss
from mtrade.domain.security.models import Security, SecurityFactory, SecurityIssuer, SecurityIssuerFactory


class SecurityAppServices():

    @staticmethod
    def list_securities() -> QuerySet:
        return ss.get_security_repo().all()
