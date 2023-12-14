# Установа модулей Node и подготовка скомпилированной сборки
FROM node:lts-alpine as build

# Устанавливаем рабочий каталог контейнера 
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm ci

# Копируем все файлы фронтенда и собираем приложение
COPY frontend ./
RUN npm run build

# Развёртывание сборки фронтенда в NGINX
FROM nginx:1.22.1
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN rm -rf /usr/share/nginx/html/*
COPY docker/product/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
