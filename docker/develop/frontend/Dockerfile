FROM node:latest

# Устанавливаем рабочий каталог контейнера 
WORKDIR /frontend

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm ci

# Копируем все файлы фронтенда и запускаем фронтенд
COPY frontend /frontend