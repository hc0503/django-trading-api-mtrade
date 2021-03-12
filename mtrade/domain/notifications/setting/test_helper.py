# python imports
import typing

# django imports

# app imports

# local imports
from .models import (
    NotificationSetting,
    NotificationSettingFactory
)

# TODO: set a constant random seed to get repeatable results
def generate_random_notification_setting() -> NotificationSetting:
    return NotificationSettingFactory.build_entity_with_id("CRM", True, True)

def generate_random_notification_settings(num_of_notification_settings: int) -> typing.List[NotificationSetting]:
    notification_settings = []
    for _ in range(num_of_notification_settings):
        notification_settings.append(generate_random_notification_setting())
    return notification_settings


