import pytest
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

#Mock for signups 
class MockConn:
    def __init__(self):
        self.executed = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

#If Title has CCCU Blog it (Pass)
def test_get_items(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CCCU Blog It" in response.data

#Sign up Test 
def test_signup_success(client, monkeypatch):
    mock_conn = MockConn()

    # Mock OpenConn so it returns our fake DB connection
    monkeypatch.setattr("app.OpenConn", lambda: mock_conn)

    response = client.post("/signup", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=False)

    # Check DB insert was attempted
    assert mock_conn.executed is True

    # Check redirect to login page
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]