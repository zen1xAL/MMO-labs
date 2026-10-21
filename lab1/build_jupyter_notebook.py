"""
Скрипт для сборки полноценного Jupyter Notebook (LR01_Variant7.ipynb)
со всеми тремя частями лабораторной работы, подробным описанием заданий,
исходным кодом и сохраненными результатами выполнения ячеек (outputs).
"""

import json
import os
import subprocess
import sys
from typing import Any, Dict, List


def run_script_capture(script_path: str, cwd: str, stdin_data: str = None) -> List[str]:
    """Запускает скрипт и перехватывает вывод в UTF-8, разбивая по строкам."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, script_path],
        cwd=cwd,
        input=stdin_data,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    lines = proc.stdout.splitlines(keepends=True)
    return [l if l.endswith("\n") else l + "\n" for l in lines]


def make_md_cell(content: str) -> Dict[str, Any]:
    lines = [l + "\n" for l in content.strip().split("\n")]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines,
    }


def make_code_cell(code: str, outputs: List[str], exec_count: int) -> Dict[str, Any]:
    lines = [l + "\n" for l in code.strip().split("\n")]
    cell_outputs = []
    if outputs:
        cell_outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": outputs,
        })

    return {
        "cell_type": "code",
        "execution_count": exec_count,
        "metadata": {},
        "outputs": cell_outputs,
        "source": lines,
    }


def load_code(rel_path: str) -> str:
    with open(os.path.join(r"d:\MMO", rel_path), "r", encoding="utf-8") as f:
        return f.read()


def build_notebook():
    cells: List[Dict[str, Any]] = []
    exec_count = 1

    # Заголовочная ячейка ноутбука
    header_md = (
        "# Лабораторная работа №1\n"
        "### Дисциплина: Методы машинного обучения\n"
        "**Белорусский государственный университет информатики и радиоэлектроники (БГУИР)**  \n"
        "Факультет компьютерных систем и сетей (ФКСиС), кафедра ПОИТ  \n\n"
        "**Выполнил:** студент гр. 351002 Власовец А. И.  \n"
        "**Проверил:** преподаватель Лебедевич А. В.  \n"
        "**Вариант:** 7\n\n"
        "---"
    )
    cells.append(make_md_cell(header_md))

    # =========================================================================
    # ЧАСТЬ 1
    # =========================================================================
    part1_header = (
        "## Часть 1. Основы синтаксиса, управляющие конструкции и коллекции Python\n"
        "В данной части рассматриваются базовые типы данных, арифметические операции, "
        "условные операторы ветвления, циклы, манипуляции со строками, списками, словарями и кортежами."
    )
    cells.append(make_md_cell(part1_header))

    # Задание 1.1
    t1_md = (
        "### Задание 1.1. Сумма нечетных цифр натурального числа\n"
        "**Условие:** Найти сумму нечетных цифр введенного натурального числа (1 балл)."
    )
    cells.append(make_md_cell(t1_md))
    c1 = load_code("part1/task1_sum_odd_digits.py")
    out1 = run_script_capture("task1_sum_odd_digits.py", "d:/MMO/part1", "9753124\n")
    cells.append(make_code_cell(c1, out1, exec_count))
    exec_count += 1

    # Задание 1.2
    t2_md = (
        "### Задание 1.2. Пары регистров и подсчет согласных букв\n"
        "**Условие:** Посчитать, сколько пар (стоят рядом) верхнего и нижнего регистра находится "
        "в веденном с клавиатуры слове (Пример: `HjkLM` - 1 пара нижнего, 1 пара верхнего), "
        "а также сколько согласных букв в слове (2 балла)."
    )
    cells.append(make_md_cell(t2_md))
    c2 = load_code("part1/task2_letter_pairs_consonants.py")
    out2 = run_script_capture("task2_letter_pairs_consonants.py", "d:/MMO/part1", "HjkLM\n")
    cells.append(make_code_cell(c2, out2, exec_count))
    exec_count += 1

    # Задание 1.3
    t3_md = (
        "### Задание 1.3. Обработка списка чисел и строк\n"
        "**Условие:** Дан список `list=[1612, 49, 'hello', 6, 19, 'world']`. Все числа этого списка "
        "проверить на чётность. Если число чётное, то посчитать сумму его цифр. Если нечётное, то заменить его на 1 в списке. "
        "Все слова: посчитать количество гласных и согласных. Вывести всё на экран (2 балла)."
    )
    cells.append(make_md_cell(t3_md))
    c3 = load_code("part1/task3_list_parity_analysis.py")
    out3 = run_script_capture("task3_list_parity_analysis.py", "d:/MMO/part1")
    cells.append(make_code_cell(c3, out3, exec_count))
    exec_count += 1

    # Задание 1.4
    t4_md = (
        "### Задание 1.4. Сортировка словаря по значению\n"
        "**Условие:** Отсортируйте словарь по значению в порядке возрастания и убывания (2 балла)."
    )
    cells.append(make_md_cell(t4_md))
    c4 = load_code("part1/task4_dict_sorting.py")
    out4 = run_script_capture("task4_dict_sorting.py", "d:/MMO/part1")
    cells.append(make_code_cell(c4, out4, exec_count))
    exec_count += 1

    # Задание 1.5
    t5_md = (
        "### Задание 1.5. Программа «Кондитерская»\n"
        "**Условие:** Реализуйте программу «Кондитерская», которая будет включать в себя шесть пунктов меню:\n"
        "1. Просмотр описания: название – описание\n"
        "2. Просмотр цены: название – цена\n"
        "3. Просмотр количества: название – количество\n"
        "4. Всю информацию\n"
        "5. Покупка (выбор товаров, расчет стоимости, контроль остатков)\n"
        "6. До свидания (2 балла)."
    )
    cells.append(make_md_cell(t5_md))
    c5 = load_code("part1/task5_confectionery_store.py")
    out5 = run_script_capture("task5_confectionery_store.py", "d:/MMO/part1", "4\n5\nПирожное 'Эклер'\n400\nТорт 'Наполеон'\n500\nn\n6\n")
    cells.append(make_code_cell(c5, out5, exec_count))
    exec_count += 1

    # Задание 1.6
    t6_md = (
        "### Задание 1.6. Сортировка кортежа по убыванию\n"
        "**Условие:** Дан кортеж целых чисел. Отсортировать его в порядке убывания. "
        "Вывести первый и последний элемент кортежа (1 балл)."
    )
    cells.append(make_md_cell(t6_md))
    c6 = load_code("part1/task6_tuple_sorting.py")
    out6 = run_script_capture("task6_tuple_sorting.py", "d:/MMO/part1", "45 12 88 -3 100 0 7\n")
    cells.append(make_code_cell(c6, out6, exec_count))
    exec_count += 1

    # =========================================================================
    # ЧАСТЬ 2
    # =========================================================================
    part2_header = (
        "## Часть 2. Функции, обработка двумерных массивов и блок try\\except\\finally\n"
        "**Общее требование:** Все задания выполнить с использованием функций и обработкой "
        "исключительных ситуаций при помощи блока `try...except...finally`."
    )
    cells.append(make_md_cell(part2_header))

    # Задание 2.1
    t21_md = (
        "### Задание 2.1. Функция проверки надежности пароля `is_password_good(password)`\n"
        "**Условие:** Напишите функцию `is_password_good(password)`, которая принимает строковое значение "
        "и возвращает True, если пароль надежен (длина не менее 10 символов, содержит как минимум "
        "одну заглавную и одну строчную букву), иначе False (2 балла)."
    )
    cells.append(make_md_cell(t21_md))
    c21 = load_code("part2/task1_password_check.py")
    out21 = run_script_capture("task1_password_check.py", "d:/MMO/part2")
    cells.append(make_code_cell(c21, out21, exec_count))
    exec_count += 1

    # Задание 2.2
    t22_md = (
        "### Задание 2.2. Универсальная функция обработки разнотипных структур данных\n"
        "**Условие:** Напишите функцию, которая принимает один аргумент:\n"
        "- Кортеж: посчитать длину всех его слов;\n"
        "- Список: сумму после первого отрицательного элемента, удалить дубликаты;\n"
        "- Число: количество четных цифр;\n"
        "- Строка: найти сумму всех чисел.\n"
        "Сделать проверку со всеми этими случаями (4 балла)."
    )
    cells.append(make_md_cell(t22_md))
    c22 = load_code("part2/task2_multi_type_processor.py")
    out22 = run_script_capture("task2_multi_type_processor.py", "d:/MMO/part2")
    cells.append(make_code_cell(c22, out22, exec_count))
    exec_count += 1

    # Задание 2.3
    t23_md = (
        "### Задание 2.3. Перестановка столбцов двумерного массива\n"
        "**Условие:** Дан двумерный массив и два числа: i и j. Поменяйте в массиве столбцы с номерами i и j "
        "и выведите результат. Программа получает на вход размеры массива n и m, затем элементы массива, затем числа i и j (3 балла)."
    )
    cells.append(make_md_cell(t23_md))
    c23 = load_code("part2/task3_matrix_column_swap.py")
    out23 = run_script_capture("task3_matrix_column_swap.py", "d:/MMO/part2")
    cells.append(make_code_cell(c23, out23, exec_count))
    exec_count += 1

    # Задание 2.4
    t24_md = (
        "### Задание 2.4. Демонстрация работы конструкции `try...except...else...finally`\n"
        "**Условие:** Напишите программу, демонстрирующую работу try\\except\\finally (2 балла)."
    )
    cells.append(make_md_cell(t24_md))
    c24 = load_code("part2/task4_exceptions_demo.py")
    out24 = run_script_capture("task4_exceptions_demo.py", "d:/MMO/part2")
    cells.append(make_code_cell(c24, out24, exec_count))
    exec_count += 1

    # =========================================================================
    # ЧАСТЬ 3
    # =========================================================================
    part3_header = (
        "## Часть 3. Объектно-ориентированное программирование\n"
        "В данной части реализуются пользовательские классы, механизмы инкапсуляции через свойства, "
        "наследование, полиморфизм, методы экземпляра, класса и статические методы, а также сохранение в файлы."
    )
    cells.append(make_md_cell(part3_header))

    # Задание 3.1
    t31_md = (
        "### Задание 3.1. Пользовательский класс `CustomList`\n"
        "**Условие:** Создать класс List (список), в котором реализовать методы для работы со списком (не менее 5) (1 балл)."
    )
    cells.append(make_md_cell(t31_md))
    c31 = load_code("part3/task1_custom_list.py")
    out31 = run_script_capture("task1_custom_list.py", "d:/MMO/part3")
    cells.append(make_code_cell(c31, out31, exec_count))
    exec_count += 1

    # Задание 3.2
    t32_md = (
        "### Задание 3.2. Иерархия классов транспортных средств\n"
        "**Условие:** Создать классы «Транспортное средство», «Самолет», «Поезд», «Автомобиль». "
        "Определить время и стоимость перевозки для указанных городов и расстояний. "
        "Вывести данные о наиболее быстрой и экономичной поездке. Предусмотреть метод записи информации в файл (3 балла)."
    )
    cells.append(make_md_cell(t32_md))
    c32 = load_code("part3/task2_transport_hierarchy.py")
    out32 = run_script_capture("task2_transport_hierarchy.py", "d:/MMO/part3")
    cells.append(make_code_cell(c32, out32, exec_count))
    exec_count += 1

    # Задание 3.3
    t33_md = (
        "### Задание 3.3. Система управления библиотекой: `Book`, `Department`, `Library`\n"
        "**Условие:** Создать классы: «Книга», «Отдел», «Библиотека». В классах реализовать следующие методы: "
        "добавление, удаление, изменение названия книг из отделов. Классы должны содержать методы доступа и изменения всех полей. "
        "Предусмотреть метод записи информации в файл (3 балла)."
    )
    cells.append(make_md_cell(t33_md))
    c33 = load_code("part3/task3_library_system.py")
    out33 = run_script_capture("task3_library_system.py", "d:/MMO/part3")
    cells.append(make_code_cell(c33, out33, exec_count))
    exec_count += 1

    # Задание 3.4
    t34_md = (
        "### Задание 3.4. Класс `StudentAccount` с методами экземпляра, класса и статическими методами\n"
        "**Условие:** Придумать класс самостоятельно, реализовать в нем методы экземпляра класса, "
        "статические методы, методы класса (1–3 балла)."
    )
    cells.append(make_md_cell(t34_md))
    c34 = load_code("part3/task4_class_methods_demo.py")
    out34 = run_script_capture("task4_class_methods_demo.py", "d:/MMO/part3")
    cells.append(make_code_cell(c34, out34, exec_count))
    exec_count += 1

    # Финальные выводы в ноутбуке
    concl_md = (
        "## Выводы по лабораторной работе\n"
        "В ходе выполнения комплексной лабораторной работы по дисциплине «Методы машинного обучения» "
        "были всесторонне изучены и практически закреплены ключевые аспекты программирования на языке Python: "
        "базовые типы данных, коллекции, функции, надежная обработка исключений try-except-finally, "
        "работа с многомерными матрицами и принципы объектно-ориентированного программирования (ООП)."
    )
    cells.append(make_md_cell(concl_md))

    # Структура документа ipynb
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbformat": 4,
                "nbformat_minor": 5,
                "pygments_lexer": "ipython3",
                "version": "3.13.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    out_path = r"d:\MMO\LR01_Variant7.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

    print(f"Jupyter Notebook успешно создан: {out_path}")
    print(f"Всего ячеек: {len(cells)} (из них кода: {exec_count - 1})")


if __name__ == "__main__":
    build_notebook()
