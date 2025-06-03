from typing import List, Optional
from sqlalchemy.orm import Session
from models.task import Task

class TaskRepository:
    """Data access layer for tasks"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, title: str, user_id: int, description: str = None) -> Task:
        """Create a new task for a specific user"""
        task = Task(title=title, description=description, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.db.query(Task).all()
    
    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        """Get all tasks for a specific user"""
        return self.db.query(Task).filter(Task.user_id == user_id).all()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_task_by_id_and_user(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get task by ID for specific user"""
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    def update_task(self, task: Task) -> Task:
        """Update task"""
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task: Task) -> None:
        """Delete task"""
        self.db.delete(task)
        self.db.commit()
