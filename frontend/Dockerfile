FROM node:16-slim

# Устанавливаем рабочий каталог контейнера 
WORKDIR /frontend

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY package.json package-lock.json ./
RUN npm ci

# Копируем все файлы фронтенда и запускаем фронтенд
COPY . /frontend
CMD ["npm", "run", "dev"]