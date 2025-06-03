from typing import List, Optional
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from models.task import Task

class TaskValidationError(Exception):
    """Custom exception for business logic validation"""
    pass

class TaskService:
    """Business logic layer for tasks"""
    
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository
    
    def create_task(self, title: str, user_id: int, description: str = None) -> Task:
        """Create a new task with validation"""
        # Business rule: User must exist
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise TaskValidationError("User not found")
        
        # Business rule: Title cannot be empty
        if not title or title.strip() == "":
            raise TaskValidationError("Task title cannot be empty")
        
        # Business rule: Title must be under 100 characters
        if len(title.strip()) > 100:
            raise TaskValidationError("Task title must be under 100 characters")
        
        return self.task_repository.create_task(title.strip(), user_id, description)
    
    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        """Get all tasks for a specific user"""
        # Business rule: User must exist
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise TaskValidationError("User not found")
        
        return self.task_repository.get_tasks_by_user(user_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks (admin function)"""
        return self.task_repository.get_all_tasks()
    
    def complete_task(self, task_id: int, user_id: int) -> Task:
        """Mark task as completed for specific user"""
        task = self.task_repository.get_task_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskValidationError("Task not found or you don't have permission")
        
        if task.is_completed:
            raise TaskValidationError("Task is already completed")
        
        task.is_completed = True
        return self.task_repository.update_task(task)
    
    def delete_task(self, task_id: int, user_id: int) -> None:
        """Delete a task with business rules for specific user"""
        task = self.task_repository.get_task_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskValidationError("Task not found or you don't have permission")
        
        # Business rule: Cannot delete completed tasks
        if task.is_completed:
            raise TaskValidationError("Cannot delete completed tasks")
        
        self.task_repository.delete_task(task)
