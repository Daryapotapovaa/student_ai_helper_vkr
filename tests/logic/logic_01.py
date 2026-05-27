# Задание: подсчёт количества элементов больше среднего

def count_above_average(numbers):
    average = sum(numbers) / len(numbers)
    count = 0

    for i in range(len(numbers) - 1):
        if numbers[i] > average:
            count += 1

    return count

print(count_above_average([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
