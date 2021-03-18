# python imports
import logging

# django imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# app imports
from mtrade.domain.users.models import User, UserPersonalData, UserBasePermissions
from mtrade.domain.users.services import UserServices

log = logging.getLogger(__name__)


class UserAppServices():
    user_factory = UserServices.get_user_factory()

    @classmethod
    def create_user(
            cls, personal_data: UserPersonalData,
            base_permissions: UserBasePermissions) -> User:
        # This method is not strictly necessary since it only wraps a call to the user factory.
        user = cls.user_factory.build_entity_with_id(
            personal_data, base_permissions)
        # NOTE: This does not handle user password
        user.save()
        log.info("model saved")
        return user

    @classmethod
    def websocket_send(
            cls,
            ws_user: User,
            ws_type: str,
            ws_payload: str) -> bool:
        # This method send websocket payload to a user
        if ws_user.is_authenticated:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'users_{}'.format(ws_user.id),
                {
                    'type': ws_type,
                    'message': ws_payload
                }
            )
            return True
        else:
            return False

    @staticmethod
    def get_user_by_id(user_id) -> User:
        return UserServices.get_user_repo().get(id=user_id)
