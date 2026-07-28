from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_register():

    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code in [200, 400]


def test_login():

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code in [200, 401]


def test_create_session():

    response = client.post(
        "/session",
        json={
            "title": "My First Chat"
        }
    )

    assert response.status_code == 200


def test_chat():

    response = client.post(
        "/chat",
        json={
            "session_id": 1,
            "message": "Hello Gemini!"
        }
    )

    assert response.status_code == 200