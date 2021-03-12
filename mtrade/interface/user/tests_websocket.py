# django imports
import asyncio
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser

# app imports
from mtrade.drivers.asgi import application
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from mtrade.application.notifications.services import NotificationAppServices as nas

# local imports
from .websocket import WSConsumer

class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, headers=None, subprotocols=None, user=None):
        super().__init__(application, path, headers, subprotocols)
        if user is not None:
            self.scope['user'] = user

class WebSocketTest(TestCase):
    def setUp(self):
        self.u_data_01 = UserPersonalData(
            username = 'user_A',
            first_name = 'Testerman',
            last_name = 'Testerson',
            email = "user1@example.com"
        )
        self.u_permissions_01 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )

        self.u_data_02 = UserPersonalData(
            username = 'user_B',
            first_name = 'Testerman',
            last_name = 'Testerson',
            email = "user2@example.com"
        )
        self.u_permissions_02 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )

        self.user_01 = UserAppServices.create_user(self.u_data_01, self.u_permissions_01)
        self.user_02 = UserAppServices.create_user(self.u_data_02, self.u_permissions_02)

    async def test_websocket_connect(self):
        # Accepts a user that has logged in
        communicator = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)
        connected, subprotocol = await communicator.connect()
        self.assertIs(connected, True)
        await communicator.disconnect()

        # Rejects a user that hasn't logged in
        communicator = AuthWebsocketCommunicator(application, "/ws/users/", user = AnonymousUser())
        connected, subprotocol = await communicator.connect()
        self.assertIs(connected, False)

    def test_register(self):
        # Test if populators contains initial_message funcs
        self.assertIs(nas.list_unread_notifications in WSConsumer.populators, True)

    async def test_websocket_send_A_not_B(self):
        communicator1 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)
        communicator2 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_02)
        await communicator1.connect()
        await communicator2.connect()
        message = {
            'type': 'raw.message',
            'message': 'This is a raw message.'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('users_{}'.format(self.user_01.id), message=message)
        response1 = await communicator1.receive_json_from()
        assert response1 == message
        try:
            await communicator2.receive_json_from()
            assert False
        except asyncio.TimeoutError:
            assert True
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_websocket_send_B_not_A(self):
        communicator1 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)
        communicator2 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_02)
        await communicator1.connect()
        await communicator2.connect()
        message = {
            'type': 'raw.message',
            'message': 'This is a raw message.'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('users_{}'.format(self.user_02.id), message=message)
        response2 = await communicator2.receive_json_from()
        assert response2 == message
        try:
            await communicator1.receive_json_from()
            assert False
        except asyncio.TimeoutError:
            assert True
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_websocket_send_all(self):
       communicator1 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)
       communicator2 = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_02)
       await communicator1.connect()
       await communicator2.connect()
       message = {
           'type': 'raw.message',
           'message': 'This is a raw message.'
       }
       channel_layer = get_channel_layer()
       await channel_layer.group_send('users', message=message)
       response1 = await communicator1.receive_json_from()
       response2 = await communicator2.receive_json_from()
       assert response1 == response2 == message
       await communicator1.disconnect()
       await communicator2.disconnect()
