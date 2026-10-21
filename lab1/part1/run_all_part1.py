"""
Запуск всех заданий Части 1 (Вариант 7).
"""

import subprocess
import sys


def run_script(script_name: str, args: list = None) -> None:
    cmd = [sys.executable, script_name] + (args or [])
    print(f"\n{'='*70}\n>>> ЗАПУСК {script_name}\n{'='*70}")
    subprocess.run(cmd, check=True)


def main() -> None:
    tasks = [
        ("task1_sum_odd_digits.py", []),
        ("task2_letter_pairs_consonants.py", []),
        ("task3_list_parity_analysis.py", []),
        ("task4_dict_sorting.py", []),
        ("task5_confectionery_store.py", ["--demo"]),
        ("task6_tuple_sorting.py", []),
    ]

    for script, args in tasks:
        run_script(f"d:/MMO/part1/{script}", args)


if __name__ == "__main__":
    main()
