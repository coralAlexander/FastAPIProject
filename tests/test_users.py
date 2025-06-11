# tests/test_users.py
from fastapi.testclient import TestClient
from main import app  # Убедись, что это путь к твоему FastAPI приложению

client = TestClient(app)

def test_create_user(auth_token,cleanup_users):
    response = client.post(
        "/users/",
        headers={"Authorization": auth_token},
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "123456",
            "role": "admin"
        }
    )
    assert response.status_code in [200, 201]

    response_data = response.json()

    assert "id" in response_data and isinstance(response_data["id"], int)
    assert response_data["username"] == "newuser"
    assert response_data["email"] == "new@example.com"
    assert response_data["role"] == "admin"
