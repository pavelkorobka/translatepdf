from fastapi import Security, APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
import os
import httpx
import jwt
import secrets
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.user import User
from app.dependencies import get_db  # ✅ Импорт get_db из dependencies.py
from app.config import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if not isinstance(payload, dict) or "id" not in payload or "email" not in payload:
            raise HTTPException(status_code=401, detail="Неверный формат токена")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")

router = APIRouter()

@router.get("/google")
def login_with_google():
    state = secrets.token_urlsafe(16)  # CSRF-защита
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&state={state}"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str, state: str, db: Session = Depends(get_db)):  # ✅ Используем get_db из dependencies.py
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка при получении токена от Google")

        token_json = response.json()

    if "access_token" not in token_json:
        raise HTTPException(status_code=400, detail="Ошибка при получении токена Google")

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {token_json['access_token']}"}

    async with httpx.AsyncClient() as client:
        user_response = await client.get(user_info_url, headers=headers)
        if user_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка при получении данных пользователя")

        user_json = user_response.json()

    if "email" not in user_json:
        raise HTTPException(status_code=400, detail="Ошибка при получении email пользователя")

    # Проверяем пользователя в БД
    user = db.query(User).filter(User.email == user_json["email"]).first()

    if not user:
        user = User(
            email=user_json["email"],
            name=user_json.get("name"),
            picture=user_json.get("picture"),
            refresh_token=secrets.token_urlsafe(32)
        )
        db.add(user)
    else:
        user.refresh_token = secrets.token_urlsafe(32)

    db.commit()
    db.refresh(user)

    # Генерируем новый JWT с истечением через 1 час
    expiration = datetime.utcnow() + timedelta(hours=1)
    token_payload = {"email": user.email, "id": user.id, "exp": expiration}
    access_token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": user.refresh_token,
        "token_type": "bearer",
        "user": user_json
    }

@router.post("/auth/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):  # ✅ Используем get_db из dependencies.py
    user = db.query(User).filter(User.refresh_token == refresh_token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Неверный refresh_token")

    expiration = datetime.utcnow() + timedelta(hours=1)
    token_payload = {"email": user.email, "id": user.id, "exp": expiration}
    new_access_token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/auth/logout")
def logout(user_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):  # ✅ Используем get_db из dependencies.py
    user = db.query(User).filter(User.id == user_data["id"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    user.refresh_token = None
    db.commit()

    return {"message": "Выход выполнен"}