"""
ASGI config for WhatWhereWhen project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# # from main.routing import websocket_urlpatterns  # импортируем маршруты
# import main.routing
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhatWhereWhen.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             main.routing.websocket_urlpatterns
#         )
#     ),
# })

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing
#
# application = ProtocolTypeRouter({
#     # Для HTTP запросов используется стандартный Django
#     'http': get_asgi_application(),
#
#     # Для WebSocket запросов
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhatWhereWhen.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})
