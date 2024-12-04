from abc import ABC, abstractmethod
import json
from typing import List


class Persistence(ABC):
    """Абстракция для работы с хранилищем задач."""

    @abstractmethod
    def load(self) -> List[dict]:
        """Загружает данные из хранилища."""
        pass

    @abstractmethod
    def save(self, tasks: List[dict]) -> None:
        """Сохраняет данные в хранилище."""
        pass


class JSONPersistence(Persistence):
    """Реализация хранилища на основе JSON-файла."""

    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file: str = storage_file

    def load(self) -> List[dict]:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.storage_file} не найден. Возвращаю пустой список.")
            return []
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON из файла {self.storage_file}: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке данных: {e}")
            return []

    def save(self, tasks: List[dict]) -> None:
        try:
            with open(self.storage_file, "w", encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
        except (TypeError, IOError) as e:
            print(f"Ошибка записи данных в файл {self.storage_file}: {e}")

