# python imports
from typing import Tuple

# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException

# app imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices

# local imports
from .serializers import UserSerializer, GroupSerializer


class BadRequest(APIException):
    status_code = 400
    default_detail = 'The request cannot be fulfilled, please try again with different parameters.'
    default_code = 'bad_request'


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def serializer_to_value_objects(serializer) -> Tuple[UserPersonalData, UserBasePermissions]:
        v = serializer.validated_data
        personal_data = None
        base_permissions = None
        try:
            personal_data = UserPersonalData(
                username = v['username'],
                first_name = v['first_name'],
                last_name = v['last_name'],
                email = v['email']
            )
            base_permissions = UserBasePermissions(
                is_staff = False,
                is_active = True
            )
        except:
            raise BadRequest()

        return (personal_data, base_permissions)

    def perform_create(self, serializer):
        u_data, u_permissions = self.serializer_to_value_objects(serializer)
        return UserAppServices.create_user(u_data, u_permissions)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
