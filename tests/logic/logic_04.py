# Задание: система накопления истории вычислений

def calculate(a, b, operation, history=[]):
    if operation == "add":
        result = a + b
    elif operation == "sub":
        result = a - b
    elif operation == "mul":
        result = a * b
    elif operation == "div":
        if b == 0:
            print("Ошибка: деление на ноль")
            return None
        result = a / b
    else:
        print(f"Неизвестная операция: {operation}")
        return None

    entry = f"{a} {operation} {b} = {result}"
    history.append(entry)
    return result


def get_history(history=[]):
    return history


print(calculate(10, 5, "add"))
print(calculate(20, 3, "mul"))
print(calculate(15, 4, "sub"))

print("\nИстория вычислений:")
for entry in get_history():
    print(f"  {entry}")
