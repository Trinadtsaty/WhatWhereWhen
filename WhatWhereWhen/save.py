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
        # self.stage["captain_id"] = await self.get_your_id(room, "captain")



        # OLD: инициализация score в self.stage
        if self.stage["score"] == None:
            if room.game_mode == 0:
                self.stage["score"] ={
                    "players": 0,
                    "authors": 0,
                    }
            elif room.game_mode == 1:
                self.stage["score"] = {
                    "players": {},
                    "authors": {},
                }

                for item in room.people_on_page.get("users", []):
                    # login = await self.get_user(item)
                    # login = login.login
                    # self.stage["score"]["players"][login] = 0
                    if item != self.leader_id:
                        # print("создаём поле score берём пользователя с id: ", item)
                        login = await self.get_user(item)
                        login = login.login
                        # print("и ником: ", login)
                        self.stage["score"]["players"][login] = 0
                        self.stage["score"]["authors"][login] = 0

            elif room.game_mode == 2:
                self.stage["score"] = {
                        "players": 0,
                        "authors": 0,
                    }


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
        # print(questions)
        # Используем асинхронную версию cache.get()
        # questions = await self.cache_get(self.cache_key)

        if questions is None:
            await self.filling_question(room)

        if self.stage["stage"] == "get_question":
            if self.stage["user_id"] == self.user_id:
                await self.notify_stage()
            else:
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
        self.leader_id = await self.get_your_id(room, "leader")
        try:
            self.stage["captain_id"] = await self.get_your_id(room, "captain")
        except Exception as e:
            print("ошибка назначения капитана", e)

        # self.leader_id = await self.get_your_id(room, "leader")
        # Получаем вопросы из кеша
        questions = cache.get(self.cache_key)
        # Используем асинхронную версию cache.get()
        # questions = await self.cache_get(self.cache_key)

        if questions is None:
            room = await self.get_room(self.room_id)
            await self.filling_question(room)
            #

            questions = cache.get(self.cache_key)

        # def get_random_unused_question(questions):
        #     import random
        #     # Фильтруем те вопросы, у которых "use" == False
        #     unused = [q for q in questions.values() if not q.get("use", False)]
        #     if not unused:
        #         return False
        #     return random.choice(unused)

        def get_random_unused_question_key(questions):
            import random
            # Собираем ключи вопросов, у которых "use" == False
            unused_keys = [key for key, q in questions.items() if not q.get("use", False)]
            # print(unused_keys)
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
                self.stage["stage"] = "random_question"
                self.stage["message"] = check_random
            else:
                # заглушка для конца игры конец вернуться
                print("Вопросы кончились")
                pass

        async def send_question_meny():
            arr = {
                "all": [],
                "use": [],
                "not_use": [],
                "right ": [],
            }

            for question_id, question_data in questions.items():
                if question_data["frostbite"]:
                    # print(question_id)
                    arr["all"].append(question_id)
                    if question_data["use"]:
                        arr["use"].append(question_id)
                    else:
                        arr["not_use"].append(question_id)
                    if question_data["answer_status"]["status"]:
                        arr["right"].append(question_id)

            self.stage["stage"] = "question_menu"
            self.stage["message"] = arr
            self.stage["user_id"] = self.leader_id
            # print("self.stage",self.stage)

            group_message = {
                'type': 'handle_action_game',
                'action_type': "question_menu",
                'message': arr,
                'user_id': self.leader_id,
                'timestamp': str(datetime.now())
            }
            return group_message

        # Вернуться
        async def chek_timer_Nsec():
            for i in range(self.time_waiting):
                await asyncio.sleep(1)

            group_message = {
                'type': 'send_skip',
                "message": "skip",
                # "leader_id": self.leader_id,
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                group_message
            )


        async def time_question():
            # Вернуться
            def time_send(time, Class, leader_id):
                group_message = {
                'type': 'time_sender',
                'time': time,
                'Class': Class,
                'leader_id':leader_id,
                }
                return group_message


            try:

                for i in range(self.stage["message"]["time_read"]-1, -1, -1):
                    await asyncio.sleep(1)
                    self.stage["message"]['time_read'] = i
                    if i>=0:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            time_send(self.stage["message"]['time_read'], "time_read", self.leader_id)
                        )
                    # print(f"Обратный отсчет чтения вопроса: {i//60}:{i-i//60*60}")
                if self.stage["message"]['time_read'] < 0:
                    self.stage["message"]['time_read'] = 0

                for i in range(self.stage["message"]["time_question"]-1, -1, -1):
                    await asyncio.sleep(1)
                    self.stage["message"]['time_question'] = i
                    if i >= 0:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            time_send(self.stage["message"]['time_question'], "time_question", self.leader_id)
                        )

                    # print(f"Обратный отсчет ответа на вопрос: {i//60}:{i-i//60*60}")
                if self.stage["message"]['time_question'] < 0:
                    self.stage["message"]['time_question'] = 0

                # if self.timer_Nsec_tasks == {}:
                #     timer = asyncio.create_task(chek_timer_Nsec())
                    # self.timer_Nsec_tasks[self.room_id] = timer

                # print("Вопрос закончился")
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print("Произошла ошибка:")
                traceback.print_exc()

        async def timer_5_sec():
            try:
                # await self.send_start_timer(self.time)
                for i in range(self.time,0,-1):
                    await asyncio.sleep(1)
                    # print(f"Обратный отсчет {i} секунда")
                await asyncio.sleep(1)
                # print("0 секунд")
                # print("start")

                if room.random_order:
                    await send_random()

                    # questions = cache.get(self.cache_key)
                    # check_random = get_random_unused_question_key(questions)
                    #
                    # if check_random != False:
                    #     await self.send(text_data=json.dumps({
                    #         'type': 'random_question',
                    #         'question_number': check_random,
                    #     }))
                    #     self.stage["stage"] = "random_question"
                    #     self.stage["message"] = check_random
                    # else:
                    #     # заглушка для конца игры конец вернуться
                    #     print("Вопросы кончились")
                    #     pass

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
            # print(data)

            print(f"Получены данные от {user.login}:", data)

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

                    questions = cache.get(self.cache_key)
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
                    self.stage["user_id"] = self.leader_id

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
                    # print(data)
                    # print(self.stage["message"])
                    self.stage["message"]["your_response"] = data["question"]
                    # print(self.stage)

                    group_message = {
                        'type': 'ready_respond_users',
                        'user_id': data["question"]
                    }
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )

                elif data["type"] == "answer" or data["type"] == "early_response":
                    # print("Мы получили вопрос")
                    # print("тип комнаты", room.game_mode)
                    if room.game_mode == 0:
                        self.stage["message"]["your_response"] = None
                    elif room.game_mode == 1:

                        try:
                            self.stage["message"]["your_response"][data["author_answer"]] = False
                        except:
                            self.stage["message"]["your_response"] = {data["author_answer"]:False,}

                        # self.stage["message"]["your_response"] = []
                    elif room.game_mode == 2:
                        try:
                            self.stage["message"]["your_response"][data["author_answer"]] = False
                        except:
                            self.stage["message"]["your_response"] = {data["author_answer"]:False,}
                        # pass

                    login = await self.get_user(data["author_answer"])
                    login = login.login

                    early_response = False
                    if data["type"] == "early_response":
                        early_response = True
                        # Вернуться
                    author_answer = login
                    author_answer_id = data["author_answer"]
                    answer = data["answer"]
                    description = data["description"]
                    Class_answer = ""
                    Class_description = ""

                    if len(answer) !=0:
                        Class_answer += "user_provide_answer"
                    else:
                        answer = "Пользователь не дал ответ"
                        Class_answer += "user_not_provide_answer"

                    if len(description) != 0:
                        Class_description += "user_provide_description"
                    else:
                        description = "Пользователь не дал описания вопроса"
                        Class_description += "user_not_provide_description"

                    if room.game_mode == 0:
                        group_message = {
                            'type': 'returned_answer',
                            'game_mode': 0,
                            "leader_id": self.leader_id,
                            "captain_id": self.stage["captain_id"],
                            "author_answer": author_answer,
                            "author_answer_id": author_answer_id,
                            "early_response": early_response,
                            'answer': answer,
                            'description': description,
                            'Class_answer': Class_answer,
                            'Class_description': Class_description,
                        }

                        self.stage["message"]["get_answer"] = group_message

                        # await self.channel_layer.group_send(
                        #     self.room_group_name,
                        #     group_message
                        # )

                    elif room.game_mode == 1:
                        group_message = {
                            'type': 'returned_answer',
                            'game_mode': 1,
                            "leader_id": self.leader_id,
                            "captain_id": self.stage["captain_id"],
                            "author_answer": author_answer,
                            "author_answer_id": author_answer_id,
                            "early_response": early_response,
                            'answer': answer,
                            'description': description,
                            'Class_answer': Class_answer,
                            'Class_description': Class_description,
                        }
                        try:
                            self.stage["message"]["get_answer"].append(group_message)
                        except:
                            self.stage["message"]["get_answer"] = [group_message]

                        # self.stage["message"]["get_answer"] = group_message
                    elif room.game_mode == 2:
                        group_message = {
                            'type': 'returned_answer',
                            'game_mode': 2,
                            "leader_id": self.leader_id,
                            "captain_id": self.stage["captain_id"],
                            "author_answer": author_answer,
                            "author_answer_id": author_answer_id,
                            "early_response": early_response,
                            'answer': answer,
                            'description': description,
                            'Class_answer': Class_answer,
                            'Class_description': Class_description,
                            'whom': "captain",
                        }
                        try:
                            self.stage["message"]["get_answer"].append(group_message)
                        except:
                            self.stage["message"]["get_answer"] = [group_message]

                    # group_message = {
                    #     'type': 'returned_answer',
                    #     "leader_id" : self.leader_id,
                    #     "author_answer": author_answer,
                    #     "early_response" : early_response,
                    #     'answer': answer,
                    #     'description': description,
                    #     'Class_answer': Class_answer,
                    #     'Class_description': Class_description,
                    # }
                    #
                    # self.stage["message"]["get_answer"] = group_message
                    #
                    # await self.channel_layer.group_send(
                    #     self.room_group_name,
                    #     group_message
                    # )

                elif data["type"] == "get_menu":
                    if self.room_tasks != {}:
                        task = self.room_tasks.pop(self.room_id, None)
                        if task:
                            task.cancel()

                        questions = cache.get(self.cache_key)
                        for question_id, question_data in questions.items():
                            if question_data["frostbite"]:
                                question_data["time_read"] = (len(question_data["text_question"]) // room.reading_speed) + 1
                                question_data["time_question"] = room.question_time
                        cache.set(self.cache_key, questions, timeout=3600)

                    group_message = await send_question_meny()

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        group_message
                    )
                elif data["type"] == "random_question":
                    # Вернуться
                    self.check_like = 0
                    if self.room_tasks != {}:
                        task = self.room_tasks.pop(self.room_id, None)
                        if task:
                            task.cancel()

                    await send_random()

                    # questions = cache.get(self.cache_key)
                    # check_random = get_random_unused_question_key(questions)
                    # if check_random != False:
                    #     await self.send(text_data=json.dumps({
                    #         'type': 'random_question',
                    #         'question_number': check_random,
                    #     }))
                    #     self.stage["stage"] = "random_question"
                    #     self.stage["message"] = check_random
                    # else:
                    #     # заглушка для конца игры конец вернуться
                    #     print("Вопросы кончились")
                    #     pass


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
                    if len(room.people_on_page["users"]) >=3 and room.leader != None and room.captain != None:
                        room.room_limit = len(room.people_on_page["users"])
                        # room.save()
                        await self.update_room(room, len(room.people_on_page["users"]))

                        group_message = {
                            'type': 'handle_action_game',  # Важно: должно соответствовать имени метода
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
                        'type': 'handle_action_game',  # Важно: должно соответствовать имени метода
                        'action_type': "cancellation",
                        'message': None,
                        'user_id': self.user_id,
                        'timestamp': str(datetime.now())
                    }


                elif data[action_type] == "play":
                    self.stage["condition"] = "play"
                    task = asyncio.create_task(time_question())
                    self.room_tasks[self.room_id] = task

                elif data[action_type] == "pause":



                    self.stage["condition"] = "pause"
                    task = self.room_tasks.pop(self.room_id, None)
                    if task:
                        task.cancel()

                elif data[action_type] == "pluse":
                    task = self.room_tasks.pop(self.room_id, None)

                    if task:
                        task.cancel()

                        if self.stage["message"]["time_read"] > 0:
                            if self.stage["message"]["time_read"] + data["value"] >=0:
                                self.stage["message"]["time_read"] += data["value"]
                            else:
                                self.stage["message"]["time_read"] = 1
                        elif self.stage["message"]["time_question"] > 0:
                            if self.stage["message"]["time_question"] + data["value"] >=0:
                                self.stage["message"]["time_question"] += data["value"]
                            else:
                                self.stage["message"]["time_question"] = 1

                        task = asyncio.create_task(time_question())
                        self.room_tasks[self.room_id] = task

                    else:

                        if self.stage["message"]["time_read"] > 0:
                            if self.stage["message"]["time_read"] + data["value"] >= 0:
                                self.stage["message"]["time_read"] += data["value"]
                            else:
                                self.stage["message"]["time_read"] = 0

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': self.stage["message"]["time_read"],
                                    'Class': "time_read",
                                }
                            )

                        elif self.stage["message"]["time_question"] > 0:
                            if self.stage["message"]["time_question"] + data["value"] >= 0:
                                self.stage["message"]["time_question"] += data["value"]
                            else:
                                self.stage["message"]["time_question"] = 0

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': self.stage["message"]["time_question"],
                                    'Class': "time_question",
                                }
                            )
                elif data[action_type] == "like" or data[action_type] == "dislike":
                    status = ""
                    Class = ""
                    if room.game_mode == 0:
                        if data[action_type] == "like":
                            self.stage["score"]["players"] += 1
                            status = "Ответ верный"
                            Class = "correct"

                        if data[action_type] == "dislike":
                            self.stage["score"]["authors"] += 1
                            status = "Ответ не верный"
                            Class = "wrong"

                        if Class == "correct":
                            questions = cache.get(self.cache_key)
                            question = questions.pop(data["question_number"], None)
                            # Проверяем, что вопрос существует
                            if question is not None:
                                # Обновляем значение
                                question["answer_status"] = {
                                    "status": True,
                                    "user": data["author_answer"],
                                }
                                # Добавляем вопрос обратно в список
                                questions[data["question_number"]] = question
                                sorted_questions = sorted(questions.items())
                                # Преобразование обратно в словарь
                                questions = dict(sorted_questions)
                                # Сохраняем обновленный список в кэш
                                cache.set(self.cache_key, questions, timeout=3600)

                    elif room.game_mode == 1:
                        self.check_like += 1
                        # print(data["author_answer"])
                        # print(self.stage["score"]["players"])
                        # print("Все your_response-ы",self.stage["message"]["your_response"])
                        # print("Автор ответа",data["author_answer"])
                        # print("Значение your_response-а",self.stage["message"]["your_response"][data["author_answer"]])
                        self.stage["message"]["your_response"][data["author_answer"]] = True

                        login = await self.get_user(data["author_answer"])
                        login = login.login
                        if data[action_type] == "like":
                            self.stage["score"]["players"][login] += 1
                            status = "Ответ верный"
                            Class = "correct"

                        if data[action_type] == "dislike":
                            self.stage["score"]["authors"][login] += 1
                            status = "Ответ не верный"
                            Class = "wrong"

                        if Class == "correct":
                            questions = cache.get(self.cache_key)
                            question = questions.pop(data["question_number"], None)
                            # Проверяем, что вопрос существует
                            if question is not None:
                                # Обновляем значение
                                question["answer_status"]["status"] = True
                                try:
                                    question["answer_status"]["user"].append(data["author_answer"])
                                except Exception as e:
                                    print(e)
                                    question["answer_status"]["user"] = [data["author_answer"]]


                                # Добавляем вопрос обратно в список
                                questions[data["question_number"]] = question
                                sorted_questions = sorted(questions.items())
                                # Преобразование обратно в словарь
                                questions = dict(sorted_questions)
                                # Сохраняем обновленный список в кэш
                                cache.set(self.cache_key, questions, timeout=3600)

                    elif room.game_mode == 2:
                        # Вернуться
                        if data['type'] == "captain":
                            group_message = {
                                'type': 'returned_answer',
                                'game_mode': 2,
                                "leader_id": self.leader_id,
                                "captain_id": self.stage["captain_id"],
                                "author_answer": data['author_answer'],
                                "author_answer_id": data['author_answer_id'],
                                'answer': data['answer'],
                                'description': data['description'],
                                'Class_answer': data['Class_answer'],
                                'Class_description': data['Class_description'],
                                'whom': "leader",
                            }
                            self.stage["message"]["get_answer"] = group_message
                        elif data['type'] == "leader":
                            if data[action_type] == "like":
                                self.stage["score"]["players"] += 1
                                status = "Ответ верный"
                                Class = "correct"

                            if data[action_type] == "dislike":
                                self.stage["score"]["authors"] += 1
                                status = "Ответ не верный"
                                Class = "wrong"

                            if Class == "correct":
                                questions = cache.get(self.cache_key)
                                question = questions.pop(data["question_number"], None)
                                # Проверяем, что вопрос существует
                                if question is not None:
                                    # Обновляем значение
                                    question["answer_status"] = {
                                        "status": True,
                                        "user": data["author_answer"],
                                    }
                                    # Добавляем вопрос обратно в список
                                    questions[data["question_number"]] = question
                                    sorted_questions = sorted(questions.items())
                                    # Преобразование обратно в словарь
                                    questions = dict(sorted_questions)
                                    # Сохраняем обновленный список в кэш
                                    cache.set(self.cache_key, questions, timeout=3600)


                    if room.game_mode != 2:
                        group_message_score = {
                            'type': 'score_send',
                            "score_players" : self.stage["score"]["players"],
                            "score_authors" : self.stage["score"]["authors"],
                            "status" : status,
                            "Class" : Class,
                            "leader_id": self.leader_id,
                        }
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            group_message_score
                        )
                    elif data['type'] == "leader":
                        group_message_score = {
                            'type': 'score_send',
                            "score_players": self.stage["score"]["players"],
                            "score_authors": self.stage["score"]["authors"],
                            "status": status,
                            "Class": Class,
                            "leader_id": self.leader_id,
                        }
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            group_message_score
                        )



                    # Вернуться
                    # Если режим "Классика"
                    if room.game_mode == 0:
                        # Если включен случайный порядок вопросов
                        if room.random_order:
                            # group_message_break = {
                            #     'type': 'send_break',
                            #     "time": room.break_between_questions,
                            # }
                            # await self.channel_layer.group_send(
                            #     self.room_group_name,
                            #     group_message_break
                            # )

                            for i in range(room.break_between_questions):
                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    {
                                        'type': 'time_sender',
                                        'time': room.break_between_questions-i,
                                        'Class': "break_between_questions",
                                    }
                                )
                                await asyncio.sleep(1)
                                print("перерыв между вопросами осталось ", room.break_between_questions - i, "скунд")
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': 0,
                                    'Class': "break_between_questions",
                                }
                            )


                            await send_random()

                            # questions = cache.get(self.cache_key)
                            # check_random = get_random_unused_question_key(questions)
                            # if check_random != False:
                            #     await self.send(text_data=json.dumps({
                            #         'type': 'random_question',
                            #         'question_number': check_random,
                            #     }))
                            #     self.stage["stage"] = "random_question"
                            #     self.stage["message"] = check_random
                            # else:
                            #     # заглушка для конца игры конец вернуться
                            #     print("Вопросы кончились")
                            #     pass
                        # Если включен не случайный порядок вопросов
                        else:
                            if self.room_tasks != {}:
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

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                group_message_2
                            )
                    # Если режим "Спорт"
                    elif room.game_mode == 1:
                        # print("Игроки: ",self.stage["score"]["players"])
                        # print("Кол-во человек ",len(self.stage["score"]["players"]))
                        # print("Ответы",self.stage["message"]["your_response"])
                        # print("Кол-во ответов",len(self.stage["message"]["your_response"]))


                        if self.check_like == len(room.people_on_page.get("users", []))-1:
                            self.check_like = 0
                            # task = self.timer_Nsec_tasks.pop(self.room_id, None)
                            # if task:
                            #     task.cancel()

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
                                    print("перерыв между вопросами осталось ", room.break_between_questions-i, "скунд")
                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    {
                                        'type': 'time_sender',
                                        'time': 0,
                                        'Class': "break_between_questions",
                                    }
                                )


                                await send_random()

                                # questions = cache.get(self.cache_key)
                                # check_random = get_random_unused_question_key(questions)
                                # if check_random != False:
                                #     await self.send(text_data=json.dumps({
                                #         'type': 'random_question',
                                #         'question_number': check_random,
                                #     }))
                                #     self.stage["stage"] = "random_question"
                                #     self.stage["message"] = check_random
                                # else:
                                #     # заглушка для конца игры конец вернуться
                                #     print("Вопросы кончились")
                                #     pass
                            # Если включен не случайный порядок вопросов
                            else:
                                if self.room_tasks != {}:
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

                                await self.channel_layer.group_send(
                                    self.room_group_name,
                                    group_message_2
                                )
                    elif room.game_mode == 2 and data['type'] == "leader":

                        # Если включен случайный порядок вопросов
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
                                print("перерыв между вопросами осталось ", room.break_between_questions-i, "скунд")

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'time_sender',
                                    'time': 0,
                                    'Class': "break_between_questions",
                                }
                            )

                            await send_random()

                        # Если включен не случайный порядок вопросов
                        else:
                            if self.room_tasks != {}:
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

                            await self.channel_layer.group_send(
                                self.room_group_name,
                                group_message_2
                            )

                        #Вернуться
                        #Заметка на полях, дать такую возможность в остальных режимах

            # Отправляем в группу
            try:
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
                "question_id": question.ID,
                "question_name": question.question_name,
                "text_question": question.text_question,
                "note": question.note,
                "answer": question.answer,
                "answer_description": question.answer_description,
                "license_id": question.license_id.ID,
                "frostbite": True,
                "question_number": i,
                'use': False,
                'time_read': (len(question.text_question) // room.reading_speed) +1,
                'time_question': room.question_time,
                'answer_status': {
                    "status":False,
                    "user": None,
                },
            }
        # Сохраняем вопросы в кеш
        sorted_questions = sorted(questions_dict.items())

        # Преобразование обратно в словарь
        questions_dict = dict(sorted_questions)

        cache.set(self.cache_key, questions_dict, timeout=3600)
        # self.cache_set(self.cache_key, questions_dict, timeout=3600)

    async def notify_stage(self):
        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': self.stage["stage"],
            'condition': self.stage["condition"],
            'message': self.stage["message"],
            'user_id': self.stage["user_id"],
            'captain_id': self.stage["captain_id"],
            'score' : self.stage["score"],
        }))

    async def send_skip(self, event):
        if self.leader_id == self.user_id:
            await self.send(text_data=json.dumps({
                'type': "skip",
            }))

    # async def send_break(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': "break_between_questions",
    #         'time': event.get('time'),
    #     }))


    async def time_sender(self, event):
        try:
            response = {
                'type': "time",
                'time': event.get('time'),
                "Class": event.get('Class'),
                "leader_id": event.get('leader_id'),
                "captain_id": self.stage["captain_id"]
            }

            await self.send(text_data=json.dumps(response))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")



    async def notify_stage_not_leader(self,room):
        try:

            question = {
                'question_id': self.stage["message"]["question_id"],
                'question_name': self.stage["message"]["question_name"],
                'text_question': self.stage["message"]["text_question"],
                'note': None,
                'answer': None,
                'answer_description': None,
                'question_number': self.stage["message"]["question_number"],
                'time_read': self.stage["message"]["time_read"],
                'time_question': self.stage["message"]["time_question"],
                'your_response': self.stage["message"]["your_response"],
            }

        except Exception as e:

            question = {
                'question_id': self.stage["message"]["question_id"],
                'question_name': self.stage["message"]["question_name"],
                'text_question': self.stage["message"]["text_question"],
                'note': None,
                'answer': None,
                'answer_description': None,
                'question_number': self.stage["message"]["question_number"],
                'time_read': self.stage["message"]["time_read"],
                'time_question': self.stage["message"]["time_question"],
                'your_response': None,
            }

            if e != 'your_response':
                print("Произошла ошибка: ",e)
                traceback.print_exc()

        if not room.show_question:
            question['text_question'] = None

        if room.game_mode == 2:
            try:
                if type(self.stage["message"]["get_answer"]) == list and self.user_id == self.stage["captain_id"]:
                    question["get_answer"] = self.stage["message"]["get_answer"]
            except Exception as e:
                print("ошибка", e)
                question["get_answer"] = None



        await self.send(text_data=json.dumps({
            'type': 'status_room',
            'stage': self.stage["stage"],
            'condition': self.stage["condition"],
            'message': question,
            'user_id': self.stage["user_id"],
            'score': self.stage["score"],
            'captain_id': self.stage["captain_id"],
        }))

    async def score_send(self, event):
        await self.send(text_data=json.dumps({
            'type': "score",
            'score_players': event.get('score_players'),
            'score_authors': event.get('score_authors'),
            'status': event.get('status'),
            'Class': event.get('Class'),
            'leader_id': self.leader_id,
        }))

    async def returned_answer(self, event):
        if event["game_mode"] != 2:
            if event["leader_id"] == self.user_id:
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
        elif event["game_mode"] == 2:
            if event["captain_id"] == self.user_id and event["whom"] == "captain":
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
            elif event["leader_id"] == self.user_id and event["whom"] == "leader":
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

    async def ready_respond_users(self, event):
        if event["user_id"] == self.user_id:
            response = {
                'type': 'return'
            }
            await self.send(text_data=json.dumps(response))

    async def sending_question(self, event):
        room = await self.get_room(self.room_id)
        await self.delete_all_messages_in_room(self.room_id)

        try:
            if event["leader_id"] == self.user_id:
                response = {
                    'type': "get_question",
                    'question_id': event.get('question_id'),
                    'question_name': event.get('question_name'),
                    'text_question': event.get('text_question'),
                    'note': event.get('note'),
                    'answer': event.get('answer'),
                    'answer_description': event.get('answer_description'),
                    'user_id': event["leader_id"],
                    'question_number': event.get('question_number'),
                    'time_read': event.get('time_read'),
                    'time_question': event.get('time_question'),
                }
            elif room.show_question:
                response = {
                    'type': "get_question",
                    'question_id': event.get('question_id'),
                    'question_name': event.get('question_name'),
                    'text_question': event.get('text_question'),
                    'note': None,
                    'answer': None,
                    'answer_description': None,
                    'user_id': event["leader_id"],
                    'question_number': event.get('question_number'),
                    'time_read': event.get('time_read'),
                    'time_question': event.get('time_question'),
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
                    'user_id': event["leader_id"],
                    'question_number': event.get('question_number'),
                    'time_read': event.get('time_read'),
                    'time_question': event.get('time_question'),
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
    def get_your_id(self, room, type):
        if type == "host":
            return room.host.ID
        elif type == "captain":
            return room.captain.ID
        elif type == "leader":
            return room.leader.ID

    @sync_to_async
    def update_room(self, room, new_limit):
        room.room_limit = new_limit
        room.save()

    def _stage_cache_key(self):
        return f'room_{self.room_id}_stage'

    def _questions_cache_key(self):
        return f'room_{self.room_id}_questions'

    async def _stage_get(self):
        stage = await sync_to_async(cache.get)(self._stage_cache_key())
        return stage

    async def _stage_set(self, stage):
        await sync_to_async(cache.set)(self._stage_cache_key(), stage, timeout=3600)