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

# local imports
from .websocket import WSConsumer
from .tests_websocket_helper import test_populator

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
        connected, _ = await communicator.connect()
        self.assertIs(connected, True)
        await communicator.disconnect()

        # Rejects a user that hasn't logged in
        communicator = AuthWebsocketCommunicator(application, "/ws/users/", user = AnonymousUser())
        connected, _ = await communicator.connect()
        self.assertIs(connected, False)

    # async def test_initial_message_populator(self):

    async def test_websocket_send_A_not_B(self):
        WSConsumer.empty_populator()
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
        WSConsumer.empty_populator()
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
        WSConsumer.empty_populator()
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

    async def test_register(self):
        # Test if populators contains initial_message funcs
        WSConsumer.register(test_populator)
        self.assertIs(test_populator in WSConsumer.populators, True)
        communicator = AuthWebsocketCommunicator(application, "/ws/users/", user = self.user_01)

        await communicator.connect()
        response1 = await communicator.receive_json_from()
        message1 = {
            'type': 'raw.message',
            'message': 'Inital message testing 1'
        }
        assert message1 == response1

        response2 = await communicator.receive_json_from()
        message2 = {
            'type': 'raw.message',
            'message': 'Inital message testing 2'
        }
        assert message2 == response2

        await communicator.disconnect()
