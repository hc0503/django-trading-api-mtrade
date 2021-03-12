# python imports
import uuid
import json
from dataclasses import dataclass, field

# django imports
from django.db import models

# app imports
from lib.django import custom_models
from lib.ddd.exceptions import VOValidationExcpetion
#from lib.data_manipulation.type_conversion import asdict

# local imports

@dataclass(frozen=True)
class NotificationSettingID():
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """
    #value: uuid.UUID = field(init=False, default_factory=uuid.uuid4)
    value: uuid.UUID

class NotificationSetting(custom_models.DatedModel):
    """
    A NotificationSetting represents the entrypoint for any type of trades of a given security
    """
    id = models.UUIDField(primary_key=True, editable=False)
    module_name = models.CharField(max_length=255)
    email_enabled = models.BooleanField()
    ws_enabled = models.BooleanField()

    def update_entity(self, module_name: str, email_enabled: bool, ws_enabled: bool):
        if module_name is not None:
            self.module_name = module_name
        if email_enabled is not None:
            self.email_enabled = email_enabled
        if ws_enabled is not None:
            self.ws_enabled = ws_enabled

    class Meta:
        ordering = ['id']

class NotificationSettingFactory():
    @staticmethod
    def build_entity(notification_setting_id: NotificationSettingID, module_name: str, email_enabled: bool, ws_enabled: bool) -> NotificationSetting:
        return NotificationSetting(id = notification_setting_id.value, module_name = module_name, email_enabled = email_enabled, ws_enabled = ws_enabled)

    @classmethod
    def build_entity_with_id(cls, module_name: str, email_enabled: bool, ws_enabled: bool) -> NotificationSetting:
        notification_setting_id = NotificationSettingID(uuid.uuid4())
        return cls.build_entity(notification_setting_id, module_name, email_enabled, ws_enabled)
