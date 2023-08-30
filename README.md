
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

# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Первый запуск
```
python manage.py createsuperuser
docker-compose exec backend python manage.py createsuperuser
superuser: admin
email: aleksioprime@gmail.com
password: A0Ru$$22
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
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --no-input --clear
```
