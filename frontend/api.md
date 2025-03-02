# 📌 API Документация для проекта **TranslatePDF**

**Base URL:** `http://localhost:8000`

## **🔹 Авторизация**
### **1. Вход через Google OAuth**
#### `GET /auth/google`
🔹 **Описание:** Перенаправляет пользователя на страницу входа Google OAuth.  
🔹 **Ответ:** 302 Redirect → Google OAuth.  

#### `GET /auth/google/callback?code=<код>`
🔹 **Описание:** Получает `code` от Google, обменивает его на `access_token` и `refresh_token`.  
🔹 **Ответ:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token_string",
  "token_type": "bearer",
  "user": {
    "email": "user@example.com",
    "name": "John Doe",
    "picture": "https://example.com/photo.jpg"
  }
}

2. Обновление JWT-токена

POST /auth/refresh

🔹 Описание: Получает refresh_token, выдает новый access_token.
🔹 Тело запроса:

{
  "refresh_token": "refresh_token_string"
}

🔹 Ответ:

{
  "access_token": "new_jwt_token",
  "token_type": "bearer"
}

3. Выход из системы

POST /auth/logout

🔹 Описание: Удаляет refresh_token, завершает сессию пользователя.
🔹 Требует заголовок:
Authorization: Bearer <jwt_token>
🔹 Ответ:

{
  "message": "Выход выполнен"
}

🔹 Работа с PDF

🔹 Требует авторизацию:
Authorization: Bearer <jwt_token>

1. Загрузка PDF

POST /pdf/upload/

🔹 Описание: Загружает PDF-файл, привязывает к пользователю.
🔹 Тело запроса: multipart/form-data

file: <PDF-файл>

🔹 Ответ:

{
  "message": "Файл загружен",
  "filename": "test.pdf"
}

2. Получение списка загруженных PDF

GET /pdf/files/

🔹 Описание: Получает список PDF, загруженных текущим пользователем.
🔹 Ответ:

[
  {
    "id": 1,
    "filename": "test.pdf",
    "uploaded_at": "2024-03-01T12:00:00"
  }
]

3. Удаление конкретного PDF

DELETE /pdf/files/{filename}

🔹 Описание: Удаляет файл по имени (если он принадлежит пользователю).
🔹 Пример запроса:

DELETE /pdf/files/test.pdf

🔹 Ответ:

{
  "message": "Файл test.pdf удалён"
}

4. Удаление всех PDF пользователя

DELETE /pdf/files/

🔹 Описание: Удаляет все файлы, загруженные пользователем.
🔹 Ответ:

{
  "message": "Все файлы удалены"
}

🔹 Пользователь

🔹 Требует авторизацию:
Authorization: Bearer <jwt_token>

1. Получение данных текущего пользователя

GET /users/me

🔹 Описание: Получает информацию о текущем пользователе.
🔹 Ответ:

{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://example.com/photo.jpg",
  "created_at": "2024-03-01T12:00:00"
}

2. Получение списка всех пользователей

GET /users/

🔹 Описание: Получает список всех пользователей (может быть ограничено только для админов).
🔹 Ответ:

[
  {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-03-01T12:00:00"
  }
]

3. Удаление аккаунта

DELETE /users/me

🔹 Описание: Удаляет текущий аккаунт пользователя и все связанные данные.
🔹 Ответ:

{
  "message": "Аккаунт успешно удален"
}

