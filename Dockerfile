# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /beauty_salon

# Копируем requirements.txt в контейнер
COPY requirements.txt /beauty_salon/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем содержимое проекта в рабочую директорию
COPY beauty_salon /beauty_salon

# Выполняем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
