# Проект StreamReport

## Запуск у разработчика

Для развёртывания проекта приложения StreamReport у разработчика должно быть установлено:

- Система контроля версий Git: https://git-scm.com/downloads
- Платформа Docker Desktop: https://www.docker.com/get-started
- Для запуска Makefile: https://chocolatey.org/install:
```choco install make```
- Имя и электронная почта глобального пользователя Git:
```git config --global user.name "имя пользователя"```
```git config --global user.email "электронная почта"```

Далее выполнить следующие действия:

1. Открыть терминал/командную строку и перейти в каталог проектов.
    
Клонировать репозиторий из GitHub (HTTPs):
```git clone https://github.com/aleksioprime/streamreport.git```
    
Клонировать репозиторий из SK (SSH: нужен ssh-ключ):
    
```git clone [git@gitlab.sk.ru](mailto:git@gitlab.sk.ru):gymnasium/freshstream.git```
    
2. Перейти в папку проекта и развернуть проект с помощью Makefile или Docker Compose:

```cd streamreport```
```make deploy```

```docker-compose up -d --build```