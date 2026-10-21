"""
Лабораторная работа №1. Часть 2.
Вариант 7. Задание 2.

Требование:
Все задания выполнить с использованием функций и обработкой
исключительных ситуаций при помощи блока try\\except\\finally.

Условие:
Напишите функцию, которая принимает один аргумент:
- Кортеж: посчитать длину всех его слов.
- Список: сумму после первого отрицательного элемента, удалить дубликаты.
- Число: кол-во четных цифр.
- Строка: найти сумму всех чисел.
Сделать проверку со всеми этими случаями.
"""

import re
from typing import Any, Dict, List, Tuple


def process_data(data: Any) -> Dict[str, Any]:
    """
    Универсальная функция обработки данных с try-except-finally.
    """
    result: Dict[str, Any] = {
        "type": type(data).__name__, "status": "pending"
    }

    try:
        if isinstance(data, tuple):
            result["action"] = "Кортеж: длина слов"
            word_lengths = [(str(w), len(str(w))) for w in data]
            result["lengths"] = word_lengths
            result["total_length"] = sum(l for _, l in word_lengths)
            result["status"] = "success"

        elif isinstance(data, list):
            result["action"] = "Список: сумма после < 0, без дубликатов"
            neg_idx = -1
            for idx, val in enumerate(data):
                if isinstance(val, (int, float)) and val < 0:
                    neg_idx = idx
                    break

            if neg_idx != -1:
                tail = data[neg_idx + 1:]
                result["neg_val"] = data[neg_idx]
                result["tail"] = tail
                result["sum_after"] = sum(
                    x for x in tail if isinstance(x, (int, float))
                )
            else:
                result["sum_after"] = None

            result["unique"] = list(dict.fromkeys(data))
            result["status"] = "success"

        elif isinstance(data, (int, float)) and not isinstance(data, bool):
            result["action"] = "Число: количество чётных цифр"
            digits = [int(d) for d in re.sub(r"[^0-9]", "", str(data))]
            evens = [d for d in digits if d % 2 == 0]
            result["digits"] = digits
            result["evens"] = evens
            result["even_count"] = len(evens)
            result["status"] = "success"

        elif isinstance(data, str):
            result["action"] = "Строка: сумма чисел"
            nums = [int(n) for n in re.findall(r"-?\d+", data)]
            result["nums"] = nums
            result["sum"] = sum(nums)
            result["status"] = "success"

        else:
            raise TypeError(f"Неподдерживаемый тип: {type(data).__name__}")

    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        print(f"  [Ошибка]: {exc}")
    finally:
        print(f"  [finally]: Тип '{result['type']}' -> {result['status']}")

    return result


def display_result(r: Dict[str, Any]) -> None:
    print(f"Действие: {r.get('action', 'Ошибка')}")
    t = r["type"]
    if t == "tuple":
        print(f"  Слова и длины: {r['lengths']}")
        print(f"  Общая длина:   {r['total_length']}")
    elif t == "list":
        if r.get("sum_after") is not None:
            print(f"  Первый < 0: {r['neg_val']}")
            print(f"  Хвост:      {r['tail']}")
            print(f"  Сумма после первого < 0: {r['sum_after']}")
        print(f"  Без дубликатов: {r['unique']}")
    elif t in ("int", "float"):
        print(f"  Чётные: {r['evens']}, Количество: {r['even_count']}")
    elif t == "str":
        print(f"  Числа: {r['nums']}, Сумма: {r['sum']}")


def main() -> None:
    print("=" * 60)
    print("Задание 2.2: Универсальная функция (try/except/finally)")
    print("=" * 60)

    test_cases = [
        ("Кортеж", ("Python", "MachineLearning", "BSUIR")),
        ("Список", [4, 10, -3, 8, 2, -5, 10, 8, 1]),
        ("Число целое", 2468135790),
        ("Число float", 4820.62),
        ("Строка", "Заказ 405: 12 пирожных, 3 торта, скидка -50 руб"),
        ("Ошибочный тип", {1, 2, 3}),
    ]

    for title, val in test_cases:
        print(f"\n--- {title}: {val} ---")
        res = process_data(val)
        display_result(res)


if __name__ == "__main__":
    main()
