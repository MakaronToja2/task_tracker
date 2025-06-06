from typing import List, Optional
from repositories.user_repository import UserRepository
from models.user import User

class UserValidationError(Exception):
    """Custom exception for user business logic validation"""
    pass

class UserService:
    """Business logic layer for users"""
    
   # Association example
    def __init__(self, repository: UserRepository):
        #UserService stores reference
        self.repository = repository
    
    def create_user(self, username: str, email: str) -> User:
        ## UserService USES its repository
        """Create a new user with validation"""
        # Business rule: Username cannot be empty
        if not username or username.strip() == "":
            raise UserValidationError("Username cannot be empty")
        
        # Business rule: Username must be unique
        existing_user = self.repository.get_user_by_username(username.strip())
        #Direct method call on stored reference
        if existing_user:
            raise UserValidationError("Username already exists")
        
        # Business rule: Email must be unique
        existing_email = self.repository.get_user_by_email(email.strip())
        if existing_email:
            raise UserValidationError("Email already exists")
        
        # Business rule: Basic email validation
        if not email or "@" not in email:
            raise UserValidationError("Invalid email format")
        
        return self.repository.create_user(username.strip(), email.strip())
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.repository.get_all_users()
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID with validation"""
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserValidationError("User not found")
        return user
