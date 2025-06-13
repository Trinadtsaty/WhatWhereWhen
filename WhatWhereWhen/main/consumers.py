from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from registration.models import Users
from .models import ChatMessage, game_rooms
from channels.db import database_sync_to_async
import asyncio
from django.core.exceptions import ValidationError

# from ..questions.views import question, selection
from questions.views import question, selection

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
        from django.conf import settings
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
                'username': user.login,
                'user_id': user.ID,
                "picture_url": settings.MEDIA_URL + str(
                        user.picture) if user.picture else "/static/registration/img/Avatar.png",
            }
        )

    # Отправляет сообщение обратно в WebSocket.
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        picture = event['picture_url']
        user_id = event['user_id']
        # Отправляем сообщение WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'picture':picture,
            'user_id':user_id,
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
    # Нововедение
    disconnect_tasks = {}
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'people_{self.room_id}'
        self.user_id = self.scope['user'].ID

        # Новый элемент
        task = self.disconnect_tasks.pop(self.user_id, None)
        if task:
            task.cancel()

        await self.add_user_to_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.notify_all_about_users()


    # Принимаем значение
    async def receive(self, text_data):
        try:
            # Получаем данные пользователя
            # user = await self.get_user(self.user_id)
            data = json.loads(text_data)

            await self.change_role(data)
            await self.notify_all_about_users()

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

    # Старая версия без задержки
    # async def disconnect(self, close_code):
    #     if hasattr(self, 'room_group_name'):
    #         await self.remove_user_from_room()
    #         await self.notify_all_about_users()
    #         await self.channel_layer.group_discard(
    #             self.room_group_name,
    #             self.channel_name
    #         )

    # Новый вариант
    async def disconnect(self, close_code):
        # Запускаем задачу с задержкой удаления пользователя
        async def delayed_remove():
            try:
                await asyncio.sleep(10)  # ждем 10 секунд
                await self.remove_user_from_room()
                await self.notify_all_about_users()
            except asyncio.CancelledError:
                # Задача была отменена, значит пользователь переподключился
                pass

        task = asyncio.create_task(delayed_remove())
        self.disconnect_tasks[self.user_id] = task

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
    def change_role(self, data):
        from registration.models import Users
        from .models import game_rooms
        # print(f"Получены данные:", data['comands'])
        # print(f"Получены данные:", data['user'])
        try:
            room = game_rooms.objects.get(ID=self.room_id)
            user = Users.objects.get(ID=data['user'])

            if data['comands'] == "host":
                if self.user_id == room.host.ID:
                    room.host = user
                    room.save()
            if data['comands'] == "leader":
                room.leader = user
                room.save()
            if data['comands'] == "captain":
                room.captain = user
                room.save()
            if data['comands'] == "player":
                if room.captain == user:
                    room.captain = None
                    room.save()
                elif room.leader == user:
                    room.leader = None
                    room.save()



        except Exception as e:
            print(f"Error removing role: {e}")

    @sync_to_async
    def remove_user_from_room(self):
        from .models import game_rooms
        from registration.models import Users
        try:
            room = game_rooms.objects.get(ID=self.room_id)
            if self.user_id in room.people_on_page.get("users", []):
                room.people_on_page["users"].remove(self.user_id)
                room.save()
                # print("Пользователей на странице выход",len(room.people_on_page["users"]))

                #Раскомитить когда завершу отладку
                # if len(room.people_on_page["users"]) ==0:
                #     room.delete()

                first_player = Users.objects.get(ID=room.people_on_page["users"][0])
                if room.host.ID == self.user_id:
                    room.host = first_player
                    room.save()
                if room.leader.ID == self.user_id:
                    room.leader = None
                    room.save()
                if room.captain.ID == self.user_id:
                    room.captain = None
                    room.save()

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

            # Старый вариант
            users_ids = room.people_on_page.get("users", [])
            users = Users.objects.filter(ID__in=users_ids)
            arr_users = []
            for user in users:
                if room.host == user:
                    host = True
                else:
                    host = False
                if room.captain == user:
                    captain = True
                else:
                    captain = False
                if room.leader == user:
                    leader = True
                else:
                    leader = False

                arr_users.append({
                    'id': user.ID,
                    'login': user.login,
                    'host': host,
                    'captain': captain,
                    'leader': leader,
                    'picture': settings.MEDIA_URL + str(
                        user.picture) if user.picture else "/static/registration/img/Avatar.png"
                })

            return arr_users
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
            # if len(room.people_on_page["users"]) == room.room_limit:

    # @database_sync_to_async
    # def get_user(self, user_id):
    #     return Users.objects.get(ID=user_id)
    #
    # @database_sync_to_async
    # def get_room(self, room_id):
    #     return game_rooms.objects.get(ID=room_id)







