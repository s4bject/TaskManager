import pytest
from unittest.mock import Mock
from datetime import date
from src.manager import Manager
from models.models import Task


# Фикстура для мокирования хранилища
@pytest.fixture
def mock_persistence():
    """Фикстура для мокирования хранилища."""
    persistence = Mock()
    persistence.load.return_value = []  # По умолчанию пустое хранилище
    persistence.save.return_value = None
    return persistence


# Фикстура для создания экземпляра менеджера
@pytest.fixture
def manager(mock_persistence):
    """Фикстура для создания экземпляра Manager с мокированным хранилищем."""
    return Manager(mock_persistence)


# Тест добавления задачи
def test_add_task(manager, mock_persistence):
    """Тест добавления задачи."""
    mock_persistence.load.return_value = []  # Обеспечить пустое состояние задач
    manager.tasks = []  # Убедиться, что задачи изначально пусты

    manager.add_task("New Task", "Description", "Work", date(2024, 12, 15), 1)

    # Проверяем, что задача добавлена
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "New Task"
    assert manager.tasks[0].category == "Work"
    assert manager.tasks[0].due_date == date(2024, 12, 15)
    assert manager.tasks[0].priority == 1

    # Проверяем, что метод save был вызван
    mock_persistence.save.assert_called_once()


# Тест удаления задачи по ID
def test_delete_task_by_id(manager, mock_persistence):
    """Тест удаления задачи по ID."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1}
    ]
    manager.tasks = [Task(**mock_persistence.load.return_value[0])]

    result = manager.delete_task("1")
    assert result is True
    assert len(manager.tasks) == 0
    mock_persistence.save.assert_called_once()


# Тест удаления задач по категории
def test_delete_task_by_category(manager, mock_persistence):
    """Тест удаления задач по категории."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1},
        {"id": 2, "title": "Task 2", "description": "Description 2", "category": "Work", "due_date": "2024-12-10", "priority": 2},
    ]
    manager.tasks = [Task(**task) for task in mock_persistence.load.return_value]

    result = manager.delete_task("Work")
    assert result is True
    assert len(manager.tasks) == 0
    mock_persistence.save.assert_called_once()


# Тест поиска задачи по ID
def test_find_task_by_id(manager, mock_persistence):
    """Тест поиска задачи по ID."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1}
    ]
    manager.tasks = [Task(**mock_persistence.load.return_value[0])]

    task = manager.find_task_by_id(1)
    assert task is not None
    assert task.title == "Task 1"


# Тест поиска задач по категории
def test_find_tasks_by_category(manager, mock_persistence):
    """Тест поиска задач по категории."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1},
        {"id": 2, "title": "Task 2", "description": "Description 2", "category": "Home", "due_date": "2024-12-10", "priority": 2},
    ]
    manager.tasks = [Task(**task) for task in mock_persistence.load.return_value]

    tasks = manager.find_tasks("category", "Work")
    assert len(tasks) == 1
    assert tasks[0].title == "Task 1"


# Тест обновления задачи
def test_update_task(manager, mock_persistence):
    """Тест обновления задачи."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1}
    ]
    manager.tasks = [Task(**mock_persistence.load.return_value[0])]

    result = manager.update_task(1, new_title="Updated Task", new_priority=3)
    assert result is True
    task = manager.find_task_by_id(1)
    assert task.title == "Updated Task"
    assert task.priority == 3
    mock_persistence.save.assert_called_once()


# Тест отображения задач
def test_display_tasks(manager, mock_persistence, capsys):
    """Тест отображения задач."""
    mock_persistence.load.return_value = [
        {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": 1}
    ]
    manager.tasks = [Task(**mock_persistence.load.return_value[0])]

    manager.display_tasks()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
