"""
Лабораторная работа №1. Часть 2.
Вариант 7. Задание 4.

Условие:
Напишите программу, демонстрирующую работу try\\except\\finally.
"""

import os
from typing import Optional


class CustomError(Exception):
    pass


def safe_divide(a: float, b: float) -> Optional[float]:
    print(f"\n[safe_divide({a}, {b})]")
    res: Optional[float] = None
    try:
        print("  1. Выполняется [try]...")
        if a < 0:
            raise CustomError("Числитель меньше нуля!")
        res = a / b
    except ZeroDivisionError as e:
        print(f"  2. Перехвачен ZeroDivisionError: {e}")
    except CustomError as e:
        print(f"  2. Перехвачен CustomError: {e}")
    except TypeError as e:
        print(f"  2. Перехвачен TypeError: {e}")
    else:
        print(f"  3. Блок [else]: Успешно, результат = {res:.4f}")
    finally:
        print("  4. Блок [finally]: Ресурсы освобождены.")
    return res


def safe_file_read(filename: str) -> None:
    print(f"\n[safe_file_read({repr(filename)})]")
    f = None
    try:
        print("  1. Открытие файла в [try]...")
        f = open(filename, "r", encoding="utf-8")
        content = f.read()
        print(f"  2. Прочитано символов: {len(content)}")
    except FileNotFoundError:
        print(f"  2. Ошибка: файл '{filename}' не найден!")
    finally:
        print("  3. Блок [finally]: закрытие файла...")
        if f is not None and not f.closed:
            f.close()
            print("     Дескриптор закрыт.")
        else:
            print("     Дескриптор не был открыт.")


def main() -> None:
    print("=" * 60)
    print("Задание 2.4: Демонстрация try / except / else / finally")
    print("=" * 60)

    # 1. Арифметические проверки
    safe_divide(100, 4)
    safe_divide(50, 0)
    safe_divide(-25, 5)
    safe_divide("100", 2)  # type: ignore

    # 2. Файловые операции
    safe_file_read("non_existent_file.txt")


if __name__ == "__main__":
    main()
