"""
Лабораторная работа №1. Часть 3.
Вариант 7. Задание 3.

Условие:
Создать классы: «Книга», «Отдел», «Библиотека». В классах реализовать
методы: добавление, удаление, изменение названия книг из отделов.
Классы должны содержать методы доступа и изменения всех полей.
Предусмотреть метод записи информации в файл.
"""

from typing import Dict, List, Optional


class Book:
    """Класс 'Книга' с инкапсуляцией всех полей через @property."""

    def __init__(
        self, title: str, author: str, year: int, isbn: str
    ) -> None:
        self._title = ""
        self._author = ""
        self._year = 0
        self._isbn = ""
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Название не может быть пустым.")
        self._title = val.strip()

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Автор не может быть пустым.")
        self._author = val.strip()

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, val: int) -> None:
        if not isinstance(val, int) or val <= 0:
            raise ValueError("Некорректный год.")
        self._year = val

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValueError("ISBN не может быть пустым.")
        self._isbn = val.strip()

    def __str__(self) -> str:
        return f"«{self._title}» ({self._author}, {self._year})"


class Department:
    """Класс 'Отдел' библиотеки."""

    def __init__(self, name: str) -> None:
        self._name = ""
        self.name = name
        self._books: Dict[str, Book] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Название отдела не должно быть пустым.")
        self._name = val.strip()

    def add_book(self, book: Book) -> bool:
        if book.isbn in self._books:
            return False
        self._books[book.isbn] = book
        return True

    def remove_book(self, identifier: str) -> Optional[Book]:
        if identifier in self._books:
            return self._books.pop(identifier)
        for isbn, b in list(self._books.items()):
            if b.title.lower() == identifier.lower():
                return self._books.pop(isbn)
        return None

    def update_book_title(self, identifier: str, new_title: str) -> bool:
        book = self.find_book(identifier)
        if book:
            book.title = new_title
            return True
        return False

    def find_book(self, identifier: str) -> Optional[Book]:
        if identifier in self._books:
            return self._books[identifier]
        for b in self._books.values():
            if b.title.lower() == identifier.lower():
                return b
        return None

    def get_books(self) -> List[Book]:
        return list(self._books.values())

    def __len__(self) -> int:
        return len(self._books)


class Library:
    """Класс 'Библиотека' с управлением отделами и экспортом в файл."""

    def __init__(self, name: str) -> None:
        self._name = ""
        self.name = name
        self._departments: Dict[str, Department] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Название не должно быть пустым.")
        self._name = val.strip()

    def add_department(self, dept: Department) -> None:
        self._departments[dept.name] = dept

    def get_department(self, name: str) -> Optional[Department]:
        return self._departments.get(name)

    def save_to_file(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"КАТАЛОГ: {self.name}\n" + "=" * 50 + "\n")
            for d_name, dept in self._departments.items():
                f.write(f"\nОтдел: {d_name} ({len(dept)} книг)\n")
                for idx, b in enumerate(dept.get_books(), 1):
                    f.write(f"  {idx}. {b.title} ({b.year})\n")


def main() -> None:
    print("=" * 60)
    print("Задание 3.3: Система Книга - Отдел - Библиотека")
    print("=" * 60)

    lib = Library("Библиотека БГУИР")
    dep_it = Department("Отдел ИТ")
    dep_ai = Department("Отдел ИИ")
    lib.add_department(dep_it)
    lib.add_department(dep_ai)

    b1 = Book("Изучаем Python", "Марк Лутц", 2020, "978-5-907144-54-5")
    b2 = Book("Глубокое обучение", "Ян Гудфеллоу", 2018, "978-5-97060-463-2")
    b3 = Book("Паттерны", "Эрих Гамма", 2021, "978-5-4461-1520-4")

    dep_it.add_book(b1)
    dep_it.add_book(b3)
    dep_ai.add_book(b2)

    print("\n--- 1. Каталог до изменений ---")
    for d_name, d in [(dep_it.name, dep_it), (dep_ai.name, dep_ai)]:
        print(f"Отдел: {d_name}")
        for b in d.get_books():
            print(f"  • {b}")

    print("\n--- 2. Изменение названия книги ---")
    dep_it.update_book_title("978-5-907144-54-5", "Python (5-е изд.)")
    print(f"Обновленная книга: {dep_it.find_book('978-5-907144-54-5')}")

    print("\n--- 3. Проверка сеттера автора ---")
    print(f"Автор до:    {b2.author}")
    b2.author = "Ян Гудфеллоу, Иошуа Бенджио"
    print(f"Автор после: {b2.author}")

    print("\n--- 4. Удаление книги ---")
    rem = dep_it.remove_book("Паттерны проектирования")
    print(f"Удалено: {rem}")

    lib.save_to_file("d:/MMO/part3/library_catalog.txt")
    print("\nКаталог сохранен в: d:/MMO/part3/library_catalog.txt")


if __name__ == "__main__":
    main()
