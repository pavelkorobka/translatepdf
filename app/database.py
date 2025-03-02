import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def init_db():
    """Создает все таблицы в базе данных (если они еще не существуют)."""
    from app.models import user, pdf  # Импортируем модели перед созданием таблиц
    Base.metadata.create_all(bind=engine)