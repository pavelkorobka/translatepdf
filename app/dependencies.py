from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db():
    """Создает и закрывает сессию базы данных для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()