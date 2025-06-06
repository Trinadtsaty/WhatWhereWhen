from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from registration.models import Users
from .models import ChatMessage, game_rooms
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    # Вызывается при установке WebSocket соединения.
    async def connect(self):
        # Имя комнаты из URL (можно использовать для групповых чатов)
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Присоединяемся к группе комнаты
        await self.channel_layer.group_add(
            # Имя комнаты
            self.room_group_name,
            # Уникальный идентификатор подключения
            self.channel_name
        )
        # Принимаем соединение
        await self.accept()


    # Вызывается при закрытии WebSocket соединения.
    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Вызывается при получении сообщения от WebSocket.
    async def receive(self, text_data):
        # print("мы в receive")
        # Парсим JSON данные
        try:

            text_data_json = json.loads(text_data)
            # print(text_data_json)
            room_id = text_data_json['room_ID']
            message = text_data_json['message']
            user_id = text_data_json['user_id']
        except (json.JSONDecodeError, KeyError) as e:
            await self.send(text_data=json.dumps({"error": "Invalid format"}))
            return

        # Получаем объект пользователя (синхронный код в асинхронном окружении)
        user = await self.get_user(user_id)
        room = await  self.get_room(room_id)

        # Сохраняем сообщение в MySQL (синхронный код)
        await self.save_message(room, user, message)
        # saved_msg = await self.save_message(room, user, message)

        # Лог после сохранения
        # print(f"Message saved with ID: {saved_msg.ID}")

        # Отправляем сообщение в группу комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.login
            }
        )

    # Отправляет сообщение обратно в WebSocket.
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Отправляем сообщение WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


    # Вспомогательный метод для получения пользователя из БД.
    # Декоратор database_sync_to_async позволяет выполнять синхронные ORM запросы.
    @database_sync_to_async
    def get_user(self, user_id):
        return Users.objects.get(ID=user_id)

    @database_sync_to_async
    def get_room(self, room_id):
        return game_rooms.objects.get(ID=room_id)

    # Вспомогательный метод для сохранения сообщения в БД.
    @database_sync_to_async
    def save_message(self, room, user, message):
        # print("мы в save_message")
        return ChatMessage.objects.create(room=room, user=user, message=message)





from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class PeopleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'people_{self.room_id}'
        self.user_id = self.scope['user'].ID

        await self.add_user_to_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.notify_all_about_users()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.remove_user_from_room()
            await self.notify_all_about_users()
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    async def send_users_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'users_list',
            'users': event['users']
        }))

    @sync_to_async
    def remove_user_from_room(self):
        from .models import game_rooms
        try:
            room = game_rooms.objects.get(ID=self.room_id)
            if self.user_id in room.people_on_page.get("users", []):
                room.people_on_page["users"].remove(self.user_id)
                room.save()
                print(len(room.people_on_page["users"]))

                #Раскомитить когда завершу отладку
                # if len(room.people_on_page["users"]) ==0:
                #     room.delete()

        except Exception as e:
            print(f"Error removing user: {e}")

    async def notify_all_about_users(self):
        users_data = await self.get_room_users_data()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_users_list',
                'users': users_data
            }
        )

    @sync_to_async
    def get_room_users_data(self):
        from registration.models import Users
        from .models import game_rooms
        from django.conf import settings

        try:
            room = game_rooms.objects.get(ID=self.room_id)
            users_ids = room.people_on_page.get("users", [])
            users = Users.objects.filter(ID__in=users_ids)

            return [
                {
                    'id': user.ID,
                    'login': user.login,
                    'picture': settings.MEDIA_URL + str(
                        user.picture) if user.picture else settings.STATIC_URL + 'default-avatar.png'
                }
                for user in users
            ]
        except Exception as e:
            print(f"Error getting room users data: {e}")
            return []

    @sync_to_async
    def add_user_to_room(self):
        from .models import game_rooms

        room = game_rooms.objects.get(ID=self.room_id)
        if "users" not in room.people_on_page:
            room.people_on_page = {"users": []}

        if self.user_id not in room.people_on_page["users"]:
            room.people_on_page["users"].append(self.user_id)
            room.save()


class StartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].ID
        self.room_group_name = f'action_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Вызывается при закрытии WebSocket соединения.
    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Получаем данные пользователя
            user = await self.get_user(self.user_id)
            data = json.loads(text_data)

            print(f"Получены данные от {user.login}:", data)

            # Определяем тип действия и сообщение
            action_info = {
                'start': ('start', f"Пользователь {user.login} начал игру"),
                'pause': ('pause', f"Пользователь {user.login} поставил на паузу"),
                'play': ('play', f"Пользователь {user.login} возобновил игру")
            }

            # Ищем первое совпадение действия
            for key in action_info:
                if key in data:
                    action_type, log_message = action_info[key]
                    message = data[key]
                    print(log_message)
                    break
            else:
                print("Неизвестный тип действия")
                await self.send(text_data=json.dumps({
                    'error': 'Unknown action type',
                    'received_data': data
                }))
                return

            # Формируем сообщение для рассылки
            group_message = {
                'type': 'handle_action_event',  # Важно: должно соответствовать имени метода
                'action_type': action_type,
                'message': message,
                'username': user.login,
                'user_id': self.user_id,
                'timestamp': str(datetime.now())
            }

            # Отправляем в группу
            await self.channel_layer.group_send(
                self.room_group_name,
                group_message
            )

        except json.JSONDecodeError:
            error_msg = "Ошибка декодирования JSON"
            print(error_msg)
            await self.send(text_data=json.dumps({
                'error': error_msg,
                'received_data': text_data
            }))
        except Exception as e:
            error_msg = f"Ошибка обработки сообщения: {str(e)}"
            print(error_msg)
            await self.send(text_data=json.dumps({
                'error': error_msg,
                'details': str(e)
            }))

    async def handle_action_event(self, event):
        """Обработчик для action-сообщений"""
        try:
            response = {
                'type': event.get('action_type', 'unknown_action'),
                'message': event.get('message', ''),
                'username': event.get('username', 'unknown'),
                'user_id': event.get('user_id', 0),
                'timestamp': event.get('timestamp', str(datetime.now()))
            }

            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")


    @database_sync_to_async
    def get_user(self, user_id):
        return Users.objects.get(ID=user_id)