"""
Запуск всех заданий Части 2 (Вариант 7).
"""

import subprocess
import sys


def run_script(script_name: str, args: list = None) -> None:
    cmd = [sys.executable, script_name] + (args or [])
    print(f"\n{'='*70}\n>>> ЗАПУСК {script_name}\n{'='*70}")
    subprocess.run(cmd, check=True)


def main() -> None:
    tasks = [
        ("task1_password_check.py", []),
        ("task2_multi_type_processor.py", []),
        ("task3_matrix_column_swap.py", ["--demo"]),
        ("task4_exceptions_demo.py", []),
    ]

    for script, args in tasks:
        run_script(f"d:/MMO/part2/{script}", args)


if __name__ == "__main__":
    main()
