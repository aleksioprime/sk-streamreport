include backend/.env/.env
# Название проекта
PROJECT_NAME = streamreport
# Данные БД
POSTGRES_USER = admin
POSTGRES_PASSWORD = 123456
POSTGRES_DB = igskolkovo
# Файл docker-compose
DOCKER_COMPOSE_FILE = ./docker-compose.yml

# Команда для запуска docker-compose
DC = docker-compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE)

# Путь к скрипту на хосте
HOST_SCRIPT_PATH=./docker/develop/load_fixtures.sh
CONTAINER_SCRIPT_PATH = /load_fixtures.sh
CONTAINER_NAME=$(shell $(DC) ps -q backend)

# Удаление, сборка с запуском проекта
build:
	$(DC) up -d --build
rebuild:
	$(DC) down -v
	$(DC) up -d --build
# Загрузка фикстур
load_fixtures:
	docker cp $(HOST_SCRIPT_PATH) $(CONTAINER_NAME):$(CONTAINER_SCRIPT_PATH)
	$(DC) exec backend sh $(CONTAINER_SCRIPT_PATH) ${SQL_HOST} ${SQL_PORT}
	docker exec $(CONTAINER_NAME) rm $(CONTAINER_SCRIPT_PATH)
# Пересборка и запуск проекта
update:
	$(DC) up -d --force-recreate --build
# Запуск всех контейнеров проекта
start:
	$(DC) up -d
# Остановка всех контейнеров проекта
stop:
	$(DC) stop
# подключение к БД PostgreSQL при помощи консольного клиента psql
db:
	export PGPASSWORD=${POSTGRES_PASSWORD}; docker exec -it database psql -U $(POSTGRES_USER) ${POSTGRES_DB}
# подключение к bash-консоли любого контейнера с явно указанным именем (make b c=backend)
b:
	docker exec -it $(c) /bin/bash
# подключение к контейнеру backend (выход - exit)
bback:
	docker exec -it backend /bin/sh
# удаление всех контейнеров проекта
destroy_all:
	$(DC) down -v
	docker system prune -f
	@IMAGES=$$(docker images -q); \
	if [ -n "$$IMAGES" ]; then \
		docker rmi $$IMAGES; \
	else \
		echo "No Docker images to remove"; \
	fi