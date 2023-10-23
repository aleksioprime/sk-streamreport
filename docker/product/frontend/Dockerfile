FROM node:16 as build-stage

# Устанавливаем рабочий каталог контейнера 
WORKDIR /frontend

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Копируем все файлы фронтенда и запускаем фронтенд
COPY frontend /frontend
RUN npm run build

FROM nginx:alpine as production-stage

COPY --from=build-stage /frontend/dist /usr/share/nginx/html
EXPOSE 8080

# Запуск сервера frontend
CMD ["nginx", "-g", "daemon off;"]