from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db

from app.oauth2 import  get_current_user, require_role

from app.models import User
from app.schemas import UserOut, UserUpdate
from app.utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.email:
        current_user.email = data.email

    if data.password:
        current_user.hashed_password = hash_password(
            data.password
        )

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/", response_model=list[UserOut])
def get_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    return db.query(User).options(joinedload(User.posts)).all()


@router.delete("/{id}")
def deactivate_user(id: int, db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = False
    db.commit()

    return {"message": "User deactivated"}


@router.post("/{id}/activate")
def activate_user(id: int, db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()

    return {"message": "User activated"}
