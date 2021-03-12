"""
ASGI config for mtrade project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mtrade.interface.user.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtrade.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            mtrade.interface.user.routing.websocket_urlpatterns
        )
    ),
})
