# Задание: логгер событий с записью в файл

import os
from datetime import datetime


class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.log_count = 0

    def _write(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}\n"

        with open(self.filename, "a", encoding="utf-8") as f:
        f.write(entry)
        self.log_count += 1

    def info(self, message):
        self._write("INFO", message)

    def warning(self, message):
        self._write("WARNING", message)

    def error(self, message):
        self._write("ERROR", message)

    def read_logs(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.readlines()

    def clear(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.log_count = 0

    def summary(self):
        logs = self.read_logs()
        levels = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        for log in logs:
            for level in levels:
                if f"[{level}]" in log:
                    levels[level] += 1
        return levels


logger = Logger("app.log")
logger.info("Приложение запущено")
logger.warning("Низкий заряд батареи")
logger.error("Соединение с базой данных потеряно")
logger.info("Попытка переподключения")
logger.info("Соединение восстановлено")

print(f"Всего записей: {logger.log_count}")
summary = logger.summary()
for level, count in summary.items():
    print(f"  {level}: {count}")

logger.clear()
