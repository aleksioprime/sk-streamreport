FROM node:16 as build-stage

# Устанавливаем рабочий каталог контейнера 
WORKDIR /app

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm ci

# Копируем все файлы фронтенда и собираем приложение
COPY frontend ./
RUN npm run build