"""
Лабораторная работа №1. Часть 2.
Вариант 7. Задание 1.

Требование:
Все задания выполнить с использованием функций и обработкой
исключительных ситуаций при помощи блока try\\except\\finally.

Условие:
Напишите функцию is_password_good(password), которая принимает строковое
значение пароля и возвращает True если пароль надежный (длина >= 10,
минимум 1 заглавная и 1 строчная буква), иначе False.
"""

from typing import Dict


def is_password_good(password: str) -> bool:
    """
    Проверяет надежность пароля с использованием try-except-finally.
    """
    is_valid = False
    try:
        if not isinstance(password, str):
            msg = f"Пароль: str, передан {type(password).__name__}"
            raise TypeError(msg)

        has_len = len(password) >= 10
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        is_valid = has_len and has_upper and has_lower
        return is_valid

    except TypeError as exc:
        print(f"  [Ошибка типа]: {exc}")
        return False
    finally:
        status = "НАДЁЖЕН" if is_valid else "НЕ НАДЁЖЕН"
        display = repr(password) if isinstance(password, str) \
            else str(password)
        print(f"  [finally]: Проверка {display} завершена -> {status}")


def main() -> None:
    print("=" * 60)
    print("Задание 2.1: Проверка надежности пароля (try/except/finally)")
    print("=" * 60)

    test_passwords = [
        "StrongPass2026",
        "SecurePassword",
        "Short1Aa",
        "alllowercasepassword",
        "ALLUPPERCASEPASSWORD",
        "1234567890",
        "",
        1234567890,
    ]

    print("\n--- Запуск контрольных тестов ---")
    for pwd in test_passwords:
        print(f"\nПроверка: {repr(pwd)}")
        res = is_password_good(pwd)
        print(f"  Результат: {res}")


if __name__ == "__main__":
    main()
