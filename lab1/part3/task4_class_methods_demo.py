"""
Лабораторная работа №1. Часть 3.
Вариант 7. Задание 4.

Условие:
Придумать класс самостоятельно, реализовать в нем:
- методы экземпляра класса,
- статические методы (@staticmethod),
- методы класса (@classmethod).
"""

from typing import ClassVar, Dict, List


class StudentAccount:
    """Класс для учета успеваемости студента университета."""

    university_name: ClassVar[str] = "БГУИР"
    _registry: ClassVar[List["StudentAccount"]] = []

    def __init__(
        self, full_name: str, group: str, student_id: str
    ) -> None:
        if not self.validate_student_id(student_id):
            raise ValueError(f"Неверный номер билета: '{student_id}'")
        self.full_name = full_name
        self.group = group
        self.student_id = student_id
        self.grades: Dict[str, int] = {}
        StudentAccount._registry.append(self)

    # 1. Методы экземпляра (Instance methods)
    def add_grade(self, subject: str, grade: int) -> None:
        if not (1 <= grade <= 10):
            raise ValueError(f"Оценка {grade} вне диапазона 1..10.")
        self.grades[subject] = grade

    def get_average_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def is_honor_student(self) -> bool:
        return self.get_average_grade() >= 8.5 and bool(self.grades)

    def get_profile(self) -> str:
        avg = self.get_average_grade()
        ects = self.convert_grade_to_ects(avg)
        return (
            f"Студент: {self.full_name} | Группа: {self.group}\n"
            f"  Билет: {self.student_id} | Вуз: {self.university_name}\n"
            f"  Средний балл: {avg:.2f} ({ects}) | "
            f"Статус: {'Отличник' if self.is_honor_student() else 'Успевает'}"
        )

    # 2. Методы класса (@classmethod)
    @classmethod
    def from_string(cls, raw: str) -> "StudentAccount":
        parts = [p.strip() for p in raw.split(";")]
        if len(parts) != 3:
            raise ValueError("Формат: 'ФИО;Группа;НомерБилета'")
        return cls(parts[0], parts[1], parts[2])

    @classmethod
    def get_total_count(cls) -> int:
        return len(cls._registry)

    @classmethod
    def get_honor_students(cls) -> List["StudentAccount"]:
        return [st for st in cls._registry if st.is_honor_student()]

    # 3. Статические методы (@staticmethod)
    @staticmethod
    def validate_student_id(sid: str) -> bool:
        return isinstance(sid, str) and sid.isdigit() and len(sid) == 8

    @staticmethod
    def convert_grade_to_ects(g: float) -> str:
        if g >= 9.0:
            return "A"
        elif g >= 8.0:
            return "B"
        elif g >= 7.0:
            return "C"
        elif g >= 6.0:
            return "D"
        elif g >= 4.0:
            return "E"
        return "F"


def main() -> None:
    print("=" * 60)
    print("Задание 3.4: Методы экземпляра, класса и статические")
    print("=" * 60)

    # Статические методы
    print("\n--- 1. @staticmethod validate_student_id ---")
    val = StudentAccount.validate_student_id('35100207')
    print(f"ID '35100207': {val}")
    print(f"ID '1234':     {StudentAccount.validate_student_id('1234')}")

    # Методы класса
    print("\n--- 2. @classmethod from_string ---")
    st1 = StudentAccount("Власовец Александр", "351002", "35100207")
    st2 = StudentAccount.from_string("Иванов Иван;351001;35100115")
    print(f"Всего студентов: {StudentAccount.get_total_count()}")

    # Методы экземпляра
    print("\n--- 3. Методы экземпляра ---")
    st1.add_grade("Машинное обучение", 10)
    st1.add_grade("Базы данных", 9)
    st2.add_grade("Машинное обучение", 7)
    st2.add_grade("Базы данных", 6)

    print(st1.get_profile())
    print()
    print(st2.get_profile())

    print("\n--- 4. @classmethod get_honor_students ---")
    for h in StudentAccount.get_honor_students():
        print(f"  • {h.full_name} (ср. балл: {h.get_average_grade():.2f})")


if __name__ == "__main__":
    main()
