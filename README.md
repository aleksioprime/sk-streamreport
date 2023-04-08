# Проект Stream Report

## Запуск приложения у разработчика
Клонировать репозиторий в выделенный для этого каталог
```
git clone https://ASemochkin@scm.sk.ru/scm/gym/freshstream.git
```
### Запуск СУБД
Выполняется через Docker один раз после клонирования репозитория
1. Установить Docker Desktop (https://www.docker.com/products/docker-desktop/)
2. Запустить Docker Desktop и в поиске ввести *postgres*
3. Перейти на вкладку Images, выбрать верхний найденный образ *postgres* и нажать RUN
4. В выпадающем списке Optional settings указать внешний порт (0 - для генерации случайного), тома хранения данных (volumes), переменные окружения (environment variables). Используются следующие данные:

Host port: 32770
Volumes:

- Host path: postgres
- Container path: /var/lib/postgresql/data/

Environment variables:

- POSTGRES_DB=igskolkovo
- POSTGRES_USER=igadmin
- POSTGRES_PASSWORD=Pox{@K

5. Нажать *RUN*

### Запуск backend
1. Открыть терминал и перейти в каталог backend проекта 
```
cd backend
```
2. Запустить стартовые команды

- Для операционной системы MacOS:
```
source run_mac.command
```
- Для операционной системы Windows:
```
run_win.bat
```

3. В случае необходимости взаимодействия с Django необходимо завершить работу сервера (Ctrl + C) и выполнить команды.
Для подготовки и миграции данных:
```
python manage.py makemigrations
python manage.py migrate
```
Для импорта данных из фикстур в формате json:
```
python manage.py loaddata --exclude contenttypes ../data/fixtures/data.json
```
Для запуска сервера:
```
python manage.py runserver
```
### Запуск frontend
1. Открыть терминал и перейти в каталог frontend проекта
```
cd frontend
```
При первом запуске после клонирования репозитория необходимо установить окружение npm:
```
npm install
```
2. Запустить сервер разработчика Vue.js:
```
npm run serve
```
