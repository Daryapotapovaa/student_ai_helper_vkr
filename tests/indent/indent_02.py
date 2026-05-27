# Задание: таблица умножения для числа

def multiplication_table(n):
    for i in range(1, 11):
    result = n * i
    print(f"{n} x {i} = {result}")

multiplication_table(7)
