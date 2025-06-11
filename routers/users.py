from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database.session import get_db
from models.user import User
from schemas.user import UserCreate, UserRead
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from models.user import User as DBUser
from dependencies.auth import get_current_user



router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Привет, {current_user.username}!"}


@router.post("/users/", response_model=UserRead)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}