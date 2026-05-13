from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db


from app.models import User
from app.schemas import UserCreate
from app.utils import hash_password, verify_password
from app.auth import create_access_token, create_refresh_token, verify_token


router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"user_id": db_user.id}
    )

    refresh_token = create_refresh_token(
        {"user_id": db_user.id}
    )

    db_user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()

    if user.refresh_token != refresh_token:
        raise HTTPException(status_code=401,detail="Refresh token revoked")

    new_access_token = create_access_token({"user_id": user.id})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
def logout(refresh_token: str,db: Session = Depends(get_db)):
    payload = verify_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()

    user.refresh_token = None
    db.commit()

    return {"message": "Logged out"}
