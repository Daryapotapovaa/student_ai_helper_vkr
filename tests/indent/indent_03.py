# Задание: поиск пар чисел с заданной суммой

def find_pairs(numbers, target):
    pairs = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
        if numbers[i] + numbers[j] == target:
                pairs.append((numbers[i], numbers[j]))
    return pairs

print(find_pairs([1, 2, 3, 4, 5, 6], 7))
