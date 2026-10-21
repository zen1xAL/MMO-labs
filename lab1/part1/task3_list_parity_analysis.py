"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 3.

Условие:
Дан список list=[1612,49,'hello',6,19,'world’].
Все числа этого списка проверить на чётность. Если число чётное, то
посчитать сумму его цифр. Если нечётное, то заменить его на 1 в списке.
Все слова: посчитать количество гласных и согласных. Вывести всё на экран.
"""

from typing import Any, List, Tuple

VOWELS = set("aeiou" "аеёиоуыэюя")
CONSONANTS = set("bcdfghjklmnpqrstvwxyz" "бвгджзйклмнпрстфхцчшщ")


def count_letters(word: str) -> Tuple[int, List[str], int, List[str]]:
    v_found = [c for c in word if c.lower() in VOWELS]
    c_found = [c for c in word if c.lower() in CONSONANTS]
    return len(v_found), v_found, len(c_found), c_found


def process_list(data: List[Any]) -> Tuple[List[Any], List[str]]:
    modified = list(data)
    reports: List[str] = []

    for idx, item in enumerate(modified):
        if isinstance(item, int):
            if item % 2 == 0:
                d_sum = sum(int(d) for d in str(abs(item)))
                reports.append(
                    f"[{idx}] {item} (чётное): сумма цифр = {d_sum}"
                )
            else:
                reports.append(
                    f"[{idx}] {item} (нечётное): заменено на 1"
                )
                modified[idx] = 1
        elif isinstance(item, str):
            v_cnt, v_ch, c_cnt, c_ch = count_letters(item)
            reports.append(
                f"[{idx}] '{item}' (слово): "
                f"гласных {v_cnt} {v_ch}, согласных {c_cnt} {c_ch}"
            )
        else:
            reports.append(f"[{idx}] {item}: пропущен")

    return modified, reports


def main() -> None:
    print("=" * 60)
    print("Задание 1.3: Обработка списка чисел и строк")
    print("=" * 60)

    initial_list = [1612, 49, 'hello', 6, 19, 'world']
    print(f"\nИсходный список: {initial_list}\n")

    res_list, logs = process_list(initial_list)

    print("--- Результаты анализа элементов списка ---")
    for log in logs:
        print(f"  • {log}")

    print("\n--- Итоговый список после преобразования ---")
    print(f"Результат: {res_list}\n")


if __name__ == "__main__":
    main()
