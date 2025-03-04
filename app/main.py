from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.pdf import router as pdf_router
from app.routes.users import router as users_router
from app.routes.project import router as project_router

print("🚀 FastAPI успешно запущен!")

app = FastAPI()

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(project_router, prefix="/project", tags=["Project"])
app.include_router(users_router, prefix="/users", tags=["Users"])

# Безопасность: добавляем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажем домен фронтенда в будущем
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализируем базу данных
init_db()