# python imports
import json
from pathlib import Path

# django imports
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import permissions
from rest_framework import viewsets

# app imports
from mtrade.interface.lib.open_api import paginate

# local imports


class BadRequest(APIException):
    status_code = 400
    default_detail = 'The request cannot be fulfilled, please try again with different parameters.'
    default_code = 'bad_request'


class SecurityViewSet(viewsets.ViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]

    dummy_securities = None

    path = Path(__file__).parent / "dummy_data/securities.json"
    with path.open(mode='r') as f:
        dummy_securities = json.load(f)

    def list(self, request):
        resp = paginate(self.dummy_securities)
        return Response(resp)

    def retrieve(self, request, pk=None):
        try:
            resp = next(
                item for item in self.dummy_securities if item["id"] == pk)
        except:
            raise BadRequest()
        return Response(resp)
