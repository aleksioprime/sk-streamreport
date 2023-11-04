# Указываем Docker использовать образ Python в качестве базового
FROM python:3.10.11-alpine

# Устанавливаем необходимые переменные окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочий каталог контейнера 
WORKDIR /backend

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Установка зависимостей
RUN pip install --upgrade pip
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Копирование entrypoint.sh
COPY backend/entrypoint.sh ./
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Копирование всех файлов из локального проекта в контейнер
COPY backend .