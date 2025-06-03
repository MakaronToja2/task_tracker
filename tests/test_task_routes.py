import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base, get_db
from main import app

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestTaskRoutes:
    """Integration tests for Task API endpoints"""
    
    def setup_method(self):
        """Setup for each test"""
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
        
        # Create a test user for task operations
        user_response = self.client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test@example.com"}
        )
        self.user_id = user_response.json()["id"]
    
    def teardown_method(self):
        """Cleanup after each test"""
        Base.metadata.drop_all(bind=engine)
    
    def test_create_task_success(self):
        """Test successful task creation via API"""
        response = self.client.post(
            "/api/tasks/",
            json={"title": "Test Task", "description": "Test Description", "user_id": self.user_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["user_id"] == self.user_id
        assert data["is_completed"] == False
    
    def test_create_task_invalid_user_fails(self):
        """Test creating task with invalid user fails"""
        response = self.client.post(
            "/api/tasks/",
            json={"title": "Test Task", "user_id": 999}
        )
        assert response.status_code == 400
        assert "User not found" in response.json()["detail"]
    
    def test_get_user_tasks(self):
        """Test getting tasks for specific user"""
        # Create a task
        self.client.post("/api/tasks/", json={"title": "Test Task", "user_id": self.user_id})
        
        # Get user's tasks
        response = self.client.get(f"/api/tasks/user/{self.user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"
    
    def test_complete_task_success(self):
        """Test completing a task"""
        # Create a task
        create_response = self.client.post(
            "/api/tasks/", 
            json={"title": "Test Task", "user_id": self.user_id}
        )
        task_id = create_response.json()["id"]
        
        # Complete the task
        response = self.client.put(f"/api/tasks/{task_id}/complete?user_id={self.user_id}")
        assert response.status_code == 200
        assert response.json()["is_completed"] == True
    
    def test_delete_task_success(self):
        """Test deleting a task"""
        # Create a task
        create_response = self.client.post(
            "/api/tasks/", 
            json={"title": "Test Task", "user_id": self.user_id}
        )
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = self.client.delete(f"/api/tasks/{task_id}?user_id={self.user_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
