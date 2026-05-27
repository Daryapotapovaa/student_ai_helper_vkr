# Задание: реализация сортировки слиянием

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def verify_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


test_cases = [
    [64, 34, 25, 12, 22, 11, 90],
    [5, 4, 3, 2, 1],
    [1],
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
    [1, 2, 3, 4, 5],
]

for test in test_cases:
    result = merge_sort(test.copy())
    is_correct = verify_sorted(result)
    print(f"Вход: {test}")
    print(f"Выход: {result}")
    print(f"Корректно: {is_correct}\n")
