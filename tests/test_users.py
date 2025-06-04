# tests/test_users.py
from fastapi.testclient import TestClient
from main import app  # Убедись, что это путь к твоему FastAPI приложению

client = TestClient(app)

def test_create_user(auth_token):
    response = client.post(
        "/auth/users/",
        headers={"Authorization": auth_token},
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200 or response.status_code == 201
