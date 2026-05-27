# Задание: поиск максимального элемента в списке

def find_max(lst):
    max_val = lst[0]
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val

print(find_max([3, 1, 4, 1, 5, 9, 2, 6]
