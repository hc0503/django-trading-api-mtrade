# python imports
import uuid
import json
import typing

# django imports
from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiExample
from rest_framework.pagination import PageNumberPagination

# app imports
from mtrade.domain.users.services import UserServices
from mtrade.domain.users.models import User, UserPersonalData, UserBasePermissions
from mtrade.interface.lib.open_api import paginate

# local imports
from .serializers import UserSerializer


# 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#personal_data_01 = UserPersonalData(
#    username = "Tester",
#    first_name = "Testerman",
#    last_name = "Testerson",
#    email = "testerman@example.com"
#)
#base_permissions_01 = UserBasePermissions(
#    is_staff = False,
#    is_active = False
#)
#
#example_user_01 = UserServices.get_user_factory().build_entity_with_id(personal_data_01, base_permissions_01)
#
#paginator = Paginator([example_user_01], 5)
#page = paginator.page(1)
#
#p_paginator = PageNumberPagination()
#p_paginator.page = page
#paginated_serializer = p_paginator.get_paginated_response(page)

example_user_01 = {
    "id": "c40f48bd-4320-4dd5-8bad-de89cda09c20",
    "username": "Tester",
    "first_name": "Testerman",
    "last_name": "Testerson",
    "email": "testerman@example.com",
}

user_list_extension=extend_schema(
        request=None,
        responses={
            200: UserSerializer
        },
        examples=[
            OpenApiExample(
                'User data',
                summary='Paginated user data',
                description='Get a user by its full name',
                value=paginate([example_user_01])
            )
        ]
    )
