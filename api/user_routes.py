from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connection import get_db
from repositories.user_repository import UserRepository
from services.user_service import UserService, UserValidationError

router = APIRouter(prefix="/api/users", tags=["users"])

# DTOs (Data Transfer Objects)
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

class UserWithTasksResponse(BaseModel):
    id: int
    username: str
    email: str
    task_count: int
    
    class Config:
        from_attributes = True

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency injection for user service"""
    repository = UserRepository(db)
    return UserService(repository)

@router.post("/", response_model=UserResponse)
# Dependency relationship example
def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)): #UserRoutes DEPENDS ON UserService
    """Create a new user"""
    try:
        user = service.create_user(user_data.username, user_data.email) ##  UserRoutes USES UserService method
        return user
    except UserValidationError as e:
        ##  UserRoutes knows about UserService except
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserWithTasksResponse])
def get_all_users(service: UserService = Depends(get_user_service)):
    """Get all users with task count"""
    users = service.get_all_users()
    return [
        UserWithTasksResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            task_count=len(user.tasks)
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Get user by ID"""
    try:
        user = service.get_user_by_id(user_id)
        return user
    except UserValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))
