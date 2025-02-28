FROM node:23

WORKDIR /translatepdf/frontend

# Копируем package.json и package-lock.json перед установкой зависимостей
COPY frontend/package*.json ./

RUN npm install

# Копируем весь исходный код фронтенда
COPY frontend/ ./

# Открываем порт для dev-сервера Vite
EXPOSE 5173

# Запускаем сервер разработки Vite
CMD ["npm", "run", "dev"]