from datetime import date
class Task:
    """Модель задачи"""

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        category: str,
        due_date: date,
        priority: str,
        status: str = "не выполнена",
    ):
        self.id: int = id
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self.due_date: date = due_date
        self.priority: str = priority
        self.status: str = status

    def __str__(self) -> str:
        return (
            f"ID: {self.id}, Название: {self.title}, Описание: {self.description}, "
            f"Категория: {self.category}, Срок выполнения: {self.due_date}, "
            f"Приоритет: {self.priority}, Статус: {self.status})"
        )
