"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 1.

Условие:
Найти сумму нечетных цифр введенного натурального числа.
"""

from typing import List, Tuple


def get_sum_of_odd_digits(number: int) -> Tuple[int, List[int]]:
    """
    Вычисляет сумму нечётных цифр натурального числа.
    :param number: Натуральное число (> 0).
    :return: Кортеж (сумма_нечётных_цифр, список_нечётных_цифр).
    """
    if number <= 0:
        raise ValueError(
            "Число должно быть натуральным (> 0)."
        )

    digits = [int(ch) for ch in str(number)]
    odd_digits = [d for d in digits if d % 2 != 0]
    total_sum = sum(odd_digits)
    return total_sum, odd_digits


def main() -> None:
    print("=" * 60)
    print("Задание 1.1: Сумма нечётных цифр натурального числа")
    print("=" * 60)

    # Демонстрация на контрольных примерах
    test_numbers = [371524, 2468, 13579, 987654321, 5]
    print("\n--- Демонстрация на тестовых данных ---")
    for num in test_numbers:
        s, odds = get_sum_of_odd_digits(num)
        print(f"Число: {num}")
        print(f"  Нечётные цифры: {odds}")
        print(f"  Сумма нечётных цифр: {s}\n")

    # Пользовательский ввод
    print("--- Пользовательский ввод ---")
    prompt = "Введите натуральное число (Enter для пропуска): "
    user_input = input(prompt).strip()
    if user_input:
        try:
            val = int(user_input)
            s, odds = get_sum_of_odd_digits(val)
            print(f"Результат для числа {val}:")
            print(f"  Нечётные цифры: {odds}")
            print(f"  Сумма нечётных цифр: {s}")
        except ValueError as err:
            print(f"Ошибка ввода: {err}")


if __name__ == "__main__":
    main()
