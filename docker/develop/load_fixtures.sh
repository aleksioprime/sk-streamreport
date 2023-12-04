#!/bin/bash

# Параметры подключения к базе данных
host="$1"
port="$2"
shift 2
cmd="$@"

# Функция для проверки готовности базы данных
check_db_ready() {
    echo "Checking if DB is ready..."
    while ! nc -z "$host" "$port"; do
        sleep 1
    done
    echo "DB is ready."
}

# Функция для проверки выполнения миграций
check_migrations() {
    echo "Checking migrations..."
    python manage.py showmigrations | grep '\[ \]' && return 1 || return 0
}

# Загрузка фикстур
load_fixtures() {
    echo "Loading fixtures..."
    python manage.py loaddata group.json
    python manage.py loaddata general.json
    python manage.py loaddata curriculum.json
    python manage.py loaddata ibo.json
    python manage.py loaddata myp.json
    python manage.py loaddata report.json
    # Добавьте дополнительные команды для загрузки других фикстур
}

# Основной поток выполнения
check_db_ready
if check_migrations; then
    load_fixtures
else
    echo "Migrations are not fully applied."
    exit 1
fi