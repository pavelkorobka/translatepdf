from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.pdf import PDFFile
from app.models.project import Project
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/{name}")
def create_project(name: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_project = Project(name=name, user_id=user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/")
def get_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Project).filter(Project.user_id == user.id).all()

@router.put("{project_id}/{name}")
def update_project(project_id: int, name: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.name = name
    db.commit()
    return {"message": "Project updated"}

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}

@router.delete("/")
def delete_all_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    db.query(Project).filter(Project.user_id == user.id).delete()
    db.commit()
    return {"message": "All projects deleted"}