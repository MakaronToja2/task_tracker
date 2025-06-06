from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    """Data access layer for users"""
    
    def __init__(self, db: Session):
        self.db = db
        ## Aggregation - Repository uses Session for all operations
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user"""
        user = User(username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
        ##  All operations go through contained session
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
