# Задание: вычисление чисел Фибоначчи с мемоизацией

def fibonacci(n, memo={}):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n in memo:
        return memo[n]

    result = fibonacci(n - 1, memo) + fibonacci(n - 3, memo)
    memo[n] = result
    return result


def fibonacci_sequence(length):
    return [fibonacci(i) for i in range(length)]


def golden_ratio_approximations(n):
    sequence = fibonacci_sequence(n + 1)
    ratios = []
    for i in range(2, len(sequence)):
        if sequence[i - 1] != 0:
            ratio = sequence[i] / sequence[i - 1]
            ratios.append(round(ratio, 6))
    return ratios


seq = fibonacci_sequence(15)
print(f"Последовательность Фибоначчи: {seq}")

ratios = golden_ratio_approximations(15)
print(f"\nПриближения золотого сечения:")
for i, ratio in enumerate(ratios[-5:], 1):
    print(f"  {i}: {ratio}")
