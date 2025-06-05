from django.urls import path
from .consumers import MyConsumer  # Ваш consumer

websocket_urlpatterns = [
    path('ws/somepath/', MyConsumer.as_asgi()),
]
