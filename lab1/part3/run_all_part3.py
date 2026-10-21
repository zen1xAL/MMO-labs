"""
Запуск всех заданий Части 3 (Вариант 7).
"""

import subprocess
import sys


def run_script(script_name: str, args: list = None) -> None:
    cmd = [sys.executable, script_name] + (args or [])
    print(f"\n{'='*70}\n>>> ЗАПУСК {script_name}\n{'='*70}")
    subprocess.run(cmd, check=True)


def main() -> None:
    tasks = [
        ("task1_custom_list.py", []),
        ("task2_transport_hierarchy.py", []),
        ("task3_library_system.py", []),
        ("task4_class_methods_demo.py", []),
    ]

    for script, args in tasks:
        run_script(f"d:/MMO/part3/{script}", args)


if __name__ == "__main__":
    main()
