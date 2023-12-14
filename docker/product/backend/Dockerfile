# Указываем Docker использовать образ Python в качестве базового
FROM python:3.10.11-alpine

# Устанавливаем необходимые переменные окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочий каталог контейнера
# create the appropriate directories
RUN mkdir /home/app
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Установка зависимостей
RUN pip install --upgrade pip
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Копирование entrypoint.sh
COPY backend/entrypoint.sh $APP_HOME
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# Копирование всех файлов из локального проекта в контейнер
COPY backend .
# Сделать порт 8000 доступным
EXPOSE 8000

# Запуск entrypoint.sh
ENTRYPOINT ["/home/app/backend/entrypoint.sh"]

# Запуск сервера backend
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]