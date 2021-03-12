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
class NotificationID():
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """
    #value: uuid.UUID = field(init=False, default_factory=uuid.uuid4)
    value: uuid.UUID

@dataclass(frozen=True)
class Payload():
    value: dict

class Notification(custom_models.DatedModel):
    """
    A Notification represents the entrypoint for any type of trades of a given security
    """
    id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.UUIDField()
    notification_type = models.IntegerField()
    payload = models.JSONField()
    priority = models.IntegerField()
    status = models.CharField(max_length=2, default='ur')

    def update_entity(self, user_id: str, notification_type: int, payload: Payload, priority: int, status: str):
        if user_id is not None:
            self.user_id = user_id
        if notification_type is not None:
            self.notification_type = notification_type
        if payload is not None:
            self.payload = json.dumps(payload.value)
        if priority is not None:
            self.priority = priority
        if status is not None:
            self.status = status

    class Meta:
        ordering = ['id']

class NotificationFactory():
    @staticmethod
    def build_entity(notification_id: NotificationID, user_id: str, notification_type: int, payload: Payload, priority: int, status: str) -> Notification:
        return Notification(id = notification_id.value, user_id = user_id, notification_type = notification_type, payload = json.dumps(payload.value), priority = priority, status = status)

    @classmethod
    def build_entity_with_id(cls, user_id: str, notification_type: int, payload: Payload, priority: int, status: str) -> Notification:
        notification_id = NotificationID(uuid.uuid4())
        return cls.build_entity(notification_id, user_id, notification_type, payload, priority, status)
