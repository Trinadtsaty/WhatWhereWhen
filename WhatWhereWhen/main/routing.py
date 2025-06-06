# from django.urls import path
# from . import consumers
#
# websocket_urlpatterns = [
#     path('ws/game_room/<int:room_id>/', consumers.GameRoomConsumer.as_asgi()),
# ]

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # w+ - когда слово
    # d+ - когда число
    # URL паттерн для WebSocket соединений
    # Используйте либо именованную группу (без указания типа)
    # re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # Или просто числовой ID
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),


]