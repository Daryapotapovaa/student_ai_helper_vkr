# Задание: создание набора функций-обработчиков через замыкание

def create_handlers(operations):
    handlers = []

    for op in operations:
        def handler(x):
            return op["func"](x)
        handlers.append(handler)

    return handlers


def create_pipeline(handlers):
    def pipeline(value):
        result = value
        for handler in handlers:
            result = handler(result)
        return result
    return pipeline


operations = [
    {"name": "double", "func": lambda x: x * 2},
    {"name": "add_ten", "func": lambda x: x + 10},
    {"name": "square", "func": lambda x: x ** 2},
    {"name": "negate", "func": lambda x: -x},
]

handlers = create_handlers(operations)

print("Проверка отдельных обработчиков:")
test_value = 5
for i, (handler, op) in enumerate(zip(handlers, operations)):
    result = handler(test_value)
    print(f"  {op['name']}({test_value}) = {result}")

pipeline = create_pipeline(handlers)
print(f"\nКонвейер для значения {test_value}:")
print(f"  Результат: {pipeline(test_value)}")

print("\nКонвейер для диапазона [1, 5]:")
for val in range(1, 6):
    print(f"  pipeline({val}) = {pipeline(val)}")
