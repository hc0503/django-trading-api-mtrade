# python imports
import typing

# django imports

# app imports
from mtrade.domain.users.models import User

# local imports
from .models import (
    Notification,
    Payload,
    NotificationFactory
)

# TODO: set a constant random seed to get repeatable results
def generate_random_notification(user: User) -> Notification:
    return NotificationFactory.build_entity_with_id(user.id, 1, Payload({"message": "A new probject is created", "period": 30}), 1, 'ur')

def generate_random_notifications(user: User, num_of_notifications: int) -> typing.List[Notification]:
    notifications = []
    for _ in range(num_of_notifications):
        notifications.append(generate_random_notification(user))
    return notifications


