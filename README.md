# Проект StreamReport

## Запуск версии develop:
1. Скопировать репозиторий в локальную папку проекта
2. В терминале перейти в папку проекта и выполнить:
```
docker-compose up -d --build
```
3. Выполнить в контейнере подготовку миграций для базы данных
```
docker-compose exec backend python manage.py makemigrations --noinput
```
4. Применить в контейнере миграцию базы данных
```
docker-compose exec backend python manage.py migrate --noinput
```
Может потребоваться перезапуск контейнера backend:
```
docker-compose restart backend
```
6. Создайть суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```

## Запуск версии product через Action GitHub на сервере:
1. На сервере Ubuntu 22.04 должен быть установлен Docker и Docker Compose
2. Убедиться в корректности сборок контейнеров backend и frontend в GitHub и  DockerHub
3. Скопировать файлы docker-compose.yaml и дополнительные зависимости проекта на сервер (нет в репозитории)
4. Запустить docker-compose:
```
docker-compose up -d --build
```
5. Собрать все статические файлы Django в папку static:
```
docker-compose exec backend python manage.py collectstatic --no-input --clear
```
6. Выполнить миграции в БД:
```
docker-compose exec backend python manage.py migrate --noinput
```
7. Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
superuser: admin
email: aleksioprime@gmail.com
password: A0Ru$$22
```
8. Запросить бесплатный сертифкат let's encript
```
certbot certonly --standalone -d skreport.ru -d www.skreport.ru
```

* Применение изменений проекта на сервере:
```
docker-compose pull
docker-compose build
docker-compose down
docker-compose up -d
```
* Удаление всех неиспользуемых контейнеров:
```
docker system prune
```
* Удаление всех имеющихся контейнеров:
```
docker-compose down -v
docker rmi $(docker images -q)
```

# Разное
Войти в базу данных через psql:
```
docker-compose exec database psql --username=igadmin --dbname=igskolkovo
```
Посмотреть базу данных и пользователя:
```
\c igskolkovo
```
Посмотреть таблицы текущей базы данных:
```
\dt
```
Выход из базы данных
```
\q
```