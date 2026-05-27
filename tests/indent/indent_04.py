# Задание: класс стек с базовыми операциями

class Stack:
    def __init__(self):
        self.items = []
        self.max_size = None

    def push(self, item):
        if self.max_size and len(self.items) >= self.max_size:
            print("Стек переполнен")
            return False
    self.items.append(item)
        return True

    def pop(self):
        if self.is_empty():
            print("Стек пуст")
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())
print(s.peek())
