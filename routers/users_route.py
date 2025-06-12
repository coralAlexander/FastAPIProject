from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from utils.security import hash_password
from routers.auth_route import get_current_user



router = APIRouter()

@router.post("/users/", response_model=UserRead)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем поля если переданы
    db_user.username = user_update.username or db_user.username
    db_user.email = user_update.email or db_user.email

    # Если пароль передан → хешируем
    if user_update.password:
        db_user.hashed_password = hash_password(user_update.password)

    db_user.role = user_update.role or db_user.role

    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/users/username/{username}", response_model=UserRead)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.delete("/users/remove/{username}")
def delete_remove_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"detail": "User not found"}
    db.delete(user)
    db.commit()
    return {"detail": f"User {username} deleted"}

