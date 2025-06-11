import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from main import app
from database.session import Base, get_db, DATABASE_URL
from models.user import User
from utils.security import hash_password
from utils.jwt import create_access_token

# Создание движка и сессии
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц
Base.metadata.create_all(bind=engine)


# Переопределение get_db для FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Подмена зависимостей FastAPI
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def auth_token():
    db = next(override_get_db())
    # Добавляем пользователя напрямую в базу
    test_email = "user1@test.com"
    user = db.query(User).filter(User.email == test_email).first()
    if not user:
        user = User(
            username="user1",
            email=test_email,
            hashed_password=hash_password("123456"),
            role="admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": user.email})
    return f"Bearer {token}"


# Очистка пользователей перед каждым тестом
@pytest.fixture(autouse=True)
def clean_users():
    db = next(override_get_db())
    db.query(User).delete()
    db.commit()
