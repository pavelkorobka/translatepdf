# routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User
from app.auth import get_current_user

router = APIRouter()

# 1️⃣ Получение информации о текущем пользователе
@router.get("/me")
def get_current_user_info(user_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_data["id"]).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "created_at": user.created_at
    }

# 2️⃣ Получение списка всех пользователей (для админов, если понадобится)
@router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "name": u.name, "created_at": u.created_at} for u in users]

# 3️⃣ Удаление аккаунта пользователя
@router.delete("/me")
def delete_user(user_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_data["id"]).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.delete(user)
    db.commit()

    return {"message": "Аккаунт успешно удален"}