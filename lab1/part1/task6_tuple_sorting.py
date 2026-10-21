"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 6.

Условие:
Дан кортеж целых чисел. Отсортировать его в порядке убывания.
Вывести первый и последний элемент кортежа.
"""

from typing import Tuple


def sort_tuple_descending(
    tup: Tuple[int, ...]
) -> Tuple[Tuple[int, ...], int, int]:
    """
    Сортирует кортеж по убыванию и возвращает первый и последний элементы.
    """
    if not tup:
        raise ValueError("Кортеж не должен быть пустым.")

    sorted_tup = tuple(sorted(tup, reverse=True))
    return sorted_tup, sorted_tup[0], sorted_tup[-1]


def main() -> None:
    print("=" * 60)
    print("Задание 1.6: Сортировка кортежа целых чисел по убыванию")
    print("=" * 60)

    test_tuples = [
        (42, 17, 89, 5, 63, 104, -12, 0, 77),
        (-5, -20, -1, -100),
        (10, 10, 5, 20, 20),
        (999,),
    ]

    print("\n--- Демонстрация на контрольных кортежах ---")
    for tup in test_tuples:
        sorted_res, first, last = sort_tuple_descending(tup)
        print(f"Исходный кортеж:       {tup}")
        print(f"Отсортированный (desc): {sorted_res}")
        print(f"  Первый элемент (max): {first}")
        print(f"  Последний элемент (min): {last}\n")

    print("--- Пользовательский ввод ---")
    user_input = input(
        "Введите числа через пробел (Enter для пропуска): "
    ).strip()
    if user_input:
        try:
            u_tup = tuple(int(x) for x in user_input.split())
            sorted_res, first, last = sort_tuple_descending(u_tup)
            print(f"Исходный кортеж:       {u_tup}")
            print(f"Отсортированный (desc): {sorted_res}")
            print(f"  Первый элемент: {first}, Последний: {last}")
        except ValueError as err:
            print(f"Ошибка ввода: {err}")


if __name__ == "__main__":
    main()
