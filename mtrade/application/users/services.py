# python imports
import uuid
from typing import Tuple
from decimal import Decimal
import logging

# app imports
from mtrade.domain.users.models import User, UserPersonalData, UserBasePermissions
from mtrade.domain.users.services import UserServices

log = logging.getLogger(__name__)

class UserAppServices():
    user_factory = UserServices.get_user_factory()

    @classmethod
    def create_user(cls, personal_data: UserPersonalData, base_permissions: UserBasePermissions) -> User:
        # This method is not strictly necessary since it only wraps a call to the user factory.
        user = cls.user_factory.build_entity_with_id(personal_data, base_permissions)
        # NOTE: This does not handle user password
        user.save()
        log.info("model saved")
        return user
