
# 
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

## Работа с Docker
### Просмотр логов в docker-контейнере
```
docker-compose logs -f
docker-compose -f docker-compose.prod.yml logs -f
```
### Удаление образа 
```
docker-compose down -v 
```
### Запуск образа разработчика
```
docker-compose up -d --build
```
### Запуск производственного образа
```
docker-compose -f docker-compose.prod.yml up -d --build
```
### Выполнение миграции в производственном файле
```
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --no-input --clear
```
