# Задание: контекстный менеджер для работы с CSV-файлами

import csv
import os
from datetime import datetime


class CSVManager:
    def __enter__(self)
        self.data = []
        self.errors = []
        self.start_time = datetime.now()
        print(f"[{self.start_time}] Начало работы с CSV")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        print(f"[{end_time}] Завершение работы. Время: {duration:.3f} сек.")

        if exc_type is not None:
            self.errors.append(str(exc_val))
            print(f"Ошибка: {exc_val}")
            return True

        return False

    def load(self, filepath, delimiter=","):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            self.data = [row for row in reader]

        print(f"Загружено строк: {len(self.data)}")
        return self

    def filter_rows(self, column, value):
        self.data = [row for row in self.data if row.get(column) == value]
        return self

    def add_column(self, column_name, func):
        for row in self.data:
            row[column_name] = func(row)
        return self

    def save(self, filepath, delimiter=","):
        if not self.data:
            print("Нет данных для сохранения")
            return self

        fieldnames = list(self.data[0].keys())

        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(self.data)

        print(f"Сохранено строк: {len(self.data)}")
        return self

    def summary(self):
        print(f"Строк в наборе: {len(self.data)}")
        if self.data:
            print(f"Колонки: {list(self.data[0].keys())}")
        if self.errors:
            print(f"Ошибок при обработке: {len(self.errors)}")


def __init__(self, filepath=None):
    self.filepath = filepath


sample_data = [
    {"name": "Анна", "grade": "5", "subject": "Математика"},
    {"name": "Борис", "grade": "3", "subject": "Физика"},
    {"name": "Виктор", "grade": "4", "subject": "Математика"},
    {"name": "Галина", "grade": "5", "subject": "Математика"},
]

test_file = "test_grades.csv"
with open(test_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "grade", "subject"])
    writer.writeheader()
    writer.writerows(sample_data)

with CSVManager() as manager:
    manager.load(test_file)
    manager.filter_rows("subject", "Математика")
    manager.add_column("passed", lambda row: "Да" if int(row["grade"]) >= 4 else "Нет")
    manager.summary()

os.remove(test_file)
