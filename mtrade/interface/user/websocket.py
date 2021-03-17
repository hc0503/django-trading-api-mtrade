# python imports
import json
from typing import List
from collections.abc import Callable

# django imports
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# app imports
from mtrade.application.users.services import UserAppServices as uas

class WSConsumer(WebsocketConsumer):
    populators : List[Callable] = []

    @classmethod
    def register(cls, populator: Callable):
        cls.populators.append(populator)

    @classmethod
    def empty_populator(cls):
        cls.populators = []

    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                'users_{}'.format(self.user.id),
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_add)(
                'users',
                self.channel_name
            )
            self.accept()

            for populator in self.populators:
                for message in populator(self.user):
                    uas.websocket_send(self.user, 'raw.message', message.payload)
        else:
            self.close()

    def disconnect(self, close_code):
        # TODO: Execute disconnect action that corresponds to close_code
        async_to_sync(self.channel_layer.group_discard)(
            'users_{}'.format(self.user.id),
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            'users',
            self.channel_name
        )

    # Receive from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type': text_data_json['type'],
            'message': message
        }))

    # Raw Message
    def raw_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))
