"""
Эксперимент 2: Замер точности локализации ошибок
=================================================
Проверяет, насколько точно языковая модель определяет
номер строки с ошибкой для каждой категории тестовых файлов.

Соответствует разделу 4.3 дипломной работы.

Использование:
    pip install openai python-dotenv
    python measure_accuracy.py
"""

import os
import json
import statistics
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("..", ".env"))

API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b:free")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "https://github.com/StudentAI",
        "X-Title": "Student AI Helper",
    }
)

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

# Словарь: файл -> правильный номер строки с ошибкой
# Номера строк соответствуют нумерации с 0 (как в server.ts)
EXPECTED_LINES = {
    # Синтаксические ошибки
    os.path.join("..", "tests", "syntax", "syntax_01.py"): 2,
    os.path.join("..", "tests", "syntax", "syntax_02.py"): 5,
    os.path.join("..", "tests", "syntax", "syntax_03.py"): 9,
    os.path.join("..", "tests", "syntax", "syntax_04.py"): 2,
    os.path.join("..", "tests", "syntax", "syntax_05.py"): 14,
    os.path.join("..", "tests", "syntax", "syntax_06.py"): 5,
    os.path.join("..", "tests", "syntax", "syntax_07.py"): 50,
    os.path.join("..", "tests", "syntax", "syntax_08.py"): 5,
    os.path.join("..", "tests", "syntax", "syntax_09.py"): 14,
    os.path.join("..", "tests", "syntax", "syntax_10.py"): 8,
    # Ошибки отступа
    os.path.join("..", "tests", "indent", "indent_01.py"): 4,
    os.path.join("..", "tests", "indent", "indent_02.py"): 4,
    os.path.join("..", "tests", "indent", "indent_03.py"): 6,
    os.path.join("..", "tests", "indent", "indent_04.py"): 11,
    os.path.join("..", "tests", "indent", "indent_05.py"): 6,
    os.path.join("..", "tests", "indent", "indent_06.py"): 31,
    os.path.join("..", "tests", "indent", "indent_07.py"): 15,
    os.path.join("..", "tests", "indent", "indent_08.py"): 3,
    os.path.join("..", "tests", "indent", "indent_09.py"): 20,
    os.path.join("..", "tests", "indent", "indent_10.py"): 13,
    # Логические ошибки
    os.path.join("..", "tests", "logic", "logic_01.py"): 6,
    os.path.join("..", "tests", "logic", "logic_02.py"): 5,
    os.path.join("..", "tests", "logic", "logic_03.py"): 2,
    os.path.join("..", "tests", "logic", "logic_04.py"): 1,
    os.path.join("..", "tests", "logic", "logic_05.py"): 19,
    os.path.join("..", "tests", "logic", "logic_06.py"): 14,
    os.path.join("..", "tests", "logic", "logic_07.py"): 9,
    os.path.join("..", "tests", "logic", "logic_08.py"): 10,
    os.path.join("..", "tests", "logic", "logic_09.py"): 7,
    os.path.join("..", "tests", "logic", "logic_10.py"): 39,
}

ATTEMPTS = 3  # Каждый файл проверяется трижды, берётся наиболее частый результат


def read_and_number_lines(filepath: str) -> str:
    """Читает файл и нумерует строки."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    numbered = [f"{i}: {line.rstrip()}" for i, line in enumerate(lines)]
    return "\n".join(numbered)


def get_predicted_line(numbered_code: str) -> int | None:
    """Отправляет запрос и возвращает предсказанный номер строки."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": numbered_code}
            ],
            timeout=20
        )
        raw = response.choices[0].message.content or ""
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        if result.get("hasError"):
            return int(result.get("line", -1))
        return None
    except Exception as e:
        print(f"    Ошибка запроса: {e}")
        return None


def most_frequent(values: list) -> int | None:
    """Возвращает наиболее часто встречающееся значение."""
    if not values:
        return None
    return max(set(values), key=values.count)


def run_experiment():
    """Основная функция эксперимента."""
    print("=" * 60)
    print("Эксперимент 2: Точность локализации ошибок")
    print(f"Модель: {MODEL_NAME}")
    print(f"Попыток на файл: {ATTEMPTS}")
    print("=" * 60)

    categories = {
        "syntax": {"correct": 0, "total": 0},
        "indent": {"correct": 0, "total": 0},
        "logic":  {"correct": 0, "total": 0},
    }

    for filepath, expected_line in EXPECTED_LINES.items():
        if not os.path.exists(filepath):
            print(f"[!] Файл не найден: {filepath}")
            continue

        # Определяем категорию по пути файла
        category = None
        for cat in categories:
            if cat in filepath:
                category = cat
                break

        numbered_code = read_and_number_lines(filepath)
        filename = os.path.basename(filepath)
        print(f"\nФайл: {filename} | Ожидаемая строка: {expected_line}")

        predictions = []
        for attempt in range(1, ATTEMPTS + 1):
            predicted = get_predicted_line(numbered_code)
            predictions.append(predicted)
            print(f"  Попытка {attempt}: предсказано {predicted}")

        final_prediction = most_frequent([p for p in predictions if p is not None])
        is_correct = final_prediction == expected_line

        categories[category]["total"] += 1
        if is_correct:
            categories[category]["correct"] += 1

        status = "ВЕРНО" if is_correct else f"НЕВЕРНО (предсказано: {final_prediction})"
        print(f"  → Итог: {status}")

    print("\n" + "=" * 60)
    print("Итоговая таблица результатов:")
    print(f"{'Категория':<25} {'Верно':<10} {'Всего':<10} {'Точность, %':<15}")
    print("-" * 60)

    total_correct = 0
    total_files = 0

    for cat, data in categories.items():
        correct = data["correct"]
        total = data["total"]
        accuracy = round((correct / total * 100), 1) if total > 0 else 0
        total_correct += correct
        total_files += total
        print(f"{cat:<25} {correct:<10} {total:<10} {accuracy:<15}")

    overall = round((total_correct / total_files * 100), 1) if total_files > 0 else 0
    print("-" * 60)
    print(f"{'Итого':<25} {total_correct:<10} {total_files:<10} {overall:<15}")
    print("=" * 60)


if __name__ == "__main__":
    run_experiment()
