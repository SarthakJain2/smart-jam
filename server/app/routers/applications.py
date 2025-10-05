from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationOut)
def create_app(payload: schemas.ApplicationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = models.Application(user_id=user.id, **payload.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("/", response_model=List[schemas.ApplicationOut])
def list_apps(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Application).filter(models.Application.user_id == user.id).order_by(models.Application.date_applied.desc()).all()

@router.put("/{app_id}", response_model=schemas.ApplicationOut)
def update_app(app_id: int, payload: schemas.ApplicationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    for k, v in payload.model_dump().items():
        setattr(app, k, v)
    db.commit()
    db.refresh(app)
    return app

@router.delete("/{app_id}")
def delete_app(app_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
    return {"ok": True}