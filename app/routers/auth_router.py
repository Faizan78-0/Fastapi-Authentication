from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime,timedelta, timezone

from app.models import User
from app.schemas import UserCreate, VerifyOPT, ForgotPasswordRequest
from app.utils import hash_password, verify_password, genrate_otp
from app.auth import create_access_token, create_refresh_token, verify_token
from app.tasks import send_welcome_email, send_opt_email


router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register", status_code=201)
def register(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_tasks.add_task(send_welcome_email, new_user.email)

    return {"message": "User created successfully", "user":new_user.email}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

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


@router.post("/forgot_password")
def forgot_password( data: ForgotPasswordRequest,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    
    opt = genrate_otp()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    user.otp_code = opt
    user.otp_expiry = expiry

    db.commit()

    background_tasks.add_task(send_opt_email, user.email, opt)
    return { "message": "OPT sent to email"}


@router.post("/reset_password")
def reset_password(data: VerifyOPT, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    if user.otp_code != data.opt:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if datetime.now() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OPT expired")
    
   
    
    

    user.hashed_password = hash_password(data.new_password)
    user.otp_code = None
    user.otp_expiry = None
    
    db.commit()
    return { "message": "Password reset successful"}
 
    

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
