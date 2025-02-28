# routes/pdf.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from app.dependencies import get_db
from app.models.pdf import PDFFile
from app.auth import get_current_user
from app.config import UPLOAD_DIR

router = APIRouter()

MAX_FILE_SIZE_MB = 10  # Ограничение размера файлов

# 1️⃣ Загрузка PDF (привязываем к пользователю)
@router.post("/upload/")
async def upload_pdf(
    file: UploadFile = File(...),
    user_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате PDF")

    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Файл слишком большой (максимум 10MB)")

    file_path = os.path.join(UPLOAD_DIR, f"{user_data['id']}_{file.filename}")

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    pdf_entry = PDFFile(
        filename=file.filename,
        filepath=file_path,
        user_id=user_data["id"]
    )
    db.add(pdf_entry)
    db.commit()

    return {"message": "Файл загружен", "filename": file.filename}

# 2️⃣ Получение списка файлов (только своих)
@router.get("/files/")
async def list_pdfs(
    user_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = db.query(PDFFile).filter(PDFFile.user_id == user_data["id"]).all()
    return [{"id": f.id, "filename": f.filename, "uploaded_at": f.uploaded_at} for f in files]

# 3️⃣ Удаление одного PDF (только своего)
@router.delete("/files/{filename}")
async def delete_pdf(
    filename: str,
    user_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pdf = db.query(PDFFile).filter(
        PDFFile.filename == filename,
        PDFFile.user_id == user_data["id"]
    ).first()

    if not pdf:
        raise HTTPException(status_code=404, detail="Файл не найден или принадлежит другому пользователю")

    os.remove(pdf.filepath)
    db.delete(pdf)
    db.commit()

    return {"message": f"Файл {filename} удалён"}

# 4️⃣ Удаление всех файлов (только своих)
@router.delete("/files/")
async def delete_all_pdfs(
    user_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = db.query(PDFFile).filter(PDFFile.user_id == user_data["id"]).all()

    if not files:
        return {"message": "Нет файлов для удаления"}

    for file in files:
        os.remove(file.filepath)
        db.delete(file)

    db.commit()
    return {"message": "Все файлы удалены"}