# Задание: конвейер обработки данных с использованием генераторов

from typing import Generator, Callable, Any
import math


def read_data(data: list) -> Generator:
    for item in data:
        yield item


def filter_pipeline(source: Generator, predicate: Callable) -> Generator:
    for item in source:
        if predicate(item):
        yield item


def transform_pipeline(source: Generator, transform: Callable) -> Generator:
    for item in source:
        yield transform(item)


def batch_pipeline(source: Generator, batch_size: int) -> Generator:
    batch = []
    for item in source:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def aggregate(source: Generator, func: Callable) -> Any:
    return func(list(source))


def stats_pipeline(source: Generator) -> dict:
    data = list(source)
    if not data:
        return {}

    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    sorted_data = sorted(data)
    median = sorted_data[n // 2] if n % 2 != 0 else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    return {
        "count": n,
        "min": min(data),
        "max": max(data),
        "mean": round(mean, 2),
        "median": median,
        "std_dev": round(std_dev, 2)
    }


raw_data = [15, -3, 42, 7, -18, 33, 0, 91, 12, -5,
            28, 64, -11, 37, 5, 19, -7, 83, 44, 2,
            -22, 56, 13, 71, -9, 38, 25, -1, 67, 49]

print("=== Конвейер обработки данных ===")
print(f"Исходный набор: {len(raw_data)} элементов")

source1 = read_data(raw_data)
positive_only = filter_pipeline(source1, lambda x: x > 0)
doubled = transform_pipeline(positive_only, lambda x: x * 2)
batched = batch_pipeline(doubled, batch_size=5)

print("\nПакеты удвоенных положительных чисел:")
for i, batch in enumerate(batched):
    print(f"  Пакет {i + 1}: {batch}")

source2 = read_data(raw_data)
positive_source = filter_pipeline(source2, lambda x: x > 0)
stats = stats_pipeline(positive_source)

print("\nСтатистика по положительным числам:")
for key, value in stats.items():
    print(f"  {key}: {value}")
