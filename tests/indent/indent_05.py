# Задание: безопасное чтение и обработка числовых данных

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
    print("Ошибка: деление на ноль")
        return None
    except TypeError:
        print("Ошибка: некорректный тип данных")
        return None
    else:
        return result
    finally:
        print(f"Операция деления {a} / {b} завершена")


def process_data(data):
    results = []
    for pair in data:
        a, b = pair
        result = safe_divide(a, b)
        if result is not None:
            results.append(result)
    return results


pairs = [(10, 2), (15, 3), (8, 0), (20, 4), (9, "три")]
output = process_data(pairs)
print(f"Результаты: {output}")
print(f"Успешных операций: {len(output)}")
