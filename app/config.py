import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Конфигурация базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Секретный ключ для JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# Настройки OAuth Google
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")


# Директория для загрузки файлов
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")

# Убедимся, что папка для загрузок существует
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ограничения
MAX_FILE_SIZE_MB = 10  # Максимальный размер файла в MB