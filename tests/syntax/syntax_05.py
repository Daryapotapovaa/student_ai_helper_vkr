# Задание: анализ частоты слов в тексте

def word_frequency(text):
    words = text.lower().split()
    frequency = {}

    for word in words:
        word = word.strip(".,!?;:")
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency

def top_words(frequency, n=5):
    sorted_words = sorted(frequency.items(), key=lambda x x[1], reverse=True)
    return sorted_words[:n]


text = """Python является одним из самых популярных языков программирования.
Python используется в веб разработке анализе данных и машинном обучении.
Многие разработчики выбирают Python за его простоту и читаемость."""

freq = word_frequency(text)
top = top_words(freq)

print("Топ слов:")
for word, count in top:
    print(f"  {word}: {count}")
