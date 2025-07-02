from datetime import datetime
from http.client import responses

from channels.generic.websocket import AsyncWebsocketConsumer
# from registration.models import Users
# from .models import ChatMessage, game_rooms
from channels.db import database_sync_to_async
import asyncio
from django.core.exceptions import ValidationError

# from ..questions.views import question, selection
from questions.views import question, selection

from WhatWhereWhen.wsgi import application


class ChatConsumer(AsyncWebsocketConsumer):
    # Вызывается при установке WebSocket соединения.
    async def connect(self):
        # Имя комнаты из URL (можно использовать для групповых чатов)
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].ID
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
        Class_out = ""

        if "У меня есть ответ" == message:
            Class_out += "answer_with_button "
        elif "ответ" in message.lower():
            Class_out += "answer_in_text "






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
                'class':Class_out,
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
        Class_out = str(event['class'])

        # print(Class_out)

        if user_id != self.user_id:
            Class_out += "messege_box_not_my"
        else:
            Class_out += "messege_box_my"

        # Отправляем сообщение WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'picture':picture,
            'user_id':user_id,
            'class_add': Class_out,
        }))


    # Вспомогательный метод для получения пользователя из БД.
    # Декоратор database_sync_to_async позволяет выполнять синхронные ORM запросы.
    @database_sync_to_async
    def get_user(self, user_id):
        from registration.models import Users
        return Users.objects.get(ID=user_id)

    @database_sync_to_async
    def get_room(self, room_id):
        from .models import game_rooms
        return game_rooms.objects.get(ID=room_id)

    # Вспомогательный метод для сохранения сообщения в БД.
    @database_sync_to_async
    def save_message(self, room, user, message):
        from .models import ChatMessage
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
                await asyncio.sleep(3)  # ждем 3 секунды
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

                #Раскомитить когда завершу отладку вернутся
                if len(room.people_on_page["users"]) ==0:
                    room.delete()

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
    time_waiting = 60
    time = 5
    # переношу в кэш
    # question = {}
    stage = {"stage":"collecting", "condition":"expectation", "message":None, "user_id": None, "score": None, "captain_id": None}
    room_tasks = {}
    # timer_Nsec_tasks = {}
    check_like = 0

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].ID
        self.room_group_name = f'action_{self.room_id}'
        room = await self.get_room(self.room_id)
        self.leader_id = await self.get_your_id(room, "leader")

        # NEW: Генерируем ключ для кеша состояния игры (stage)
        self.stage_cache_key = f'room_{self.room_id}_stage'
        self.cache_key = f'room_{self.room_id}_questions'

        # Получаем состояние игры из кэша
        stage = await self._stage_get()
        if stage is None:
            stage = {
                "stage": "collecting",
                "condition": "expectation",
                "message": None,
                "user_id": None,
                "score": None,
                "captain_id": None,
            }

        # Инициализация score, если None
        if stage.get("score") is None:
            if room.game_mode == 0:
                stage["score"] = {
                    "players": 0,
                    "authors": 0,
                }
            elif room.game_mode == 1:
                stage["score"] = {
                    "players": {},
                    "authors": {},
                }
                for item in room.people_on_page.get("users", []):
                    if item != self.leader_id:
                        login_obj = await self.get_user(item)
                        login = login_obj.login
                        stage["score"]["players"][login] = 0
                        stage["score"]["authors"][login] = 0
            elif room.game_mode == 2:
                stage["score"] = {
                    "players": 0,
                    "authors": 0,
                }
            # Сохраняем инициализированный stage в кэш
            await self._stage_set(stage)

        # Добавляем канал в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Получаем вопросы из кэша
        questions = cache.get(self.cache_key)
        if questions is None:
            await self.filling_question(room)

        # Обновляем stage из кэша (на случай, если filling_question что-то поменял)
        stage = await self._stage_get()

        # Отправляем состояние клиенту в зависимости от состояния игры
        if stage["stage"] == "get_question":
            if stage["user_id"] == self.user_id:
                await self.notify_stage_with_stage(stage)
            else:
                await self.notify_stage_not_leader_with_stage(room, stage)
        else:
            await self.notify_stage_with_stage(stage)
    async def disconnect(self, close_code):
        # Удаляем канал из группы комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # При необходимости можно очистить состояние, если нужно
        # Например, если в комнате больше нет участников, можно удалить stage из кэша
        # Но это зависит от логики приложения и не обязательно здесь

    async def receive(self, text_data):
        room = await self.get_room(self.room_id)
        self.leader_id = await self.get_your_id(room, "leader")

        # Получаем stage из кеша
        stage = await self._stage_get()
        if stage is None:
            # На всякий случай инициализируем, если вдруг нет
            stage = {
                "stage": "collecting",
                "condition": "expectation",
                "message": None,
                "user_id": None,
                "score": None,
                "captain_id": None,
            }

        try:
            stage["captain_id"] = await self.get_your_id(room, "captain")
        except Exception as e:
            print("ошибка назначения капитана", e)

        questions = cache.get(self.cache_key)
        if questions is None:
            room = await self.get_room(self.room_id)
            await self.filling_question(room)
            questions = cache.get(self.cache_key)

        import random
        def get_random_unused_question_key(questions):
            unused_keys = [key for key, q in questions.items() if not q.get("use", False)]
            if not unused_keys:
                return False
            return random.choice(unused_keys)

        async def send_random():
            questions = cache.get(self.cache_key)
            check_random = get_random_unused_question_key(questions)
            if check_random != False:
                await self.send(text_data=json.dumps({
                    'type': 'random_question',
                    'question_number': check_random,
                }))
                stage["stage"] = "random_question"
                stage["message"] = check_random
                await self._stage_set(stage)
            else:
                print("Вопросы кончились")

        async def send_question_meny():
            arr = {
                "all": [],
                "use": [],
                "not_use": [],
                "right": [],
            }

            for question_id, question_data in questions.items():
                if question_data["frostbite"]:
                    arr["all"].append(question_id)
                    if question_data["use"]:
                        arr["use"].append(question_id)
                    else:
                        arr["not_use"].append(question_id)
                    if question_data["answer_status"]["status"]:
                        arr["right"].append(question_id)

            stage["stage"] = "question_menu"
            stage["message"] = arr
            stage["user_id"] = self.leader_id
            await self._stage_set(stage)

            group_message = {
                'type': 'handle_action_game',
                'action_type': "question_menu",
                'message': arr,
                'user_id': self.leader_id,
                'timestamp': str(datetime.now())
            }
            return group_message

        async def chek_timer_Nsec():
            for _ in range(self.time_waiting):
                await asyncio.sleep(1)

            group_message = {
                'type': 'send_skip',
                "message": "skip",
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                group_message
            )

        async def time_question():
            def time_send(time, Class, leader_id):
                group_message = {
                    'type': 'time_sender',
                    'time': time,
                    'Class': Class,
                    'leader_id': leader_id,
                }
                return group_message

            try:
                for i in range(stage["message"]["time_read"] - 1, -1, -1):
                    await asyncio.sleep(1)
                    stage["message"]['time_read'] = i
                    if i >= 0:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            time_send(stage["message"]['time_read'], "time_read", self.leader_id)
                        )
                if stage["message"]['time_read'] < 0:
                    stage["message"]['time_read'] = 0

                for i in range(stage["message"]["time_question"] - 1, -1, -1):
                    await asyncio.sleep(1)
                    stage["message"]['time_question'] = i
                    if i >= 0:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            time_send(stage["message"]['time_question'], "time_question", self.leader_id)
                        )
                if stage["message"]['time_question'] < 0:
                    stage["message"]['time_question'] = 0

                await self._stage_set(stage)
            except asyncio.CancelledError:
                pass
            except Exception:
                traceback.print_exc()

        async def timer_5_sec():
            try:
                for _ in range(self.time, 0, -1):
                    await asyncio.sleep(1)
                await asyncio.sleep(1)

                if room.random_order:
                    await send_random()
                else:
                    group_message = await send_question_meny()
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )
            except asyncio.CancelledError:
                pass
            except Exception:
                traceback.print_exc()

        try:
            user = await self.get_user(self.user_id)
            data = json.loads(text_data)
            print(f"Получены данные от {user.login}:", data)

            action_info = {
                'status_game': ("status_game", f"Пользователь {user.login} Производит действия с сессией"),
                'question': ("question", f"Пользователь {user.login} Производит действия с вопросами")
            }

            for key in action_info:
                if key in data.keys():
                    action_type, log_message = action_info[key]
                    message = data[key]
                    break
            else:
                print("Неизвестный тип действия")
                await self.send(text_data=json.dumps({
                    'error': 'Unknown action type',
                    'received_data': data
                }))
                return

            # --- Обработка action_type == "question" ---
            if action_type == "question":
                if data["type"] == "open_question":
                    questions = cache.get(self.cache_key)
                    questions_number = int(data["question"])
                    question = questions.pop(questions_number, None)
                    if question is not None:
                        question["use"] = True
                        questions[questions_number] = question
                        questions = dict(sorted(questions.items()))
                        cache.set(self.cache_key, questions, timeout=3600)

                        stage["stage"] = "get_question"
                        stage["message"] = {
                            'question_id': question["question_id"],
                            'question_name': question["question_name"],
                            'text_question': question["text_question"],
                            'note': question["note"],
                            'answer': question["answer"],
                            'answer_description': question["answer_description"],
                            'question_number': question["question_number"],
                            'time_read': (len(question["text_question"]) // room.reading_speed) + 1,
                            'time_question': room.question_time,
                        }
                        stage["user_id"] = self.leader_id
                        await self._stage_set(stage)

                        group_message = {
                            'type': 'sending_question',
                            'question_id': question["question_id"],
                            'question_name': question["question_name"],
                            'text_question': question["text_question"],
                            'note': question["note"],
                            'answer': question["answer"],
                            'answer_description': question["answer_description"],
                            'leader_id': self.leader_id,
                            'question_number': question["question_number"],
                            'time_read': (len(question["text_question"]) // room.reading_speed) + 1,
                            'time_question': room.question_time,
                        }

                        task = asyncio.create_task(time_question())
                        self.room_tasks[self.room_id] = task

                elif data["type"] == "captain_chose_your":
                    stage["message"]["your_response"] = data["question"]
                    await self._stage_set(stage)

                    group_message = {
                        'type': 'ready_respond_users',
                        'user_id': data["question"]
                    }
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )

                elif data["type"] in ("answer", "early_response"):
                    if room.game_mode == 0:
                        stage["message"]["your_response"] = None
                    elif room.game_mode in (1, 2):
                        try:
                            stage["message"]["your_response"][data["author_answer"]] = False
                        except Exception:
                            stage["message"]["your_response"] = {data["author_answer"]: False}

                    login_obj = await self.get_user(data["author_answer"])
                    login = login_obj.login

                    early_response = (data["type"] == "early_response")
                    author_answer = login
                    author_answer_id = data["author_answer"]
                    answer = data["answer"]
                    description = data["description"]
                    Class_answer = "user_provide_answer" if answer else "user_not_provide_answer"
                    if not answer:
                        answer = "Пользователь не дал ответ"
                    Class_description = "user_provide_description" if description else "user_not_provide_description"
                    if not description:
                        description = "Пользователь не дал описания вопроса"

                    group_message = {
                        'type': 'returned_answer',
                        'game_mode': room.game_mode,
                        "leader_id": self.leader_id,
                        "captain_id": stage.get("captain_id"),
                        "author_answer": author_answer,
                        "author_answer_id": author_answer_id,
                        "early_response": early_response,
                        'answer': answer,
                        'description': description,
                        'Class_answer': Class_answer,
                        'Class_description': Class_description,
                    }
                    if room.game_mode == 2:
                        group_message['whom'] = "captain"

                    if room.game_mode == 0:
                        stage["message"]["get_answer"] = group_message
                    else:
                        try:
                            stage["message"]["get_answer"].append(group_message)
                        except Exception:
                            stage["message"]["get_answer"] = [group_message]

                    await self._stage_set(stage)

                elif data["type"] == "get_menu":
                    if self.room_tasks:
                        task = self.room_tasks.pop(self.room_id, None)
                        if task:
                            task.cancel()

                        questions = cache.get(self.cache_key)
                        for question_id, question_data in questions.items():
                            if question_data["frostbite"]:
                                question_data["time_read"] = (len(
                                    question_data["text_question"]) // room.reading_speed) + 1
                                question_data["time_question"] = room.question_time
                        cache.set(self.cache_key, questions, timeout=3600)

                    group_message = await send_question_meny()
                    await self.channel_layer.group_send(self.room_group_name, group_message)

                elif data["type"] == "random_question":
                    self.check_like = 0
                    if self.room_tasks:
                        task = self.room_tasks.pop(self.room_id, None)
                        if task:
                            task.cancel()
                    await send_random()

                elif data["type"] == "delete":
                    question_id = data[action_type]
                    if question_id in questions:
                        questions[question_id]["frostbite"] = not questions[question_id]["frostbite"]
                        cache.set(self.cache_key, questions, timeout=3600)

                    group_message = {
                        'type': 'handle_action_question',
                        'action_type': action_type,
                        'message': message,
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }

            # --- Обработка action_type == "status_game" ---
            elif action_type == "status_game":
                if data[action_type] == "start":
                    if len(room.people_on_page["users"]) >= 3 and room.leader is not None and room.captain is not None:
                        room.room_limit = len(room.people_on_page["users"])
                        await self.update_room(room, len(room.people_on_page["users"]))

                        group_message = {
                            'type': 'handle_action_game',
                            'action_type': "start_timer",
                            'message': self.time,
                            'user_id': self.user_id,
                            'timestamp': str(datetime.now())
                        }
                        task = asyncio.create_task(timer_5_sec())
                        self.room_tasks[self.room_id] = task
                    else:
                        print("Ошибка запуска")

                elif data[action_type] == "cancellation":
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()

                    group_message = {
                        'type': 'handle_action_game',
                        'action_type': "cancellation",
                        'message': None,
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }

                elif data[action_type] == "play":
                    stage["condition"] = "play"
                    await self._stage_set(stage)
                    task = asyncio.create_task(time_question())
                    self.room_tasks[self.room_id] = task

                elif data[action_type] == "pause":
                    stage["condition"] = "pause"
                    await self._stage_set(stage)
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()

                elif data[action_type] == "pluse":
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()

                        if stage["message"]["time_read"] > 0:
                            if stage["message"]["time_read"] + data["value"] >= 0:
                                stage["message"]["time_read"] += data["value"]
                            else:
                                stage["message"]["time_read"] = 1
                        elif stage["message"]["time_question"] > 0:
                            if stage["message"]["time_question"] + data["value"] >= 0:
                                stage["message"]["time_question"] += data["value"]
                            else:
                                stage["message"]["time_question"] = 1

                        await self._stage_set(stage)
                        task = asyncio.create_task(time_question())
                        self.room_tasks[self.room_id] = task

                    else:
                        if stage["message"]["time_read"] > 0:
                            if stage["message"]["time_read"] + data["value"] >= 0:
                                stage["message"]["time_read"] += data["value"]
                            else:
                                stage["message"]["time_read"] = 0

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': stage["message"]["time_read"],
                                    'Class': "time_read",
                                }
                            )
                        elif stage["message"]["time_question"] > 0:
                            if stage["message"]["time_question"] + data["value"] >= 0:
                                stage["message"]["time_question"] += data["value"]
                            else:
                                stage["message"]["time_question"] = 0

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': stage["message"]["time_question"],
                                    'Class': "time_question",
                                }
                            )
                        await self._stage_set(stage)

                elif data[action_type] in ("like", "dislike"):
                    status = ""
                    Class = ""
                    if room.game_mode == 0:
                        if data[action_type] == "like":
                            stage["score"]["players"] += 1
                            status = "Ответ верный"
                            Class = "correct"
                        if data[action_type] == "dislike":
                            stage["score"]["authors"] += 1
                            status = "Ответ не верный"
                            Class = "wrong"

                        if Class == "correct":
                            questions = cache.get(self.cache_key)
                            question = questions.pop(data["question_number"], None)
                            if question is not None:
                                question["answer_status"] = {
                                    "status": True,
                                    "user": data["author_answer"],
                                }
                                questions[data["question_number"]] = question
                                questions = dict(sorted(questions.items()))
                                cache.set(self.cache_key, questions, timeout=3600)

                    elif room.game_mode == 1:
                        self.check_like += 1
                        stage["message"]["your_response"][data["author_answer"]] = True

                        login_obj = await self.get_user(data["author_answer"])
                        login = login_obj.login
                        if data[action_type] == "like":
                            stage["score"]["players"][login] += 1
                            status = "Ответ верный"
                            Class = "correct"
                        if data[action_type] == "dislike":
                            stage["score"]["authors"][login] += 1
                            status = "Ответ не верный"
                            Class = "wrong"

                        if Class == "correct":
                            questions = cache.get(self.cache_key)
                            question = questions.pop(data["question_number"], None)
                            if question is not None:
                                question["answer_status"]["status"] = True
                                try:
                                    question["answer_status"]["user"].append(data["author_answer"])
                                except Exception:
                                    question["answer_status"]["user"] = [data["author_answer"]]
                                questions[data["question_number"]] = question
                                questions = dict(sorted(questions.items()))
                                cache.set(self.cache_key, questions, timeout=3600)

                    elif room.game_mode == 2:
                        if data['type'] == "captain":
                            group_message = {
                                'type': 'returned_answer',
                                'game_mode': 2,
                                "leader_id": self.leader_id,
                                "captain_id": stage.get("captain_id"),
                                "author_answer": data['author_answer'],
                                "author_answer_id": data['author_answer_id'],
                                'answer': data['answer'],
                                'description': data['description'],
                                'Class_answer': data['Class_answer'],
                                'Class_description': data['Class_description'],
                                'whom': "leader",
                            }
                            stage["message"]["get_answer"] = group_message
                        elif data['type'] == "leader":
                            if data[action_type] == "like":
                                stage["score"]["players"] += 1
                                status = "Ответ верный"
                                Class = "correct"
                            if data[action_type] == "dislike":
                                stage["score"]["authors"] += 1
                                status = "Ответ не верный"
                                Class = "wrong"

                            if Class == "correct":
                                questions = cache.get(self.cache_key)
                                question = questions.pop(data["question_number"], None)
                                if question is not None:
                                    question["answer_status"] = {
                                        "status": True,
                                        "user": data["author_answer"],
                                    }
                                    questions[data["question_number"]] = question
                                    questions = dict(sorted(questions.items()))
                                    cache.set(self.cache_key, questions, timeout=3600)

                    await self._stage_set(stage)

                    if room.game_mode != 2 or (room.game_mode == 2 and data['type'] == "leader"):
                        group_message_score = {
                            'type': 'score_send',
                            "score_players": stage["score"]["players"],
                            "score_authors": stage["score"]["authors"],
                            "status": status,
                            "Class": Class,
                            "leader_id": self.leader_id,
                        }
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            group_message_score
                        )

                    # Логика перехода к следующему вопросу и паузы с таймерами
                    if room.game_mode == 0:
                        if room.random_order:
                            for i in range(room.break_between_questions):
                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    {
                                        'type': 'time_sender',
                                        'time': room.break_between_questions - i,
                                        'Class': "break_between_questions",
                                    }
                                )
                                await asyncio.sleep(1)
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': 0,
                                    'Class': "break_between_questions",
                                }
                            )
                            await send_random()
                        else:
                            if self.room_tasks:
                                task = self.room_tasks.pop(self.room_id, None)
                                if task:
                                    task.cancel()

                                questions = cache.get(self.cache_key)
                                for question_id, question_data in questions.items():
                                    if question_data["frostbite"]:
                                        question_data["time_read"] = (len(
                                            question_data["text_question"]) // room.reading_speed) + 1
                                        question_data["time_question"] = room.question_time
                                cache.set(self.cache_key, questions, timeout=3600)

                            group_message_2 = await send_question_meny()
                            await self.channel_layer.group_send(self.room_group_name, group_message_2)

                    elif room.game_mode == 1:
                        if self.check_like == len(room.people_on_page.get("users", [])) - 1:
                            self.check_like = 0
                            if room.random_order:
                                for i in range(room.break_between_questions):
                                    await self.channel_layer.group_send(
                                        self.room_group_name,
                                        {
                                            'type': 'time_sender',
                                            'time': room.break_between_questions - i,
                                            'Class': "break_between_questions",
                                        }
                                    )
                                    await asyncio.sleep(1)
                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    {
                                        'type': 'time_sender',
                                        'time': 0,
                                        'Class': "break_between_questions",
                                    }
                                )
                                await send_random()
                            else:
                                if self.room_tasks:
                                    task = self.room_tasks.pop(self.room_id, None)
                                    if task:
                                        task.cancel()

                                    questions = cache.get(self.cache_key)
                                    for question_id, question_data in questions.items():
                                        if question_data["frostbite"]:
                                            question_data["time_read"] = (len(
                                                question_data["text_question"]) // room.reading_speed) + 1
                                            question_data["time_question"] = room.question_time
                                    cache.set(self.cache_key, questions, timeout=3600)

                                group_message_2 = await send_question_meny()
                                await self.channel_layer.group_send(self.room_group_name, group_message_2)

                    elif room.game_mode == 2 and data['type'] == "leader":
                        if room.random_order:
                            for i in range(room.break_between_questions):
                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    {
                                        'type': 'time_sender',
                                        'time': room.break_between_questions - i,
                                        'Class': "break_between_questions",
                                    }
                                )
                                await asyncio.sleep(1)
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': 0,
                                    'Class': "break_between_questions",
                                }
                            )
                            await send_random()
                        else:
                            if self.room_tasks:
                                task = self.room_tasks.pop(self.room_id, None)
                                if task:
                                    task.cancel()

                                questions = cache.get(self.cache_key)
                                for question_id, question_data in questions.items():
                                    if question_data["frostbite"]:
                                        question_data["time_read"] = (len(
                                            question_data["text_question"]) // room.reading_speed) + 1
                                        question_data["time_question"] = room.question_time
                                cache.set(self.cache_key, questions, timeout=3600)

                            group_message_2 = await send_question_meny()
                            await self.channel_layer.group_send(self.room_group_name, group_message_2)

            # Отправляем в группу, если group_message определён
            try:
                if 'group_message' in locals():
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )
            except Exception as e:
                if str(e) != "cannot access local variable 'group_message' where it is not associated with a value":
                    print(e)

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

    from asgiref.sync import sync_to_async, database_sync_to_async
    from django.core.cache import cache
    import json
    import traceback
    from datetime import datetime

    @sync_to_async
    def filling_question(self, room):
        from questions.models import Question
        questions_bd = Question.objects.filter(Question_Select__selection_id=room.selections.ID)

        questions_dict = {}
        for i, question in enumerate(questions_bd, start=1):
            questions_dict[question.ID] = {
                "question_id": question.ID,
                "question_name": question.question_name,
                "text_question": question.text_question,
                "note": question.note,
                "answer": question.answer,
                "answer_description": question.answer_description,
                "license_id": question.license_id.ID if question.license_id else None,
                "frostbite": True,
                "question_number": i,
                'use': False,
                'time_read': (len(question.text_question) // room.reading_speed) + 1 if room.reading_speed else 1,
                'time_question': room.question_time,
                'answer_status': {
                    "status": False,
                    "user": None,
                },
            }

        # Сортируем по ключу (question ID)
        sorted_questions = dict(sorted(questions_dict.items()))
        cache.set(self.cache_key, sorted_questions, timeout=3600)

    async def notify_stage(self):
        # self.stage должна быть локальной переменной, полученной из кеша
        stage = await self._stage_get()
        if not stage:
            return
        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': stage.get("stage"),
            'condition': stage.get("condition"),
            'message': stage.get("message"),
            'user_id': stage.get("user_id"),
            'captain_id': stage.get("captain_id"),
            'score': stage.get("score"),
        }))

    async def send_skip(self, event):
        if getattr(self, 'leader_id', None) == getattr(self, 'user_id', None):
            await self.send(text_data=json.dumps({
                'type': "skip",
            }))

    async def time_sender(self, event):
        try:
            stage = await self._stage_get()
            response = {
                'type': "time",
                'time': event.get('time'),
                "Class": event.get('Class'),
                "leader_id": event.get('leader_id'),
                "captain_id": stage.get("captain_id") if stage else None
            }
            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения time_sender: {e}")

    async def notify_stage_not_leader(self, room):
        stage = await self._stage_get()
        if not stage:
            return

        try:
            message = stage.get("message", {})
            question = {
                'question_id': message.get("question_id"),
                'question_name': message.get("question_name"),
                'text_question': message.get("text_question"),
                'note': None,
                'answer': None,
                'answer_description': None,
                'question_number': message.get("question_number"),
                'time_read': message.get("time_read"),
                'time_question': message.get("time_question"),
                'your_response': message.get("your_response", None),
            }
        except Exception as e:
            question = {
                'question_id': stage.get("message", {}).get("question_id"),
                'question_name': stage.get("message", {}).get("question_name"),
                'text_question': stage.get("message", {}).get("text_question"),
                'note': None,
                'answer': None,
                'answer_description': None,
                'question_number': stage.get("message", {}).get("question_number"),
                'time_read': stage.get("message", {}).get("time_read"),
                'time_question': stage.get("message", {}).get("time_question"),
                'your_response': None,
            }
            print("Произошла ошибка в notify_stage_not_leader:", e)
            traceback.print_exc()

        if not room.show_question:
            question['text_question'] = None

        if room.game_mode == 2:
            try:
                get_answer = stage.get("message", {}).get("get_answer")
                if isinstance(get_answer, list) and self.user_id == stage.get("captain_id"):
                    question["get_answer"] = get_answer
                else:
                    question["get_answer"] = None
            except Exception as e:
                print("Ошибка в notify_stage_not_leader при получении get_answer:", e)
                question["get_answer"] = None

        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': stage.get("stage"),
            'condition': stage.get("condition"),
            'message': question,
            'user_id': stage.get("user_id"),
            'score': stage.get("score"),
            'captain_id': stage.get("captain_id"),
        }))

    async def score_send(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': "score",
                'score_players': event.get('score_players'),
                'score_authors': event.get('score_authors'),
                'status': event.get('status'),
                'Class': event.get('Class'),
                'leader_id': getattr(self, 'leader_id', None),
            }))
        except Exception as e:
            print(f"Ошибка отправки сообщения score_send: {e}")

    async def returned_answer(self, event):
        try:
            game_mode = event.get("game_mode")
            if game_mode != 2:
                if event.get("leader_id") == getattr(self, 'user_id', None):
                    response = {
                        'type': "return_answer",
                        "early_response": event.get('early_response'),
                        "answer": event.get('answer'),
                        "description": event.get('description'),
                        "Class_answer": event.get('Class_answer'),
                        "Class_description": event.get('Class_description'),
                        "author_answer": event.get('author_answer'),
                        "author_answer_id": event.get('author_answer_id'),
                    }
                    await self.send(text_data=json.dumps(response))
            else:  # game_mode == 2
                if event.get("captain_id") == getattr(self, 'user_id', None) and event.get("whom") == "captain":
                    response = {
                        'type': "return_answer",
                        "early_response": event.get('early_response'),
                        "answer": event.get('answer'),
                        "description": event.get('description'),
                        "Class_answer": event.get('Class_answer'),
                        "Class_description": event.get('Class_description'),
                        "author_answer": event.get('author_answer'),
                        "author_answer_id": event.get('author_answer_id'),
                        "captain_id": event.get('captain_id'),
                        "whom": event.get('whom'),
                    }
                    await self.send(text_data=json.dumps(response))
                elif event.get("leader_id") == getattr(self, 'user_id', None) and event.get("whom") == "leader":
                    response = {
                        'type': "return_answer",
                        "early_response": event.get('early_response'),
                        "answer": event.get('answer'),
                        "description": event.get('description'),
                        "Class_answer": event.get('Class_answer'),
                        "Class_description": event.get('Class_description'),
                        "author_answer": event.get('author_answer'),
                        "author_answer_id": event.get('author_answer_id'),
                        "whom": event.get('whom'),
                    }
                    await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка в returned_answer: {e}")
            traceback.print_exc()

    async def ready_respond_users(self, event):
        if event.get("user_id") == getattr(self, 'user_id', None):
            await self.send(text_data=json.dumps({'type': 'return'}))

    async def sending_question(self, event):
        try:
            room = await self.get_room(self.room_id)
            await self.delete_all_messages_in_room(self.room_id)

            leader_id = event.get("leader_id")
            question_name = event.get('question_name')
            text_question = event.get('text_question')
            note = event.get('note')
            answer = event.get('answer')
            answer_description = event.get('answer_description')
            question_number = event.get('question_number')
            time_read = event.get('time_read')
            time_question = event.get('time_question')

            if leader_id == getattr(self, 'user_id', None):
                response = {
                    'type': "get_question",
                    'question_id': event.get('question_id'),
                    'question_name': question_name,
                    'text_question': text_question,
                    'note': note,
                    'answer': answer,
                    'answer_description': answer_description,
                    'user_id': leader_id,
                    'question_number': question_number,
                    'time_read': time_read,
                    'time_question': time_question,
                }
            elif room.show_question:
                response = {
                    'type': "get_question",
                    'question_id': event.get('question_id'),
                    'question_name': question_name,
                    'text_question': text_question,
                    'note': None,
                    'answer': None,
                    'answer_description': None,
                    'user_id': leader_id,
                    'question_number': question_number,
                    'time_read': time_read,
                    'time_question': time_question,
                }
            else:
                response = {
                    'type': "get_question",
                    'question_id': event.get('question_id'),
                    'question_name': None,
                    'text_question': None,
                    'note': None,
                    'answer': None,
                    'answer_description': None,
                    'user_id': leader_id,
                    'question_number': question_number,
                    'time_read': time_read,
                    'time_question': time_question,
                }
            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения sending_question: {e}")
            traceback.print_exc()

    async def handle_action_question(self, event):
        try:
            response = {
                'type': event.get('action_type', 'unknown_action'),
                'message': event.get('message', ''),
                'user_id': event.get('user_id', 0),
                'timestamp': event.get('timestamp', str(datetime.now()))
            }
            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения handle_action_question: {e}")

    async def handle_action_game(self, event):
        try:
            response = {
                'type': event.get('action_type'),
                'message': event.get('message'),
                'user_id': event.get('user_id', 0),
                'timestamp': event.get('timestamp', str(datetime.now()))
            }
            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения handle_action_game: {e}")

    @database_sync_to_async
    def get_user(self, user_id):
        from registration.models import Users
        return Users.objects.get(ID=user_id)

    @database_sync_to_async
    def get_room(self, room_id):
        from .models import game_rooms
        return game_rooms.objects.get(ID=room_id)

    @database_sync_to_async
    def delete_all_messages_in_room(self, room_id):
        from .models import ChatMessage
        ChatMessage.objects.filter(room__ID=room_id).delete()

    @sync_to_async
    def get_your_id(self, room, type_):
        if type_ == "host":
            return room.host.ID
        elif type_ == "captain":
            return room.captain.ID
        elif type_ == "leader":
            return room.leader.ID
        return None

    @sync_to_async
    def update_room(self, room, new_limit):
        room.room_limit = new_limit
        room.save()

    def _stage_cache_key(self):
        return f'room_{self.room_id}_stage'

    def _questions_cache_key(self):
        return f'room_{self.room_id}_questions'

    async def _stage_get(self):
        return await sync_to_async(cache.get)(self.stage_cache_key)

    async def _stage_set(self, stage):
        await sync_to_async(cache.set)(self.stage_cache_key, stage, timeout=3600)

