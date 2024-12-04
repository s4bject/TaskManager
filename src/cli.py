from datetime import datetime
from typing import List, Optional, Union

class TaskManagerCLI:
    """Интерфейс командной строки для управления задачами."""

    def __init__(self, manager):
        self.manager = manager

    def run(self):
        """Запуск CLI."""

        search_field_map = {
            "категория": "category",
            "статус": "status",
            "название": "title"
        }

        while True:
            print("\nДоступные команды:")
            print("1. Добавить задачу")
            print("2. Удалить задачу")
            print("3. Найти задачи")
            print("4. Отобразить все задачи")
            print("5. Изменить задачу")
            print("6. Выйти")

            command = input("Введите номер команды: ").strip()

            try:
                if command == "1":
                    title = input("Название: ").strip()
                    if not title:
                        print("Название не может быть пустым.")
                        continue

                    description = input("Описание: ").strip()
                    if not description:
                        print("Описание не может быть пустым.")
                        continue

                    category = input("Категория: ").strip()
                    if not category:
                        print("Категория не может быть пустой.")
                        continue

                    due_date = input("Срок выполнения (YYYY-MM-DD): ").strip()
                    try:
                        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                    except ValueError:
                        print("Некорректная дата. Используйте формат YYYY-MM-DD.")
                        continue

                    priority = input("Приоритет (низкий, средний, высокий): ").strip().lower()
                    if priority not in ['низкий', 'средний', 'высокий']:
                        print("Некорректный приоритет. Используйте: низкий, средний, высокий.")
                        continue

                    self.manager.add_task(title, description, category, due_date, priority)

                elif command == "2":
                    sub_command = input("Введите 1, чтобы удалить задачу по ID или 2, чтобы удалить по категории: ").strip()
                    if sub_command == "1":
                        task_id_input = input("ID задачи: ").strip()
                        if not task_id_input.isdigit():
                            print("ID задачи должно быть числом.")
                            continue
                        task_id = task_id_input
                        self.manager.delete_task(task_id)
                    elif sub_command == "2":
                        category = input("Категория: ").strip()
                        if not category:
                            print("Категория не может быть пустой.")
                            continue
                        self.manager.delete_task(category)
                    else:
                        print("Недопустимая подкоманда. Попробуйте снова.")

                elif command == "3":
                    field_ru = input("Поле для поиска (категория, статус, название): ").strip().lower()
                    field_en = search_field_map.get(field_ru)

                    if not field_en:
                        print("Недопустимое поле для поиска. Используйте: категория, статус, название.")
                        continue

                    value = input("Значение: ").strip()
                    if not value:
                        print("Значение для поиска не может быть пустым.")
                        continue

                    results = self.manager.find_tasks(field_en, value)
                    self.manager.display_tasks(results)

                elif command == "4":
                    self.manager.display_tasks()

                elif command == "5":
                    task_id_input = input("ID задачи: ").strip()
                    if not task_id_input.isdigit():
                        print("ID задачи должно быть числом.")
                        continue
                    task_id = int(task_id_input)

                    title = input("Новое название (нажмите Enter, чтобы пропустить): ").strip()
                    description = input("Новое описание (нажмите Enter, чтобы пропустить): ").strip()
                    category = input("Новая категория (нажмите Enter, чтобы пропустить): ").strip()

                    due_date = input("Новый срок выполнения (YYYY-MM-DD, нажмите Enter, чтобы пропустить): ").strip()
                    if due_date:
                        try:
                            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                        except ValueError:
                            print("Некорректная дата. Используйте формат YYYY-MM-DD.")
                            continue

                    priority = input("Новый приоритет (низкий, средний, высокий, нажмите Enter, чтобы пропустить): ").strip().lower()
                    if priority and priority not in ['низкий', 'средний', 'высокий']:
                        print("Некорректный приоритет.")
                        continue

                    status = input("Новый статус (выполнена, не выполнена, нажмите Enter, чтобы пропустить): ").strip().lower()
                    if status and status not in ['выполнена', 'не выполнена']:
                        print("Некорректный статус.")
                        continue

                    self.manager.update_task(
                        task_id,
                        new_title=title or None,
                        new_description=description or None,
                        new_category=category or None,
                        new_due_date=due_date or None,
                        new_priority=priority or None,
                        new_status=status or None
                    )

                elif command == "6":
                    print("Выход из программы.")
                    break

                else:
                    print("Недопустимая команда. Попробуйте снова.")
            except Exception as e:
                print(f"Ошибка: {e}")
