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

class TestUserRoutes:
    """Integration tests for User API endpoints"""
    
    def setup_method(self):
        """Setup for each test"""
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
    
    def teardown_method(self):
        """Cleanup after each test"""
        Base.metadata.drop_all(bind=engine)
    
    def test_create_user_success(self):
        """Test successful user creation via API"""
        response = self.client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_create_user_duplicate_username_fails(self):
        """Test creating user with duplicate username fails"""
        # Create first user
        self.client.post("/api/users/", json={"username": "testuser", "email": "test1@example.com"})
        
        # Try to create duplicate
        response = self.client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test2@example.com"}
        )
        assert response.status_code == 400
        assert "Username already exists" in response.json()["detail"]
    
    def test_get_all_users(self):
        """Test getting all users"""
        # Create a user first
        self.client.post("/api/users/", json={"username": "testuser", "email": "test@example.com"})
        
        # Get all users
        response = self.client.get("/api/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == "testuser"
        assert data[0]["task_count"] == 0
