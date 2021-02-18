# python imports
import json
from pathlib import Path

# django imports
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import permissions
from rest_framework import viewsets

# app imports

# local imports

class BadRequest(APIException):
    status_code = 400
    default_detail = 'The request cannot be fulfilled, please try again with different parameters.'
    default_code = 'bad_request'


class SecurityView(viewsets.ViewSet):
    """
    API endpoint that allows the client to interact with securities.
    """
    permission_classes = [permissions.IsAuthenticated]

    dummy_securities = None

    path = Path(__file__).parent / "dummy_data/securities.json"
    with path.open(mode='r') as f:
        dummy_securities = json.load(f)

    def list(self, request):
        """
        Return a list of securities
        """
        # TODO: Define if it requires pagination, pagination changes response structure
        resp = self.dummy_securities

        return Response(resp)
