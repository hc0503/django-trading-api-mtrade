# python imports
import asyncio
from asgiref.sync import sync_to_async

# django imports
from django.test import TestCase
from django.db.models.query import QuerySet
from channels.testing import WebsocketCommunicator

# app imoprts
from mtrade.drivers.asgi import application
from mtrade.domain.notifications.models import Notification
from mtrade.domain.notifications.services import NotificationServices as ns
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices

# local imports
from .services import NotificationAppServices as nos
from mtrade.interface.user.websocket import WSConsumer

class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, headers=None, subprotocols=None, user=None):
        super().__init__(application, path, headers, subprotocols)
        if user is not None:
            self.scope['user'] = user

class NotificationAppServicesTests(TestCase):
    def setUp(self):
        self.u_data_01 = UserPersonalData(
            username = 'Teser',
            first_name = 'Testerman',
            last_name = 'Testerson',
            email = "testerman@example.com"
        )
        self.u_permissions_01 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )
        self.user_01 = UserAppServices.create_user(self.u_data_01, self.u_permissions_01)

    def test_list_notifications(self):
        nqs = nos.list_notifications(self.user_01)
        self.assertEqual(type(nqs), QuerySet)

    def test_list_unread_notifications(self):
        nqs = nos.list_unread_notifications(self.user_01)
        self.assertEqual(type(nqs), QuerySet)

    async def test_create_notification(self):
        communicator = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)
        connected, subprotocol = await communicator.connect()
        data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": {"message": "A new probject is created", "period": 30},
            "priority": 1,
            "status": 'ur'
        }
        message = {
            'type': 'raw.message',
            'message': '{"message": "A new probject is created", "period": 30}'
        }
        ntc = await sync_to_async(nos.create_notification_from_dict)(self.user_01, data)
        self.assertEqual(type(ntc), Notification)

        # Test notification created and websocket sent successfully
        response = await communicator.receive_json_from()
        self.assertEqual(response == message, True)

        # Test notification was stored
        stored_notification = await sync_to_async(ns.get_notification_repo().get)(id=ntc.id)
        self.assertEqual(type(stored_notification), Notification)

        await communicator.disconnect()

        # Test notfication created but websocket sent failure
        ntc = await sync_to_async(nos.create_notification_from_dict)(self.user_01, data)
        self.assertEqual(type(ntc), Notification)

        try:
            await communicator.receive_json_from()
            assert False
        except asyncio.TimeoutError:
            assert True

    def test_update_notification(self):
        data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": {"message": "A new probject is created", "period": 30},
            "priority": 1,
            "status": 'ur'
        }
        ntc = nos.create_notification_from_dict(self.user_01, data)

        pre_update_created_at = ntc.created_at
        pre_update_modified_at = ntc.modified_at

        updated_data = {
            "user_id": "c13cce88-42e3-40a1-9402-abf7e2f0a297",
            "notification_type": 1,
            "payload": {"message": "A new probject is created", "period": 30},
            "priority": 1,
            "status": 'rd'
        }

        nos.update_notification_from_dict(self.user_01, ntc, updated_data)

        ntc.refresh_from_db()
        self.assertEqual(ntc.status, 'rd')

        self.assertEqual(ntc.created_at, pre_update_created_at)
        self.assertNotEqual(ntc.modified_at, pre_update_modified_at)
