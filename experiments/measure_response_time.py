"""
Эксперимент 1: Замер времени отклика системы
=============================================
Измеряет время от отправки запроса к языковой модели
до получения ответа для файлов разного размера.

Соответствует разделу 4.2 дипломной работы.

Использование:
    pip install openai python-dotenv
    python measure_response_time.py

Настройка:
    Создайте файл .env со следующими переменными:
    API_BASE_URL=https://openrouter.ai/api/v1
    API_KEY=your-api-key-here
    MODEL_NAME=meta-llama/llama-3.2-3b-instruct:free
"""

import time
import os
import statistics
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения из server/.env
load_dotenv(dotenv_path=os.path.join("..", ".env"))

API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-3.2-3b-instruct:free")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "https://github.com/StudentAI",
        "X-Title": "Student AI Helper",
    }
)

# Системный промпт — копия из server.ts
SYSTEM_PROMPT = """
    Ты — опытный, терпеливый преподаватель Python и наставник для новичков.
    Твоя задача — найти главную ошибку или логическую недоработку в коде студента.
    Все объяснения пиши только на русском языке.
    Пользователь пришлет код с номерами строк.

    ПРАВИЛА ДЛЯ ФОРМИРОВАНИЯ ПОДСКАЗКИ (поле "message"):
    1. КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ дублировать стандартные ошибки интерпретатора Python.
    2. Объясни суть проблемы простым, человеческим языком.
    3. Кратко объясни ПОЧЕМУ это важно.
    4. Дай наводящий совет, как это исправить, но НЕ пиши сам исправленный код.
    5. Объем сообщения: 2-3 ясных предложения.

    Ты ДОЛЖЕН ответить СТРОГО в формате JSON без markdown разметки и лишнего текста:
    {
    "hasError": true или false,
    "line": <номер строки с ошибкой (число)>,
    "message": "<подробное педагогическое объяснение ошибки и совет>",
    "suggestedCode": "<исправленный фрагмент кода или null>"
    }
    Если ошибок нет, верни {"hasError": false}.
"""

# Тестовые файлы разного размера из тестовой базы
TEST_FILES = {
    10:  os.path.join("..", "tests", "syntax", "syntax_01.py"),
    30:  os.path.join("..", "tests", "syntax", "syntax_04.py"),
    50:  os.path.join("..", "tests", "syntax", "syntax_07.py"),
    100: os.path.join("..", "tests", "syntax", "syntax_10.py"),
}

ATTEMPTS = 5  # Количество замеров для каждого размера файла


def read_and_number_lines(filepath: str) -> str:
    """Читает файл и нумерует строки — точно как в server.ts."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    numbered = [f"{i}: {line.rstrip()}" for i, line in enumerate(lines)]
    return "\n".join(numbered)


def measure_single_request(numbered_code: str) -> float:
    """
    Выполняет один запрос к модели и возвращает время в секундах.
    Отсчёт начинается перед запросом, заканчивается после получения ответа —
    аналогично меткам в серверном логе (connection.console.log).
    """
    start = time.perf_counter()

    client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": numbered_code}
        ],
        timeout=15
    )

    end = time.perf_counter()
    return round(end - start, 3)


def run_experiment():
    print("=" * 60)
    print("Эксперимент 1: Замер времени отклика системы")
    print(f"Модель: {MODEL_NAME}")
    print(f"Провайдер: {API_BASE_URL}")
    print(f"Количество замеров на размер файла: {ATTEMPTS}")
    print("=" * 60)

    results = {}

    for size, filepath in TEST_FILES.items():
        if not os.path.exists(filepath):
            print(f"[!] Файл не найден: {filepath}")
            continue

        numbered_code = read_and_number_lines(filepath)
        actual_lines = len(numbered_code.split("\n"))
        print(f"\nРазмер файла: ~{size} строк (фактически: {actual_lines})")
        print(f"Файл: {filepath}")

        times = []
        for attempt in range(1, ATTEMPTS + 1):
            try:
                elapsed = measure_single_request(numbered_code)
                times.append(elapsed)
                print(f"  Попытка {attempt}: {elapsed:.3f} с")
            except Exception as e:
                print(f"  Попытка {attempt}: ОШИБКА — {e}")

        if times:
            avg = round(statistics.mean(times), 2)
            min_t = round(min(times), 2)
            max_t = round(max(times), 2)
            results[size] = avg
            print(f"  → Среднее: {avg} с | Мин: {min_t} с | Макс: {max_t} с")

    print("\n" + "=" * 60)
    print("Итоговая таблица результатов:")
    print(f"{'Размер файла, строк':<25} {'Среднее время, с':<20}")
    print("-" * 45)
    for size, avg in sorted(results.items()):
        print(f"{size:<25} {avg:<20}")
    print("=" * 60)


if __name__ == "__main__":
    run_experiment()
