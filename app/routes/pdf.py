# routes/pdf.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os
from app.dependencies import get_db
from app.models.pdf import PDFFile
from app.models.project import Project
from app.routes.auth import get_current_user
from app.config import UPLOAD_DIR, MAX_FILE_SIZE_MB

router = APIRouter()

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

    # Создаем уникальное имя файла
    unique_id = str(uuid.uuid4())[:8]  # Генерируем короткий UUID (8 символов)
    file_extension = os.path.splitext(file.filename)[1]  # Получаем расширение
    new_filename = f"{unique_id}_{file.filename}"  # Уникальное имя файла
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # Сохраняем файл на диск
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    pdf_entry = PDFFile(
        filename=new_filename,
        filepath=file_path,
        user_id=user_data["id"]
    )
    db.add(pdf_entry)
    db.commit()

    return {"message": "Файл загружен", "filename": new_filename}

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

@router.put("/{pdf_id}/set_project")
def set_pdf_project(pdf_id: int, project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    pdf = db.query(PDFFile).filter(PDFFile.id == pdf_id, PDFFile.user_id == user.id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    pdf.project_id = project.id
    db.commit()
    return {"message": "PDF project updated"}