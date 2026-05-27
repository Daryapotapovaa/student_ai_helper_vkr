# Задание: система управления библиотекой

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True

    def __str__(self):
        status = "доступна" if self.is_available else "выдана"
        return f'"{self.title}" — {self.author} ({self.year}) [{status}]'


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.borrowed = {}

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title, reader):
        book = self.find_book(title)
        if book is None:
            print(f'Книга "{title}" не найдена')
            return False
        if not book.is_available:
        print(f'Книга "{title}" уже выдана')
            return False
        book.is_available = False
        self.borrowed[title] = reader
        print(f'Книга "{title}" выдана читателю {reader}')
        return True

    def return_book(self, title):
        book = self.find_book(title)
        if book and not book.is_available:
            book.is_available = True
            reader = self.borrowed.pop(title, None)
            print(f'Книга "{title}" возвращена от {reader}')
            return True
        print(f'Книга "{title}" не была выдана')
        return False

    def available_books(self):
        return [b for b in self.books if b.is_available]


lib = Library("Городская библиотека")
lib.add_book(Book("Мастер и Маргарита", "Булгаков", 1967))
lib.add_book(Book("Преступление и наказание", "Достоевский", 1866))
lib.add_book(Book("Война и мир", "Толстой", 1869))

lib.borrow_book("Мастер и Маргарита", "Анна")
lib.borrow_book("Мастер и Маргарита", "Борис")
lib.return_book("Мастер и Маргарита")
print(f"\nДоступно книг: {len(lib.available_books())}")
