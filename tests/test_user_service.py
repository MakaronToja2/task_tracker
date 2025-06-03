import pytest
from unittest.mock import Mock
from services.user_service import UserService, UserValidationError
from models.user import User

class TestUserService:
    """Unit tests for UserService (Business Logic Layer)"""
    
    def setup_method(self):
        """Setup for each test"""
        self.mock_repository = Mock()
        self.service = UserService(self.mock_repository)
    
    def test_create_user_success(self):
        """Test successful user creation"""
        # Arrange
        self.mock_repository.get_user_by_username.return_value = None
        self.mock_repository.get_user_by_email.return_value = None
        self.mock_repository.create_user.return_value = User(id=1, username="testuser", email="test@example.com")
        
        # Act
        result = self.service.create_user("testuser", "test@example.com")
        
        # Assert
        self.mock_repository.create_user.assert_called_once_with("testuser", "test@example.com")
        assert result.username == "testuser"
    
    def test_create_user_empty_username_raises_error(self):
        """Test that empty username raises validation error"""
        with pytest.raises(UserValidationError, match="Username cannot be empty"):
            self.service.create_user("", "test@example.com")
    
    def test_create_user_duplicate_username_raises_error(self):
        """Test that duplicate username raises validation error"""
        # Arrange
        self.mock_repository.get_user_by_username.return_value = User(id=1, username="existing")
        
        # Act & Assert
        with pytest.raises(UserValidationError, match="Username already exists"):
            self.service.create_user("existing", "test@example.com")
    
    def test_create_user_duplicate_email_raises_error(self):
        """Test that duplicate email raises validation error"""
        # Arrange
        self.mock_repository.get_user_by_username.return_value = None
        self.mock_repository.get_user_by_email.return_value = User(id=1, email="existing@example.com")
        
        # Act & Assert
        with pytest.raises(UserValidationError, match="Email already exists"):
            self.service.create_user("newuser", "existing@example.com")
    
    def test_create_user_invalid_email_raises_error(self):
        """Test that invalid email raises validation error"""
        with pytest.raises(UserValidationError, match="Invalid email format"):
            self.service.create_user("testuser", "invalid-email")
