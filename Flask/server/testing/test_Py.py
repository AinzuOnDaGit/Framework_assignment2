import pytest
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
import io


# Ensure project is in path of file location
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#App.py importing
from app import app

#MockUp for signups 
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
      
      def fetchall(self):
         return []
        
    class MockConn:
      def __enter__(self):
        return self  
      
      def __exit__(self, exc_type, exc, tb):
        pass
          
      def execute(self, query, params=None):
        return MockCursor()

    monkeypatch.setattr("app.OpenConn", lambda: MockConn())

    response = client.post("/login", data= {
        "username" : "testuser",
        "password" : "testuser"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Swal.fire" in response.data
    assert b"Logged in successfully!" in response.data
    assert b"success" in response.data

#Login Test failed
def test_fail_login(client, monkeypatch):
    login_db = {
        "id": 1,
        "username": "testuser1",
        "password": generate_password_hash("testuser1")
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
        "username" : "testuser1",
        "password" : "testuser2"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Swal.fire" in response.data
    assert b"Invalid username or password" in response.data
    assert b"error" in response.data

#Logging out
def test_logout(client):
    response = client.get("/logout_post", follow_redirects=True)

    assert response.status_code == 200
    assert b"Swal.fire" in response.data
    assert b"Logged out successfully!" in response.data
    assert b"info" in response.data 

#Direct to post (Post on Dover)
def test_viewPost(client):
   response = client.get("/post/2")
   assert response.status_code == 200

#Directing to create post location
def test_create_directory(client):
   response = client.get("/addPost")

   assert response.status_code == 200
   assert b"New Post" in response.data 

def test_create_post(client):
   response = client.post("/addPost", data={
      "title": "TestTitle",
      "description": "TestDescription",
      "image": (io.BytesIO(b"fakeimg"), "fake.png")
   }, content_type="multipart/form-data", follow_redirects=True)
   assert response.status_code == 200
   assert b"TestTitle" in response.data
   assert b"TestDescription" in response.data
