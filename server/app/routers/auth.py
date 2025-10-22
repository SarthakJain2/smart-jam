from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..db import get_db
from .. import models, schemas
from ..security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
)
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------- REGISTER ----------------------
@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email, hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------------- LOGIN ----------------------
@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(user.email, settings.JWT_SECRET)
    refresh = create_refresh_token(user.email, settings.JWT_REFRESH_SECRET)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


# ---------------------- REFRESH TOKEN ----------------------
@router.post("/refresh", response_model=schemas.Token)
def refresh_token(req: schemas.RefreshIn, db: Session = Depends(get_db)):
    payload = decode_token(req.refresh_token, settings.JWT_REFRESH_SECRET)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access = create_access_token(email, settings.JWT_SECRET)
    refresh = create_refresh_token(email, settings.JWT_REFRESH_SECRET)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


# ---------------------- FORGOT PASSWORD ----------------------
@router.post("/forgot-password")
def forgot_password(
    req: schemas.ForgotPasswordIn,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if user:
        token = create_reset_token(user.email, settings.JWT_RESET_SECRET)
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(minutes=30)
        db.commit()
        background.add_task(
            print, f"[RESET LINK] http://localhost:5173/reset-password?token={token}"
        )
    return {"detail": "If that email exists, a reset link has been sent."}


# ---------------------- RESET PASSWORD ----------------------
@router.post("/reset-password")
def reset_password(req: schemas.ResetPasswordIn, db: Session = Depends(get_db)):
    payload = decode_token(req.token, settings.JWT_RESET_SECRET)
    if not payload or payload.get("type") != "reset":
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if (
        not user
        or user.reset_token != req.token
        or not user.reset_token_expires
        or user.reset_token_expires < datetime.utcnow()
    ):
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.hashed_password = get_password_hash(req.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    return {"detail": "Password updated"}
