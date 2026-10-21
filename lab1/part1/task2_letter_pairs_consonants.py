"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 2.

Условие:
Посчитать, сколько пар (стоят рядом) верхнего и нижнего регистра находится
в введенном слове (Пример HjkLM: 1 пара нижн., 1 верхн.),
а также сколько согласных букв в слове.
"""

from typing import Dict, List, Tuple

VOWELS = set("aeiou" "аеёиоуыэюя")
CONSONANTS = set("bcdfghjklmnpqrstvwxyz" "бвгджзйклмнпрстфхцчшщ")


def analyze_word(word: str) -> Dict[str, object]:
    """
    Анализирует пары регистров и согласные в слове.
    """
    cleaned = word.strip()
    upper_pairs: List[Tuple[str, str]] = []
    lower_pairs: List[Tuple[str, str]] = []

    for i in range(len(cleaned) - 1):
        c1, c2 = cleaned[i], cleaned[i + 1]
        if c1.isalpha() and c2.isalpha():
            if c1.isupper() and c2.isupper():
                upper_pairs.append((c1, c2))
            elif c1.islower() and c2.islower():
                lower_pairs.append((c1, c2))

    consonants = [c for c in cleaned if c.lower() in CONSONANTS]

    return {
        "word": cleaned,
        "upper_cnt": len(upper_pairs),
        "upper_pairs": [f"{a}{b}" for a, b in upper_pairs],
        "lower_cnt": len(lower_pairs),
        "lower_pairs": [f"{a}{b}" for a, b in lower_pairs],
        "cons_cnt": len(consonants),
        "consonants": consonants,
    }


def print_analysis(res: Dict[str, object]) -> None:
    print(f"Слово: '{res['word']}'")
    print(f"  Верхний регистр: {res['upper_cnt']} {res['upper_pairs']}")
    print(f"  Нижний регистр:  {res['lower_cnt']} {res['lower_pairs']}")
    print(f"  Согласных букв: {res['cons_cnt']} {res['consonants']}\n")


def main() -> None:
    print("=" * 60)
    print("Задание 1.2: Пары регистров и подсчет согласных букв")
    print("=" * 60)

    test_words = ["HjkLM", "AbcDEfghIJ", "Python", "Программирование"]
    print("\n--- Демонстрация на контрольных словах ---")
    for w in test_words:
        res = analyze_word(w)
        print_analysis(res)

    print("--- Пользовательский ввод ---")
    user_word = input("Введите слово (Enter для пропуска): ").strip()
    if user_word:
        res = analyze_word(user_word)
        print_analysis(res)


if __name__ == "__main__":
    main()
