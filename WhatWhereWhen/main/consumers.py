from datetime import datetime
from http.client import responses

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

            if data['comands'] == "out":
                    await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "redirect_user",
                        "target_user_id": data['user'],
                    }
                )
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
                await asyncio.sleep(1)  # ждем 10 секунд
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

    async def redirect_user(self, event):
        if event["target_user_id"] == self.user_id:
            await self.send(text_data=json.dumps({
                "type": "redirect",
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
            if data['comands'] == "out":
                try:
                    if data["user"] in room.people_on_page.get("users", []):
                        room.people_on_page["users"].remove(data["user"])
                        room.save()

                        first_player = Users.objects.get(ID=room.people_on_page["users"][0])
                        if room.host.ID == data["user"]:
                            room.host = first_player
                            room.save()
                        if room.leader.ID == data["user"]:
                            room.leader = None
                            room.save()
                        if room.captain.ID == data["user"]:
                            room.captain = None
                            room.save()

                except Exception as e:
                    print(f"Error removing user: {e}")

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


from django.core.cache import cache
import traceback


class StartConsumer(AsyncWebsocketConsumer):
    time = 1
    # переношу в кэш
    # question = {}
    stage = {"stage":"collecting", "condition":"expectation", "message":None, "user_id": None}
    room_tasks = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].ID
        self.room_group_name = f'action_{self.room_id}'

        # Генерируем ключ для кеша
        self.cache_key = f'room_{self.room_id}_questions'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # print(self.question)

        # Получаем вопросы из кеша
        questions = cache.get(self.cache_key)
        print(questions)
        # Используем асинхронную версию cache.get()
        # questions = await self.cache_get(self.cache_key)

        if questions is None:
            room = await self.get_room(self.room_id)
            await self.filling_question(room)

        print('self.stage["stage"]', self.stage["stage"])
        print('self.stage["user_id"] == self.user_id', self.stage["user_id"] == self.user_id)

        if self.stage["stage"] == "get_question":
            if self.stage["user_id"] == self.user_id:
                await self.notify_stage()
            else:
                room = await self.get_room(self.room_id)
                await self.notify_stage_not_leader(room)
        else:
            await self.notify_stage()

        # Проверяем, заполнилась ли комната
        # await self.check_room_and_start()

    # Вызывается при закрытии WebSocket соединения.
    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        room = await self.get_room(self.room_id)
        leader_id = await self.get_your_id(room, "leader")
        # Получаем вопросы из кеша
        questions = cache.get(self.cache_key)
        # Используем асинхронную версию cache.get()
        # questions = await self.cache_get(self.cache_key)

        if questions is None:
            room = await self.get_room(self.room_id)
            await self.filling_question(room)
            #

            questions = cache.get(self.cache_key)

        async def send_question_meny():
            arr = {
                "all": [],
                "use": [],
                "not_use": [],
            }

            for question_id, question_data in questions.items():
                if question_data["frostbite"]:
                    print(question_id)
                    arr["all"].append(question_id)
                    if question_data["use"]:
                        arr["use"].append(question_id)
                    else:
                        arr["not_use"].append(question_id)
            self.stage["stage"] = "question_menu"
            self.stage["message"] = arr
            self.stage["user_id"] = leader_id
            # print("self.stage",self.stage)

            group_message = {
                'type': 'handle_action_game',
                'action_type': "question_menu",
                'message': arr,
                'user_id': leader_id,
                'timestamp': str(datetime.now())
            }
            return group_message


        async def timer_5_sec(leader_id):
            try:
                # await self.send_start_timer(self.time)
                for i in range(self.time,0,-1):
                    await asyncio.sleep(1)
                    print(f"Обратный отсчет {i} секунда")
                await asyncio.sleep(1)
                print("0 секунд")
                print("start")

                # print("room.random_order", room.random_order)
                if room.random_order:
                    group_message = {
                        'type': 'handle_action_game',
                        'action_type': "question",
                        'message': self.time,
                        # 'username': user.login,
                        'user_id': leader_id,
                        'timestamp': str(datetime.now())
                    }
                else:
                    group_message = await send_question_meny()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    group_message
                )

            except asyncio.CancelledError:
                pass
            except Exception as e:
                print("Произошла ошибка:")
                traceback.print_exc()
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
                if key in data.keys():
                    action_type, log_message = action_info[key]
                    # log_message = action_info[key]
                    message = data[key]
                    # print(log_message + " " + str(message))
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
                if data["type"] == "open_question":
                    questions_number =  int(data["question"])

                    # уже существуе
                    # questions = cache.get(self.cache_key)
                    question = questions.pop(questions_number, None)
                    # Проверяем, что вопрос существует
                    if question is not None:
                        # Обновляем значение
                        question["use"] = True

                        # Добавляем вопрос обратно в список
                        questions[questions_number] = question

                        sorted_questions = sorted(questions.items())

                        # Преобразование обратно в словарь
                        questions = dict(sorted_questions)

                        # questions = sorted(questions)
                        # questions.insert(questions_number, question)

                        # Сохраняем обновленный список в кэш
                        cache.set(self.cache_key, questions, timeout=3600)
                    # cache.set(self.cache_key, questions_dict, timeout=3600)

                    self.stage["stage"] = "get_question"
                    self.stage["message"] = {
                        'question_name': question["question_name"],
                        'text_question': question["text_question"],
                        'note': question["note"],
                        'answer': question["answer"],
                        'answer_description': question["answer_description"],
                        'question_number': question["question_number"],
                    }
                    self.stage["user_id"] = leader_id

                    group_message = {
                        'type': 'sending_question',
                        'question_name': question["question_name"],
                        'text_question': question["text_question"],
                        'note': question["note"],
                        'answer': question["answer"],
                        'answer_description': question["answer_description"],
                        'lider_id': leader_id,
                        'question_number': question["question_number"],
                    }
                elif data["type"] == "get_menu":
                    group_message = await send_question_meny()

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )
                elif data["type"] == "delete":
                    question_id = data[action_type]
                    if question_id in questions:
                        questions[question_id]["frostbite"] = not questions[question_id]["frostbite"]

                        # Сохраняем обновленные вопросы обратно в кеш
                        cache.set(self.cache_key, questions, timeout=3600)
                        # await self.cache_set(self.cache_key, questions, timeout=3600)

                    group_message = {
                        'type': 'handle_action_question',  # Важно: должно соответствовать имени метода
                        'action_type': action_type,
                        'message': message,
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
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }
                    task = asyncio.create_task(timer_5_sec(leader_id))
                    self.room_tasks[self.room_id] = task

                elif data[action_type] == "cancellation":
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()

                    group_message = {
                        'type': 'handle_action_game',  # Важно: должно соответствовать имени метода
                        'action_type': "cancellation",
                        'message': None,
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }

                elif data[action_type] == "play":
                    self.stage["condition"] = "play"
                elif data[action_type] == "pause":
                    self.stage["condition"] = "pause"

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
            print("Произошла ошибка:")
            traceback.print_exc()
            error_msg = f"Ошибка обработки сообщения: {str(e)}"
            print(error_msg)
            await self.send(text_data=json.dumps({
                'error': error_msg,
                'details': str(e)
            }))

    @sync_to_async
    def filling_question(self, room):
        from questions.models import Question
        questions_bd = Question.objects.filter(Question_Select__selection_id=room.selections.ID)
        # print(questions)

        questions_dict = {}
        i=0
        for question in questions_bd:
            i+=1
            questions_dict[question.ID] = {
                "question_name": question.question_name,
                "text_question": question.text_question,
                "note": question.note,
                "answer": question.answer,
                "answer_description": question.answer_description,
                "license_id": question.license_id.ID,
                "frostbite": True,
                "question_number": i,
                'use': False,
            }

        # Сохраняем вопросы в кеш
        sorted_questions = sorted(questions_dict.items())

        # Преобразование обратно в словарь
        questions_dict = dict(sorted_questions)

        # Вывод отсортированного результата
        print(questions_dict)

        cache.set(self.cache_key, questions_dict, timeout=3600)
        # self.cache_set(self.cache_key, questions_dict, timeout=3600)

    async def notify_stage(self):
        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': self.stage["stage"],
            'condition': self.stage["condition"],
            'message': self.stage["message"],
            'user_id': self.stage["user_id"],
        }))


    async def notify_stage_not_leader(self,room):
        question = {
                'question_name': self.stage["message"]["question_name"],
                'text_question': self.stage["message"]["text_question"],
                'note': None,
                'answer': None,
                'answer_description': None,
                'question_number': self.stage["message"]["question_number"],
            }

        if not room.show_question:
            question['text_question'] = None


        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': self.stage["stage"],
            'condition': self.stage["condition"],
            'message': question,
            'user_id': self.stage["user_id"],
        }))

    async def sending_question(self,event):
        room = await self.get_room(self.room_id)
        try:
            if event["lider_id"] == self.user_id:
                response = {
                    'type': "get_question",
                    'question_name': event.get('question_name'),
                    'text_question': event.get('text_question'),
                    'note': event.get('note'),
                    'answer': event.get('answer'),
                    'answer_description': event.get('answer_description'),
                    'user_id': event["lider_id"],
                    'question_number': event.get('question_number'),
                }
            elif room.show_question:
                response = {
                    'type': "get_question",
                    'question_name': event.get('question_name'),
                    'text_question': event.get('text_question'),
                    'note': None,
                    'answer': None,
                    'answer_description': None,
                    'user_id': event["lider_id"],
                    'question_number': event.get('question_number'),
                }
            else:
                response = {
                    'type': "get_question",
                    'question_name': None,
                    'text_question': None,
                    'note': None,
                    'answer': None,
                    'answer_description': None,
                    'user_id': event["lider_id"],
                    'question_number': event.get('question_number'),
                }
            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            print("Произошла ошибка:")
            traceback.print_exc()

    async def handle_action_question(self, event):
        """Обработчик для action-сообщений"""
        try:
            response = {
                'type': event.get('action_type', 'unknown_action'),
                'message': event.get('message', ''),
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

    @sync_to_async
    def get_your_id(self, room, type):
        if type == "host":
            return room.host.ID
        elif type == "captain":
            return room.captain.ID
        elif type == "leader":
            return room.leader.ID