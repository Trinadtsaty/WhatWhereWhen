# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем системные зависимости для сборки mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    python3-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
# Копируем весь проект
COPY . .

# Экспортируем переменные окружения (если хотите, можно задавать через docker-compose)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Собираем статику (опционально, если хотите делать это в образе)
# RUN python manage.py collectstatic --noinput
RUN python manage.py collectstatic --noinput
# Команда запуска (можно переопределить в docker-compose)
# CMD ["gunicorn", "WhatWhereWhen.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "WhatWhereWhen.asgi:application"]

