# python imports
import json
from pathlib import Path

# django imports
from django.db.models.query import QuerySet

# app imports
from mtrade.domain.notifications.services import NotificationServices as ns
from mtrade.domain.notifications.models import Notification, Payload, NotificationFactory
from mtrade.application.users.services import UserAppServices as uas

class NotificationAppServices():
    @staticmethod
    def list_notifications(user) -> QuerySet:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return ns.get_notification_repo().all()

    def list_unread_notifications(user) -> QuerySet:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        return ns.get_notification_repo().filter(user_id=user.id).filter(status='ur')

    def create_notification_from_dict(user, data: dict) -> Notification:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        notification_type = data["notification_type"]
        payload = Payload(data["payload"])
        priority = data["priority"]
        status = data["status"]

        notification = NotificationFactory.build_entity_with_id(user.id, notification_type, payload, priority, status)
        notification.save()

        uas.websocket_send(user, 'raw.message', notification.payload)
        return notification

    def update_notification_from_dict(user, instance: Notification, data: dict) -> Notification:
        # TODO:
        # Fetch controller by user id
        # If controller does not exist propagate or handle exception
        # get notification by id

        notification_type = data.get("notification_type", None)
        data_payload = data.get("payload", None)
        priority = data.get("priority", None)
        status = data.get("status", None)

        payload = None
        if data_payload:
            payload = Payload(data_payload)

        instance.update_entity(user.id, notification_type, payload, priority, status)
        instance.save()
        return instance
