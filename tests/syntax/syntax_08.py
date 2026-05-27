# Задание: декоратор для измерения времени выполнения функции

import time
import functools

def timer(func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} выполнилась за {end - start:.4f} сек.")
        return result
    return wrapper


@timer
def bubble_sort(lst):
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = bubble_sort(data)
print(f"Отсортированный список: {sorted_data}")
