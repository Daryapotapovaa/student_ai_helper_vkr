# Задание: поиск минимального и максимального элемента без встроенных функций

def find_min_max(numbers):
    min_val = 0
    max_val = 0

    for num in numbers:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num

    return min_val, max_val

print(find_min_max([3, 1, 4, 1, 5, 9, 2, 6]))
print(find_min_max([10, 20, 30, 40, 50]))