class StartConsumer(AsyncWebsocketConsumer):
    time = 5
    question = {}
    stage = {"stage":"collecting", "condition":"expectation"}
    room_tasks = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].ID
        self.room_group_name = f'action_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        print(self.question)

        if self.question == {}:
            room = await self.get_room(self.room_id)
            await self.filling_question(room)

        await self.notify_stage()


        # Проверяем, заполнилась ли комната
        # await self.check_room_and_start()

    @sync_to_async
    def filling_question(self, room):
        from questions.models import Question
        questions = Question.objects.filter(Question_Select__selection_id=room.selections.ID)
        print(questions)
        for question in questions:
            self.question[question.ID] = {}
            self.question[question.ID]["question_name"] = question.question_name
            self.question[question.ID]["text_question"] = question.text_question
            self.question[question.ID]["note"] = question.note
            self.question[question.ID]["answer"] = question.answer
            self.question[question.ID]["answer_description"] = question.answer_description
            self.question[question.ID]["license_id"] = question.license_id.ID
            self.question[question.ID]["frostbite"] = True


    # Вызывается при закрытии WebSocket соединения.
    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def check_room_and_start(self):
    #     """Проверяет, заполнена ли комната, и отправляет 'start' если да"""
    #     room = await self.get_room(self.room_id)
    #     if len(room.people_on_page["users"]) == room.room_limit:
    #         user = await self.get_user(self.user_id)
    #
    #         group_message = {
    #             'type': 'handle_action_event',
    #             'action_type': 'start',
    #             'message': 'Game is starting automatically!',
    #             'username': 'System',
    #             'user_id': 0,  # System user
    #             'timestamp': str(datetime.now())
    #         }
    #
    #         await self.channel_layer.group_send(
    #             self.room_group_name,
    #             group_message
    #         )

    async def receive(self, text_data):
        room = await self.get_room(self.room_id)
        async def timer_5_sec():
            try:
                # await self.send_start_timer(self.time)
                for i in range(self.time,0,-1):
                    await asyncio.sleep(1)
                    print(f"Обратный отсчет {i} секунда")
                print("0 секунд")
                print("start")

            except asyncio.CancelledError:
                pass
        try:
            # Получаем данные пользователя
            user = await self.get_user(self.user_id)
            data = json.loads(text_data)
            print(data)

            print(f"Получены данные от {user.login}:", data.keys())

            # Определяем тип действия и сообщение
            action_info = {
                'status_game':  ("status_game", f"Пользователь {user.login} Производит действия с сессией"),
                'question': ("question", f"Пользователь {user.login} Производит действия с вопросами")
            }

            # Ищем первое совпадение действия
            for key in action_info:
                print(key)
                if key in data.keys():
                    action_type, log_message = action_info[key]
                    # log_message = action_info[key]
                    message = data[key]
                    print(log_message + " " + str(message))
                    break
            else:
                print("Неизвестный тип действия")
                await self.send(text_data=json.dumps({
                    'error': 'Unknown action type',
                    'received_data': data
                }))
                return

            # Если на вход поступил вопрос:
            if action_type == "question":
                if self.question[data[action_type]]:
                    self.question[data[action_type]]["frostbite"] = False
                else:
                    self.question[data[action_type]]["frostbite"] = True
                print(self.question)


                group_message = {
                    'type': 'handle_action_question',  # Важно: должно соответствовать имени метода
                    'action_type': action_type,
                    'message': message,
                    'username': user.login,
                    'user_id': self.user_id,
                    'timestamp': str(datetime.now())
                }


            elif action_type == "status_game":
                # question_tasks = {"stage": "collecting", "condition": "expectation"}
                if data[action_type] == "start":
                    group_message = {
                        'type': 'handle_action_game',  # Важно: должно соответствовать имени метода
                        'action_type': "start_timer",
                        'message': self.time,
                        'username': user.login,
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }
                    task = asyncio.create_task(timer_5_sec())
                    self.room_tasks[self.room_id] = task


                elif data[action_type] == "cancellation":
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()
                elif data[action_type] == "play":
                    self.stage["condition"] = "play"
                elif data[action_type] == "pause":
                    self.stage["condition"] = "pause"


                # Формируем сообщение для рассылки
                # group_message = {
                #     'type': 'handle_action_game',  # Важно: должно соответствовать имени метода
                #     'action_type': action_type,
                #     'message': message,
                #     'username': user.login,
                #     'user_id': self.user_id,
                #     'timestamp': str(datetime.now())
                # }


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


    async def notify_stage(self):
        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': self.stage["stage"],
            'condition': self.stage["condition"],
        }))

    # async def send_start_timer(self,n):
    #     await self.send(text_data=json.dumps({
    #         'type' : 'status_room',
    #         'status' : "start_timer",
    #         'time' : n,
    #     }))

    # stage = {"stage":"collecting", "condition":"expectation"}
    # async def notify_stage(self):
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'send_status_room',
    #             'stage': self.stage["stage"],
    #             'condition': self.stage["condition"],
    #         }
    #     )
    #
    # async def send_status_room(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'status_room',
    #         'stage': event['stage'],
    #         'condition': event["condition"],
    #     }))


    async def handle_action_question(self, event):
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

    async def handle_action_game(self, event):
        """Обработчик для action-сообщений"""
        try:
            response = {
                'type': event.get('action_type'),
                'message': event.get('message'),
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

    @database_sync_to_async
    def get_room(self, room_id):
        return game_rooms.objects.get(ID=room_id)

