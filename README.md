
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