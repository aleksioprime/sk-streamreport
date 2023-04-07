#!/bin/zsh
# Установить POSTGRESQL: https://www.postgresql.org/download/
# Создать пользователя и базу данных:
# CREATE USER igadmin WITH PASSWORD 'Pox{@K';
# CREATE DATABASE igskolkovo WITH owner=postgres ENCODING = 'UTF-8' template template1;
# CREATE DATABASE igskolkovo WITH owner=igadmin ENCODING = 'UTF-8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' template template0;
# GRANT ALL PRIVILEGES ON DATABASE "igskolkovo" to igadmin;
# Если не напишет, что нет доступа: ALTER DATABASE igskolkovo OWNER TO igadmin;
# Загрузить фикстуры:
# python manage.py loaddata ../local/database/data.json
source ~/venv/freshstream/bin/activate
export POSTGRES_PORT=5432
export POSTGRES_HOST=localhost
export POSTGRES_DB=igskolkovo
export POSTGRES_USER=igadmin
export POSTGRES_PASSWORD=Pox{@K
python3 ~/develop/freshstream/backend/manage.py runserver
