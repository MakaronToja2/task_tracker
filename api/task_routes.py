from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connection import get_db
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from services.task_service import TaskService, TaskValidationError

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# DTOs (Data Transfer Objects)
class TaskCreate(BaseModel):
    title: str
    description: str = None
    user_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    user_id: int
    
    class Config:
        from_attributes = True

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency injection for task service"""
    task_repository = TaskRepository(db)
    user_repository = UserRepository(db)
    return TaskService(task_repository, user_repository)

@router.post("/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, service: TaskService = Depends(get_task_service)):
    """Create a new task"""
    try:
        task = service.create_task(task_data.title, task_data.user_id, task_data.description)
        return task
    except TaskValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks (admin function)"""
    return service.get_all_tasks()

@router.get("/user/{user_id}", response_model=List[TaskResponse])
def get_user_tasks(user_id: int, service: TaskService = Depends(get_task_service)):
    """Get all tasks for a specific user"""
    try:
        return service.get_tasks_by_user(user_id)
    except TaskValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, user_id: int, service: TaskService = Depends(get_task_service)):
    """Mark task as completed for specific user"""
    try:
        task = service.complete_task(task_id, user_id)
        return task
    except TaskValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int, service: TaskService = Depends(get_task_service)):
    """Delete a task for specific user"""
    try:
        service.delete_task(task_id, user_id)
        return {"message": "Task deleted successfully"}
    except TaskValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
