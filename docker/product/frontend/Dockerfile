# Установа модулей Node и подготовка скомпилированной сборки
FROM node:lts-alpine as build

# Устанавливаем рабочий каталог контейнера 
WORKDIR /app

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
COPY frontend/package-lock.json ./
RUN npm ci

# Копируем все файлы фронтенда и собираем приложение
COPY frontend ./
RUN npm run build

# Развёртывание сборки фронтенда в NGINX
FROM nginx:latest
COPY docker/product/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

# Открываем 80 порт
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]