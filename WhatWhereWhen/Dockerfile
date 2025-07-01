# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем системные зависимости для сборки mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Экспортируем переменные окружения (если хотите, можно задавать через docker-compose)
ENV PYTHONUNBUFFERED=1

# Собираем статику (опционально, если хотите делать это в образе)
# RUN python manage.py collectstatic --noinput

# Команда запуска (можно переопределить в docker-compose)
CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
