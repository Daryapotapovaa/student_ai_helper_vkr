"""
Эксперимент 3: Замер потребления вычислительных ресурсов
=========================================================
Измеряет потребление RAM и нагрузку на CPU процессом
LSP-сервера в трёх состояниях: ожидание, запрос, обработка.

Соответствует разделу 4.5 дипломной работы.

Важно: перед запуском скрипта необходимо запустить LSP-сервер
вручную командой из папки server/:
    node out/server.js --stdio

Использование:
    pip install psutil python-dotenv openai
    python measure_resources.py

Примечание: PID процесса сервера можно найти в диспетчере задач
или передать как аргумент командной строки:
    python measure_resources.py --pid 12345
"""

import time
import os
import argparse
import statistics
import threading
import json
from openai import OpenAI
from dotenv import load_dotenv

try:
    import psutil
except ImportError:
    print("Установите psutil: pip install psutil")
    exit(1)

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

SYSTEM_PROMPT = """
    Ты — опытный, терпеливый преподаватель Python и наставник для новичков.
    Твоя задача — найти главную ошибку или логическую недоработку в коде студента.
    Все объяснения пиши только на русском языке.
    Ты ДОЛЖЕН ответить СТРОГО в формате JSON без markdown разметки и лишнего текста:
    {
    "hasError": true или false,
    "line": <номер строки с ошибкой (число)>,
    "message": "<объяснение>",
    "suggestedCode": "<код или null>"
    }
"""

TEST_FILE = os.path.join("..", "tests", "syntax", "syntax_04.py")
IDLE_DURATION = 5    # секунд наблюдения в режиме ожидания
MEASUREMENTS = 10    # количество замеров для каждого состояния


def find_server_process() -> psutil.Process | None:
    """Ищет процесс Node.js с сервером среди запущенных процессов."""
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = " ".join(proc.info["cmdline"] or [])
            if "node" in proc.info["name"].lower() and "server.js" in cmdline:
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def measure_process(proc: psutil.Process, duration: float = 1.0) -> dict:
    """
    Измеряет потребление ресурсов процесса за указанный период.
    Возвращает среднее значение RAM (МБ) и CPU (%).
    """
    ram_samples = []
    cpu_samples = []

    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            mem = proc.memory_info().rss / (1024 * 1024)  # в МБ
            cpu = proc.cpu_percent(interval=0.1)
            ram_samples.append(mem)
            cpu_samples.append(cpu)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            break
        time.sleep(0.1)

    return {
        "ram_mb": round(statistics.mean(ram_samples), 1) if ram_samples else 0,
        "cpu_pct": round(statistics.mean(cpu_samples), 2) if cpu_samples else 0,
    }


def read_and_number_lines(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return "\n".join(f"{i}: {line.rstrip()}" for i, line in enumerate(lines))


def send_request(numbered_code: str):
    """Отправляет запрос к модели — используется в отдельном потоке."""
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": numbered_code}
            ],
            timeout=15
        )
    except Exception as e:
        print(f"  Ошибка запроса: {e}")


def run_experiment(pid: int | None = None):
    """Основная функция эксперимента."""
    print("=" * 60)
    print("Эксперимент 3: Потребление вычислительных ресурсов")
    print(f"Модель: {MODEL_NAME}")
    print("=" * 60)

    # Находим процесс сервера
    if pid:
        try:
            proc = psutil.Process(pid)
            print(f"Используем процесс с PID {pid}: {proc.name()}")
        except psutil.NoSuchProcess:
            print(f"[!] Процесс с PID {pid} не найден")
            return
    else:
        proc = find_server_process()
        if proc is None:
            print("[!] LSP-сервер не найден среди запущенных процессов.")
            print("    Запустите сервер командой: node server/out/server.js --stdio")
            print("    Или укажите PID вручную: python measure_resources.py --pid <PID>")
            return
        print(f"Найден LSP-сервер: PID {proc.pid}")

    results = {}

    # --- Состояние 1: Режим ожидания ---
    print(f"\n[1/3] Замер в режиме ожидания ({IDLE_DURATION} сек.)...")
    idle_measurements = []
    for i in range(MEASUREMENTS):
        m = measure_process(proc, duration=0.5)
        idle_measurements.append(m)
        time.sleep(IDLE_DURATION / MEASUREMENTS)

    results["idle"] = {
        "ram_mb": round(statistics.mean([m["ram_mb"] for m in idle_measurements]), 1),
        "cpu_pct": round(statistics.mean([m["cpu_pct"] for m in idle_measurements]), 2),
    }
    print(f"  RAM: {results['idle']['ram_mb']} МБ | CPU: {results['idle']['cpu_pct']}%")

    # --- Состояние 2: Режим запроса (ожидание ответа от модели) ---
    print("\n[2/3] Замер в режиме запроса (ожидание ответа от модели)...")
    numbered_code = read_and_number_lines(TEST_FILE)

    request_measurements = []
    request_thread = threading.Thread(target=send_request, args=(numbered_code,))
    request_thread.start()

    # Измеряем пока идёт запрос
    while request_thread.is_alive():
        m = measure_process(proc, duration=0.5)
        request_measurements.append(m)

    request_thread.join()

    if request_measurements:
        results["request"] = {
            "ram_mb": round(statistics.mean([m["ram_mb"] for m in request_measurements]), 1),
            "cpu_pct": round(statistics.mean([m["cpu_pct"] for m in request_measurements]), 2),
        }
        print(f"  RAM: {results['request']['ram_mb']} МБ | CPU: {results['request']['cpu_pct']}%")

    # --- Состояние 3: Режим обработки ответа ---
    print("\n[3/3] Замер в режиме обработки ответа...")
    processing_measurements = []

    # Имитируем обработку JSON — максимальная нагрузка при парсинге
    for _ in range(MEASUREMENTS):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": numbered_code}
                ],
                timeout=15
            )
            raw = response.choices[0].message.content or ""
            # Момент парсинга JSON — пик нагрузки
            start_proc = time.perf_counter()
            m = measure_process(proc, duration=0.3)
            clean = raw.replace("```json", "").replace("```", "").strip()
            json.loads(clean)
            processing_measurements.append(m)
        except Exception:
            pass

    if processing_measurements:
        results["processing"] = {
            "ram_mb": round(statistics.mean([m["ram_mb"] for m in processing_measurements]), 1),
            "cpu_pct": round(statistics.mean([m["cpu_pct"] for m in processing_measurements]), 2),
        }
        print(f"  RAM: {results['processing']['ram_mb']} МБ | CPU: {results['processing']['cpu_pct']}%")

    # --- Итоговая таблица ---
    print("\n" + "=" * 60)
    print("Итоговая таблица результатов:")
    print(f"{'Состояние':<30} {'RAM, МБ':<15} {'CPU, %':<10}")
    print("-" * 55)

    state_labels = {
        "idle": "Режим ожидания",
        "request": "Режим запроса",
        "processing": "Режим обработки ответа",
    }

    for state, label in state_labels.items():
        if state in results:
            r = results[state]
            print(f"{label:<30} {r['ram_mb']:<15} {r['cpu_pct']:<10}")

    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Замер ресурсов LSP-сервера")
    parser.add_argument("--pid", type=int, help="PID процесса Node.js сервера")
    args = parser.parse_args()
    run_experiment(pid=args.pid)
