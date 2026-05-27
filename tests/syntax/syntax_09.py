# Задание: генератор простых чисел с использованием решета Эратосфена

def sieve_generator(limit):
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, limit + 1, i):
                primes[j] = False

    for num in range(2, limit + 1)
        if primes[num]:
            yield num


def prime_stats(limit):
    gen = sieve_generator(limit)
    prime_list = list(gen)

    if not prime_list:
        return None

    return {
        "count": len(prime_list),
        "first": prime_list[0],
        "last": prime_list[-1],
        "sum": sum(prime_list),
        "average": sum(prime_list) / len(prime_list)
    }


def twin_primes(limit):
    gen = sieve_generator(limit)
    prime_list = list(gen)
    twins = []

    for i in range(len(prime_list) - 1):
        if prime_list[i + 1] - prime_list[i] == 2:
            twins.append((prime_list[i], prime_list[i + 1]))

    return twins


limit = 100
stats = prime_stats(limit)
print(f"Простые числа до {limit}:")
print(f"  Количество: {stats['count']}")
print(f"  Первое: {stats['first']}, последнее: {stats['last']}")
print(f"  Сумма: {stats['sum']}")
print(f"  Среднее: {stats['average']:.2f}")

twins = twin_primes(limit)
print(f"\nПары простых-близнецов: {len(twins)}")
for pair in twins[:5]:
    print(f"  {pair}")
