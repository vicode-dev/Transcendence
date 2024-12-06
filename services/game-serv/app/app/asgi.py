"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django_asgi_app = get_asgi_application()
import chat.routing, lobby.routing, app.routing, tournament.routing

from lobby.middleware import AuthMiddleware
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddleware(
                URLRouter(
                    chat.routing.websocket_urlpatterns +
                    lobby.routing.websocket_urlpatterns +
                    app.routing.websocket_urlpatterns + 
                    tournament.routing.websocket_urlpatterns
                )
            )
        )
    }
)
