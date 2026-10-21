"""
Лабораторная работа №1. Часть 2.
Вариант 7. Задание 3.

Требование:
Все задания выполнить с использованием функций и обработкой
исключительных ситуаций при помощи блока try\\except\\finally.

Условие:
Дан двумерный массив и два числа: i и j. Поменяйте в массиве столбцы
с номерами i и j и выведите результат.
"""

import sys
from typing import Any, List, Optional


def print_matrix(matrix: List[List[Any]], title: str) -> None:
    print(f"\n{title}:")
    if not matrix or not matrix[0]:
        print("  [Матрица пуста]")
        return
    m = len(matrix[0])
    print("      " + " ".join(f"[{c:^3}]" for c in range(m)))
    print("      " + "-" * (m * 6))
    for r_idx, row in enumerate(matrix):
        print(f"[{r_idx:^2}] | " + " ".join(f"{val:>4}" for val in row))


def swap_matrix_columns(
    matrix: List[List[Any]], col_i: int, col_j: int
) -> Optional[List[List[Any]]]:
    result = None
    try:
        if not matrix or not isinstance(matrix, list):
            raise ValueError("Матрица должна быть непустым списком строк.")

        n, m = len(matrix), len(matrix[0])
        for r_idx, row in enumerate(matrix):
            if len(row) != m:
                raise ValueError(f"Строка {r_idx}: некорректная длина.")

        if not (0 <= col_i < m) or not (0 <= col_j < m):
            raise IndexError(
                f"Индексы {col_i}, {col_j} вне диапазона [0, {m-1}]."
            )

        result = [list(row) for row in matrix]
        for row in result:
            row[col_i], row[col_j] = row[col_j], row[col_i]
        return result

    except (ValueError, IndexError, TypeError) as exc:
        print(f"  [Ошибка матрицы]: {exc}")
        return None
    finally:
        st = "УСПЕШНО" if result is not None else "ОШИБКА"
        print(f"  [finally]: Обмен столбцов {col_i} и {col_j} -> {st}")


def main() -> None:
    print("=" * 60)
    print("Задание 2.3: Перестановка столбцов матрицы")
    print("=" * 60)

    sample = [
        [11, 12, 13, 14, 15],
        [21, 22, 23, 24, 25],
        [31, 32, 33, 34, 35],
        [41, 42, 43, 44, 45],
    ]
    col_i, col_j = 1, 3
    print_matrix(sample, "Исходная матрица (4x5)")
    print(f"\nМеняем столбцы {col_i} и {col_j}:")
    swapped = swap_matrix_columns(sample, col_i, col_j)
    if swapped:
        print_matrix(swapped, f"Результат после обмена {col_i} и {col_j}")

    print("\n--- Проверка исключения при выходе за границы (i=10) ---")
    swap_matrix_columns(sample, 10, 1)


if __name__ == "__main__":
    main()
