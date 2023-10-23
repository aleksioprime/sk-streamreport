FROM node:16 as build-stage

# Устанавливаем рабочий каталог контейнера 
WORKDIR /app

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm install

# Копируем все файлы фронтенда и запускаем фронтенд
COPY frontend ./
RUN npm run build

FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

# Запуск сервера frontend
CMD ["nginx", "-g", "daemon off;"]