"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 4.

Условие:
Отсортируйте словарь по значению в порядке возрастания и убывания.
"""

from typing import Any, Dict


def sort_dict_by_value(
    d: Dict[Any, Any], reverse: bool = False
) -> Dict[Any, Any]:
    """
    Сортирует словарь по значениям.
    :param d: Исходный словарь.
    :param reverse: False - возрастание, True - убывание.
    """
    return dict(
        sorted(d.items(), key=lambda item: item[1], reverse=reverse)
    )


def print_dict_table(title: str, d: Dict[Any, Any]) -> None:
    print(f"\n{title}:")
    print(f"{'Ключ':<22} | {'Значение':<12}")
    print("-" * 37)
    for k, v in d.items():
        print(f"{str(k):<22} | {str(v):<12}")


def main() -> None:
    print("=" * 60)
    print("Задание 1.4: Сортировка словаря по значению")
    print("=" * 60)

    sample_dict = {
        "Машинное обучение": 95,
        "Математика": 88,
        "Базы данных": 74,
        "Операционные системы": 81,
        "Алгоритмы и структуры": 92,
        "Компьютерные сети": 67,
    }

    print_dict_table("Исходный словарь", sample_dict)

    asc_dict = sort_dict_by_value(sample_dict, reverse=False)
    print_dict_table("По возрастанию значений", asc_dict)

    desc_dict = sort_dict_by_value(sample_dict, reverse=True)
    print_dict_table("По убыванию значений", desc_dict)


if __name__ == "__main__":
    main()
