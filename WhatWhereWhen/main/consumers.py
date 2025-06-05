# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import game_rooms


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):

# async def connect(self):
    #     self.room_id = self.scope['url_route']['kwargs']['room_id']
    #     self.user_id = self.scope['user'].ID  # Предполагается аутентификация
    #     self.room_group_name = f'game_room_{self.room_id}'
    #
    #     # Добавляем пользователя в комнату
    #     success = await self.add_user_to_room()
    #     if not success:
    #         await self.close()
    #         return
    #
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     await self.accept()
    #
    #     # Отправляем обновленный список пользователей
    #     await self.send_user_list()
    #
    #     # Проверяем условие старта (5 пользователей)
    #     await self.check_start_condition()
    #
    # async def disconnect(self, close_code):
    #     # Удаляем пользователя из комнаты
    #     await self.remove_user_from_room()
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     # Отправляем обновленный список пользователей
    #     await self.send_user_list()
    #
    # @database_sync_to_async
    # def add_user_to_room(self):
    #     try:
    #         room = game_rooms.objects.get(ID=self.room_id)
    #         if not room.people_on_page.get('users'):
    #             room.people_on_page = {'users': []}
    #
    #         if self.user_id not in room.people_on_page['users']:
    #             room.people_on_page['users'].append(self.user_id)
    #             room.save()
    #             return True
    #     except ObjectDoesNotExist:
    #         return False
    #     return False
    #
    # @database_sync_to_async
    # def remove_user_from_room(self):
    #     try:
    #         room = game_rooms.objects.get(ID=self.room_id)
    #         if self.user_id in room.people_on_page.get('users', []):
    #             room.people_on_page['users'].remove(self.user_id)
    #             room.save()
    #             return True
    #     except ObjectDoesNotExist:
    #         return False
    #     return False
    #
    # @database_sync_to_async
    # def get_room_users(self):
    #     try:
    #         room = game_rooms.objects.get(ID=self.room_id)
    #         return room.people_on_page.get('users', [])
    #     except ObjectDoesNotExist:
    #         return []
    #
    # async def send_user_list(self):
    #     users = await self.get_room_users()
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'user_list',
    #             'users': users,
    #             'count': len(users)
    #         }
    #     )
    #
    # async def check_start_condition(self):
    #     users = await self.get_room_users()
    #     if len(users) >= 5:  # Или room.room_limit если хотите использовать лимит комнаты
    #         await self.channel_layer.group_send(
    #             self.room_group_name,
    #             {
    #                 'type': 'start_game',
    #                 'message': 'Игра начинается! Набрано достаточное количество игроков!'
    #             }
    #         )
    #
    # # Обработчики сообщений для группы
    # async def user_list(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'user_list',
    #         'users': event['users'],
    #         'count': event['count']
    #     }))
    #
    # async def start_game(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'start_game',
    #         'message': event['message']
    #     }))