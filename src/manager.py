from models.models import Task
from datetime import datetime,date
from typing import List, Optional

class Manager:
    """Класс менеджера задач для управления задачами."""

    def __init__(self, persistence):
        self.persistence = persistence
        self.tasks: List[Task] = self.__load_tasks()

    def __load_tasks(self) -> List[Task]:
        try:
            data = self.persistence.load()
            for task in data:
                if "due_date" in task and isinstance(task["due_date"], str):
                    try:
                        task["due_date"] = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    except ValueError:
                        print(f"Ошибка преобразования даты: {task['due_date']}")
            return [Task(**task) for task in data]
        except Exception as e:
            print(f"Ошибка загрузки задач: {e}")
            return []

    def __save_tasks(self) -> None:
        try:
            data = [
                {
                    **task.__dict__,
                    "due_date": task.due_date.isoformat() if isinstance(task.due_date, date) else task.due_date
                }
                for task in self.tasks
            ]
            self.persistence.save(data)
        except Exception as e:
            print(f"Ошибка сохранения задач: {e}")

    def add_task(
        self, title: str, description: str, category: str, due_date: date, priority: str
    ) -> None:
        try:
            new_id = max((task.id for task in self.tasks), default=0) + 1
            new_task = Task(new_id, title, description, category, due_date, priority)
            self.tasks.append(new_task)
            self.__save_tasks()
            print("Задача успешно добавлена.")
        except Exception as e:
            print(f"Ошибка добавления задачи: {e}")

    def delete_task(self, option: str) -> bool:
        try:
            if option.isdigit():
                task_id = int(option)
                task = self.find_task_by_id(task_id)
                if task:
                    self.tasks.remove(task)
                    self.__save_tasks()
                    print(f"Задача с ID {task_id} удалена.")
                    return True
                else:
                    print(f"Задача с ID {task_id} не найдена.")
                    return False
            else:
                tasks = self.find_tasks("category", option)
                if tasks:
                    for task in tasks:
                        self.tasks.remove(task)
                    self.__save_tasks()
                    print(f"Все задачи в категории '{option}' удалены.")
                    return True
                else:
                    print(f"Задачи в категории '{option}' не найдены.")
                    return False
        except Exception as e:
            print(f"Ошибка удаления задачи: {e}")
            return False

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        try:
            for task in self.tasks:
                if task.id == task_id:
                    return task
            return None
        except Exception as e:
            print(f"Ошибка поиска задачи по ID: {e}")
            return None

    def find_tasks(self, key: str, value: str) -> List[Task]:
        try:
            key = key.lower()
            value = value.lower()
            if key == "category":
                return [task for task in self.tasks if value == task.category.lower()]
            elif key == "status":
                return [task for task in self.tasks if value == task.status.lower()]
            elif key == "title":
                return [task for task in self.tasks if value in task.title.lower()]
            else:
                print(f"Неизвестный ключ поиска: {key}")
                return []
        except Exception as e:
            print(f"Ошибка поиска задач: {e}")
            return []

    def update_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_category: Optional[str] = None,
        new_due_date: Optional[date] = None,
        new_priority: Optional[str] = None,
        new_status: Optional[str] = None,
    ) -> bool:
        try:
            task = self.find_task_by_id(task_id)
            if task:
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                if new_category:
                    task.category = new_category
                if new_due_date:
                    task.due_date = new_due_date
                if new_priority:
                    task.priority = new_priority
                if new_status:
                    task.status = new_status
                self.__save_tasks()
                print(f"Задача с ID {task_id} обновлена.")
                return True
            else:
                print(f"Задача с ID {task_id} не найдена.")
                return False
        except Exception as e:
            print(f"Ошибка обновления задачи: {e}")
            return False

    def display_tasks(self, tasks: Optional[List[Task]] = None) -> None:
        try:
            tasks = tasks if tasks is not None else self.tasks
            if not tasks:
                print("Нет задач для отображения.")
                return
            for task in tasks:
                print(task)
        except Exception as e:
            print(f"Ошибка отображения задач: {e}")
