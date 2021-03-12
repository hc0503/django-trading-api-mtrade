from django.urls import re_path

from . import websocket

websocket_urlpatterns = [
    re_path(r'ws/(?P<module_name>\w+)/$', websocket.WSConsumer.as_asgi()),
]