import pytest
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash


# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

#Mock for signups 
class MockConn:
    def __init__(self):
        self.executed = False

    def execute(self, query, params):
        self.executed = True
        return None

    def commit(self):
        pass

    def __enter__(self):
        return self  

    def __exit__(self, exc_type, exc, tb):
        pass
    
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
def test_signup_test(client, monkeypatch):
    mock_conn = MockConn()

    monkeypatch.setattr("app.OpenConn", lambda: mock_conn)

    response = client.post("/signup", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=False)

    assert mock_conn.executed is True
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

#Login test
def test_login(client, monkeypatch):
    login_db = {
        "id": 1,
        "username": "testuser",
        "password": generate_password_hash("testuser")
    }

    class MockCursor:
      def fetchone(self):
            return login_db
        
    class MockConn:
      def __enter__(self):
        return self  
      
      def __exit__(self, exc_type, exc, tb):
        pass
          
      def execute(self, query, params):
        return MockCursor()

    monkeypatch.setattr("app.OpenConn", lambda: MockConn())

    response = client.post("/login", data= {
        "username" : "testuser",
        "password" : "testuser"
    }, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")