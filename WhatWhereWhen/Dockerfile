# Используем официальный образ Python 3.13
FROM python:3.13-slim

# Устанавливаем переменную окружения, чтобы Python не буферизовал вывод
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Собираем статику (если используется)
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 (для HTTP) и 8001 (если нужен отдельный порт для Channels, можно настроить)
EXPOSE 8000

# Запускаем ASGI-сервер Daphne для поддержки Channels
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "WhatWhereWhen.asgi:application"]
