import pytest
from unittest.mock import Mock
from services.task_service import TaskService, TaskValidationError
from models.task import Task
from models.user import User

class TestTaskService:
    """Unit tests for TaskService (Business Logic Layer)"""
    
    def setup_method(self):
        """Setup for each test"""
        self.mock_task_repository = Mock()
        self.mock_user_repository = Mock()
        self.service = TaskService(self.mock_task_repository, self.mock_user_repository)
    
    def test_create_task_success(self):
        """Test successful task creation"""
        # Arrange
        user = User(id=1, username="testuser", email="test@example.com")
        self.mock_user_repository.get_user_by_id.return_value = user
        self.mock_task_repository.create_task.return_value = Task(id=1, title="Test Task", user_id=1)
        
        # Act
        result = self.service.create_task("Test Task", 1, "Description")
        
        # Assert
        self.mock_task_repository.create_task.assert_called_once_with("Test Task", 1, "Description")
        assert result.title == "Test Task"
    
    def test_create_task_user_not_found_raises_error(self):
        """Test that non-existent user raises validation error"""
        # Arrange
        self.mock_user_repository.get_user_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="User not found"):
            self.service.create_task("Test Task", 999)
    
    def test_create_task_empty_title_raises_error(self):
        """Test that empty title raises validation error"""
        # Arrange
        user = User(id=1, username="testuser", email="test@example.com")
        self.mock_user_repository.get_user_by_id.return_value = user
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="Task title cannot be empty"):
            self.service.create_task("", 1)
    
    def test_get_tasks_by_user_success(self):
        """Test getting tasks for specific user"""
        # Arrange
        user = User(id=1, username="testuser", email="test@example.com")
        tasks = [Task(id=1, title="Task 1", user_id=1), Task(id=2, title="Task 2", user_id=1)]
        self.mock_user_repository.get_user_by_id.return_value = user
        self.mock_task_repository.get_tasks_by_user.return_value = tasks
        
        # Act
        result = self.service.get_tasks_by_user(1)
        
        # Assert
        assert len(result) == 2
        self.mock_task_repository.get_tasks_by_user.assert_called_once_with(1)
    
    def test_complete_task_success(self):
        """Test successful task completion"""
        # Arrange
        task = Task(id=1, title="Test Task", user_id=1, is_completed=False)
        self.mock_task_repository.get_task_by_id_and_user.return_value = task
        self.mock_task_repository.update_task.return_value = task
        
        # Act
        result = self.service.complete_task(1, 1)
        
        # Assert
        assert result.is_completed == True
        self.mock_task_repository.update_task.assert_called_once()
    
    def test_complete_task_not_owner_raises_error(self):
        """Test completing task not owned by user raises error"""
        # Arrange
        self.mock_task_repository.get_task_by_id_and_user.return_value = None
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="Task not found or you don't have permission"):
            self.service.complete_task(1, 999)
    
    def test_delete_completed_task_raises_error(self):
        """Test that deleting completed task raises error"""
        # Arrange
        task = Task(id=1, title="Test Task", user_id=1, is_completed=True)
        self.mock_task_repository.get_task_by_id_and_user.return_value = task
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="Cannot delete completed tasks"):
            self.service.delete_task(1, 1)
