# Задание: реализация LRU-кэша без использования встроенных средств

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

    def current_state(self):
        state = []
        current = self.head.next
        while current != self.tail:
            state.append((current.key, current.value))
            current = current.prev
        return state

    def size(self):
        return len(self.cache)


cache = LRUCache(3)

print("=== Тест LRU-кэша (ёмкость: 3) ===")

cache.put(1, "один")
cache.put(2, "два")
cache.put(3, "три")
print(f"После добавления 1,2,3: {cache.current_state()}")

print(f"get(1) = {cache.get(1)}")
print(f"После get(1): {cache.current_state()}")

cache.put(4, "четыре")
print(f"После добавления 4 (должен вытеснить 2): {cache.current_state()}")
print(f"get(2) = {cache.get(2)}")

cache.put(5, "пять")
print(f"После добавления 5: {cache.current_state()}")

test_keys = [1, 2, 3, 4, 5]
print("\nПроверка всех ключей:")
for key in test_keys:
    result = cache.get(key)
    print(f"  get({key}) = {result}")
