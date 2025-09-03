"""
ASGI config for nymega project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import hmi.routing # Import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nymega.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
  "http": get_asgi_application(), # Handles standard HTTP requests
  "websocket": AuthMiddlewareStack( # Handles WebSocket requests
        URLRouter(
            hmi.routing.websocket_urlpatterns
        )
    ),
})
