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

@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def auth_token():
    db = next(get_db())
    # Добавляем пользователя напрямую в базу
    test_email = "user2@test.com"
    user = db.query(User).filter(User.email == test_email).first()
    if not user:
        user = User(
            username="user2",
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
@pytest.fixture
def cleanup_users():
    yield
    db = next(get_db())
    db.query(User).filter(User.email.in_([
        "new@example.com",
        "user2@test.com"
    ])).delete(synchronize_session=False)
    db.commit()