from sqlalchemy import Column, Integer, String
from models.base import Base  # Наш общий declarative_base()
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))  # ✅ правильно
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)  # ✅ новое поле
