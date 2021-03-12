# django imports
from mtrade.interface.user.websocket import WSConsumer
from .services import NotificationAppServices as nas

WSConsumer.register(nas.list_unread_notifications)