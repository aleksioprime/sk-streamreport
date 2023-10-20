#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Создание файлов миграций
# python manage.py makemigrations
# Очистка БД от данных
# python manage.py flush --no-input
# Применение миграций Django
# python manage.py migrate

# Запуск команды (обычно запуск сервера Django)
exec "$@"