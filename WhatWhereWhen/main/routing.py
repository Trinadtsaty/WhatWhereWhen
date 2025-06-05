from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/game_room/<int:room_id>/', consumers.GameRoomConsumer.as_asgi()),
]