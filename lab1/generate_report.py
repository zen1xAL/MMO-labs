"""
Генератор отчета по лабораторной работе №1 (Части 1, 2, 3).
Оформление строго по стандарту БГУИР СТП 01-2017 с учетом всех правок:
- Титульный лист: весь текст НЕ жирным шрифтом.
- Исполнитель: студент гр. 351002 Власовец А. И.
- Проверил: Лебедевич А. В.
- Код: Courier New 9.0 пт, одинарный интервал, БЕЗ рамок и обводок (чистый текст).
- Цель и выводы: сплошные цельные абзацы без деления на списки 1, 2, 3.
- Поля: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм.
- Номер страницы: в правом нижнем углу со 2 страницы.
"""

import os
from typing import List

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor


def add_code_block(doc, code_text: str):
    """
    Добавляет код программы как простой чистый текст моноширинным шрифтом
    Courier New 9.0 пт без каких-либо рамок, таблиц или фона.
    """
    for line in code_text.strip().split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Mm(0)
        p.paragraph_format.left_indent = Mm(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(line)
        run.font.name = "Courier New"
        run.font.size = Pt(9.0)
        run.font.bold = False
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Небольшой интервал после блока кода
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.first_line_indent = Mm(0)
    p_sp.paragraph_format.line_spacing = 1.0
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)


def add_page_number_to_footer(footer):
    """Добавляет номер страницы в правом нижнем углу согласно СТП 01-2017 п. 2.2.8."""
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = False

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def create_report():
    doc = docx.Document()

    # 1. Поля страницы по СТП 01-2017 (Приложение Л)
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)

    # Титульный лист без номера, последующие страницы нумеруются
    section.different_first_page_header_footer = True
    add_page_number_to_footer(section.footer)

    # 2. Базовый стиль основного текста по СТП 01-2017 п. 2.1.1, 2.1.3:
    # Times New Roman 14 пт, 1.5 интервал, абзац 1.25 см, выравнивание по ширине
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Times New Roman"
    style_normal.font.size = Pt(14)
    style_normal.font.bold = False
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.space_after = Pt(0)
    style_normal.paragraph_format.first_line_indent = Mm(12.5)

    # =========================================================================
    # ТИТУЛЬНЫЙ ЛИСТ (весь текст НЕ жирным шрифтом)
    # =========================================================================

    p_header = doc.add_paragraph()
    p_header.paragraph_format.first_line_indent = Mm(0)
    p_header.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.line_spacing = 1.15
    run = p_header.add_run(
        "МИНИСТЕРСТВО ОБРАЗОВАНИЯ РЕСПУБЛИКИ БЕЛАРУСЬ\n"
        "БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ\n"
        "ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ\n"
        "Факультет компьютерных систем и сетей\n"
        "Кафедра программного обеспечения информационных технологий\n"
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = False

    for _ in range(6):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    p_title = doc.add_paragraph()
    p_title.paragraph_format.first_line_indent = Mm(0)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.3

    r1 = p_title.add_run("ОТЧЕТ\nПО ЛАБОРАТОРНОЙ РАБОТЕ № 1\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(16)
    r1.font.bold = False

    r2 = p_title.add_run(
        "по дисциплине «Методы машинного обучения»\n\n"
        "Вариант № 7"
    )
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = False

    for _ in range(6):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    # Таблица для подписей (2 колонки: левая пустая 9.0 см, правая 7.5 см)
    sign_table = doc.add_table(rows=1, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False

    cell_left = sign_table.cell(0, 0)
    cell_right = sign_table.cell(0, 1)
    cell_left.width = Mm(90)
    cell_right.width = Mm(75)

    p_right = cell_right.paragraphs[0]
    p_right.paragraph_format.first_line_indent = Mm(0)
    p_right.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_right.paragraph_format.line_spacing = 1.2
    run_sign = p_right.add_run(
        "Выполнил:\n"
        "студент гр. 351002\n"
        "Власовец А. И.\n\n"
        "Проверил:\n"
        "преподаватель\n"
        "Лебедевич А. В.\n"
    )
    run_sign.font.name = "Times New Roman"
    run_sign.font.size = Pt(13)
    run_sign.font.bold = False

    for _ in range(6):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    p_city = doc.add_paragraph()
    p_city.paragraph_format.first_line_indent = Mm(0)
    p_city.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_city.add_run("Минск 2026")
    r_city.font.name = "Times New Roman"
    r_city.font.size = Pt(12)
    r_city.font.bold = False

    # Переход на следующую страницу (начиная со 2 страницы идет нумерация)
    doc.add_page_break()

    # Функции для оформления заголовков разделов по СТП 01-2017:
    def add_sec_h1(title_text: str):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.bold = True
        return p

    def add_sec_h2(title_text: str):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.bold = True
        return p

    def add_figure_caption(text: str):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Mm(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(10)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)

    # =========================================================================
    # 1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ (цельный текст без разбиения на 1, 2, 3)
    # =========================================================================
    add_sec_h1("1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ")

    doc.add_paragraph(
        "Целью выполнения лабораторной работы является изучение языка программирования Python "
        "и получение практических навыков его применения при решении задач компьютерной обработки данных. "
        "В рамках работы осуществляется комплексное освоение базового синтаксиса языка, стандартных типов данных, "
        "управляющих конструкций ветвления и циклов, приобретаются устойчивые навыки манипуляции встроенными коллекциями, "
        "включая строки, списки, кортежи и ассоциативные словари."
    )
    doc.add_paragraph(
        "В процессе выполнения заданий исследуются принципы функциональной декомпозиции программ, "
        "методы работы с двумерными числовыми массивами и организация отказоустойчивых алгоритмов "
        "на основе синтаксической конструкции try...except...finally. На завершающем этапе осваивается "
        "парадигма объектно-ориентированного программирования, проектирование классов с инкапсуляцией полей "
        "через свойства, применение механизмов наследования и полиморфизма, разграничение методов экземпляра, "
        "методов класса и статических методов, а также интеграция файлового ввода-вывода информации."
    )

    # =========================================================================
    # 2 ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ (не более 4 страниц по условию)
    # =========================================================================
    add_sec_h1("2 ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ")

    add_sec_h2("2.1 Базовые структуры данных и коллекции языка Python")
    doc.add_paragraph(
        "Язык Python поддерживает развитый набор встроенных скалярных и составных типов данных. "
        "Основными скалярными типами являются целые числа произвольной разрядности int, числа с плавающей "
        "точкой double-точности float, логические значения bool и неизменяемые последовательности символов Unicode str. "
        "Управление ходом вычислений обеспечивается условным оператором if-elif-else, а также циклическими конструкциями "
        "for и while. Принятый в языке синтаксис отступов жестко определяет блочную структуру программы."
    )
    doc.add_paragraph(
        "Коллекции в Python разделяются на изменяемые (mutable) и неизменяемые (immutable). "
        "Динамический список list представляет собой индексированный массив ссылок на произвольные объекты, "
        "поддерживающий вставку, удаление, срезы и сортировку алгоритмом Timsort. Кортеж tuple является неизменяемым "
        "аналогом списка с минимальным расходом памяти и фиксированной структурой. Словарь dict реализует "
        "ассоциативный массив на основе хеш-таблицы с константным средним временем доступа к элементам по ключу."
    )

    add_sec_h2("2.2 Функции и обработка исключений try-except-finally")
    doc.add_paragraph(
        "Функции в Python определяются с помощью ключевого слова def и позволяют разделять программу на логически "
        "независимые подпрограммы. Для предотвращения аварийных сбоев программы применяется развитый механизм исключений. "
        "Синтаксическая конструкция try-except-else-finally включает блок try с потенциально опасным кодом, блоки except "
        "для перехвата конкретных классов ошибок, блок else, выполняющийся при успешном завершении без исключений, "
        "и обязательный блок finally, команды которого выполняются гарантированно независимо от исхода вычислений, "
        "что обеспечивает надежное освобождение дескрипторов файлов и системных ресурсов."
    )

    add_sec_h2("2.3 Двумерные массивы (матрицы)")
    doc.add_paragraph(
        "В базовом синтаксисе Python двумерные числовые массивы формируются в виде вложенных списков. "
        "Доступ к элементам матрицы осуществляется двойным индексом строки и столбца matrix[i][j]. "
        "Операция перестановки столбцов требует поэлементного обмена значений в цикле по каждой строке матрицы. "
        "При манипуляциях с многомерными структурами обязательным условием надежности является валидация прямоугольности "
        "матрицы и проверка попадания индексов столбцов в допустимый диапазон размерностей."
    )

    add_sec_h2("2.4 Объектно-ориентированное программирование")
    doc.add_paragraph(
        "Парадигма ООП в Python базируется на проектировании пользовательских классов. Инкапсуляция реализуется "
        "путем сокрытия полей с префиксом подчеркивания и предоставления контролируемого доступа через декораторы "
        "@property и @<field>.setter. Механизм наследования позволяет создавать специализированные классы-потомки, "
        "расширяющие функционал базовых классов посредством вызова конструктора super().__init__(...). "
        "Полиморфизм обеспечивает единый интерфейс взаимодействия с разнородными классами иерархии."
    )
    doc.add_paragraph(
        "В объектной модели Python четко разграничены методы трех категорий: методы экземпляра, принимающие self "
        "и оперирующие состоянием конкретного объекта; методы класса с декоратором @classmethod, принимающие ссылку "
        "на класс cls и выступающие фабриками или регуляторами параметров класса; статические методы с декоратором "
        "@staticmethod, представляющие собой служебные функции общего назначения, логически привязанные к классу."
    )

    # =========================================================================
    # 3 ФОРМУЛИРОВКА ИНДИВИДУАЛЬНОГО ЗАДАНИЯ
    # =========================================================================
    add_sec_h1("3 ФОРМУЛИРОВКА ИНДИВИДУАЛЬНОГО ЗАДАНИЯ")

    add_sec_h2("3.1 Задания Части 1 (Вариант 7)")
    doc.add_paragraph("Задание 1: Найти сумму нечетных цифр введенного натурального числа (1 балл).")
    doc.add_paragraph(
        "Задание 2: Посчитать, сколько пар (стоят рядом) верхнего и нижнего регистра находится в введенном "
        "с клавиатуры слове (Пример HjkLM - 1 пара нижнего, 1 пара верхнего), а также сколько согласных букв в слове (2 балла)."
    )
    doc.add_paragraph(
        "Задание 3: Дан список list=[1612,49,'hello',6,19,'world’]. Все числа этого списка проверить на чётность. "
        "Если число чётное, то посчитать сумму его цифр. Если нечётное, то заменить его на 1 в списке. "
        "Все слова: посчитать количество гласных и согласных. Вывести всё на экран (2 балла)."
    )
    doc.add_paragraph("Задание 4: Отсортируйте словарь по значению в порядке возрастания и убывания (2 балла).")
    doc.add_paragraph(
        "Задание 5: Реализуйте программу «Кондитерская», которая будет включать в себя шесть пунктов меню. "
        "У вас есть словарь, где ключ – название продукции (торт, пирожное, маффин и т.д.). Значение – список, "
        "который содержит состав, цену (за 100гр) и кол-во (в граммах):\n"
        "1. Просмотр описания: название – описание\n"
        "2. Просмотр цены: название – цена\n"
        "3. Просмотр количества: название – количество\n"
        "4. Всю информацию\n"
        "5. Покупка: в пункте «Покупка» необходимо совершить покупку, с клавиатуры вводить название продукции "
        "и его кол-во, n – выход из программы. Посчитать цену выбранных товаров и сколько товаров осталось в изначальном списке\n"
        "6. До свидания (2 балла)."
    )
    doc.add_paragraph(
        "Задание 6: Дан кортеж целых чисел. Отсортировать его в порядке убывания. Вывести первый и последний "
        "элемент кортежа (1 балл)."
    )

    add_sec_h2("3.2 Задания Части 2 (Вариант 7)")
    doc.add_paragraph(
        "Общее требование: Все задания выполнить с использованием функций и обработкой исключительных "
        "ситуаций при помощи блока try\\except\\finally."
    )
    doc.add_paragraph(
        "Задание 1: Напишите функцию is_password_good(password), которая принимает в качестве аргумента строковое "
        "значение пароля password и возвращает значение True если пароль является надежным и False в противном случае. "
        "Пароль является надежным если: его длина не менее 10 символов; содержит как минимум одну заглавную букву; "
        "содержит как минимум одну строчную букву (2 балла)."
    )
    doc.add_paragraph(
        "Задание 2: Напишите функцию, которая будет принимать один аргумент. Если в функцию передаётся кортеж, "
        "то посчитать длину всех его слов. Если список, то сумму после первого отрицательного элемента. "
        "Удалить все повторяющиеся элементы. Число – кол-во четных цифр. Строка – найти сумму всех чисел. "
        "Сделать проверку со всеми этими случаями (4 балла)."
    )
    doc.add_paragraph(
        "Задание 3: Дан двумерный массив и два числа: i и j. Поменяйте в массиве столбцы с номерами i и j и "
        "выведите результат. Программа получает на вход размеры массива n и m, затем элементы массива, затем числа i и j (3 балла)."
    )
    doc.add_paragraph("Задание 4: Напишите программу, демонстрирующую работу try\\except\\finally (2 балла).")

    add_sec_h2("3.3 Задания Части 3 (Вариант 7)")
    doc.add_paragraph(
        "Задание 1: Создать класс List (список), в котором реализовать методы для работы со списком (не менее 5) (1 балл)."
    )
    doc.add_paragraph(
        "Задание 2: Создать классы «Транспортное средство», «Самолет», «Поезд», «Автомобиль». Определить время "
        "и стоимость перевозки для указанных городов и расстояний. Вывести данные о наиболее быстрой и экономичной поездке. "
        "Предусмотреть метод записи информации в файл (3 балла)."
    )
    doc.add_paragraph(
        "Задание 3: Создать классы: «Книга», «Отдел», «Библиотека». В классах реализовать следующие методы: "
        "добавление, удаление, изменение названия книг из отделов. Классы должны содержать методы доступа и изменения всех полей. "
        "Предусмотреть метод записи информации в файл (3 балла)."
    )
    doc.add_paragraph(
        "Задание 4: Придумать класс самостоятельно, реализовать в нем методы экземпляра класса, статические методы, "
        "методы класса (1–3 балла)."
    )

    # =========================================================================
    # 4 КОД РЕШЕНИЯ ИНДИВИДУАЛЬНОГО ЗАДАНИЯ (чистый текст, без рамок)
    # =========================================================================
    add_sec_h1("4 КОД РЕШЕНИЯ ИНДИВИДУАЛЬНОГО ЗАДАНИЯ")

    def load_code(rel_path: str) -> str:
        full_p = os.path.join(r"d:\MMO", rel_path)
        with open(full_p, "r", encoding="utf-8") as f:
            return f.read()

    def add_listing_header(title: str):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True

    add_sec_h2("4.1 Программы Части 1 (Основы языка Python)")

    add_listing_header("Листинг 4.1 – Вычисление суммы нечетных цифр числа (task1_sum_odd_digits.py)")
    add_code_block(doc, load_code("part1/task1_sum_odd_digits.py"))

    add_listing_header("Листинг 4.2 – Анализ пар регистров и согласных букв (task2_letter_pairs_consonants.py)")
    add_code_block(doc, load_code("part1/task2_letter_pairs_consonants.py"))

    add_listing_header("Листинг 4.3 – Анализ четности чисел и слов в списке (task3_list_parity_analysis.py)")
    add_code_block(doc, load_code("part1/task3_list_parity_analysis.py"))

    add_listing_header("Листинг 4.4 – Сортировка словаря по значениям (task4_dict_sorting.py)")
    add_code_block(doc, load_code("part1/task4_dict_sorting.py"))

    add_listing_header("Листинг 4.5 – Консольная программа «Кондитерская» (task5_confectionery_store.py)")
    add_code_block(doc, load_code("part1/task5_confectionery_store.py"))

    add_listing_header("Листинг 4.6 – Сортировка кортежа по убыванию (task6_tuple_sorting.py)")
    add_code_block(doc, load_code("part1/task6_tuple_sorting.py"))

    add_sec_h2("4.2 Программы Части 2 (Функции, матрицы и блок try\\except\\finally)")

    add_listing_header("Листинг 4.7 – Проверка надежности пароля is_password_good (task1_password_check.py)")
    add_code_block(doc, load_code("part2/task1_password_check.py"))

    add_listing_header("Листинг 4.8 – Универсальная функция обработки структур (task2_multi_type_processor.py)")
    add_code_block(doc, load_code("part2/task2_multi_type_processor.py"))

    add_listing_header("Листинг 4.9 – Перестановка столбцов двумерного массива (task3_matrix_column_swap.py)")
    add_code_block(doc, load_code("part2/task3_matrix_column_swap.py"))

    add_listing_header("Листинг 4.10 – Демонстрация работы try/except/else/finally (task4_exceptions_demo.py)")
    add_code_block(doc, load_code("part2/task4_exceptions_demo.py"))

    add_sec_h2("4.3 Программы Части 3 (Объектно-ориентированное программирование)")

    add_listing_header("Листинг 4.11 – Пользовательский класс CustomList (task1_custom_list.py)")
    add_code_block(doc, load_code("part3/task1_custom_list.py"))

    add_listing_header("Листинг 4.12 – Иерархия классов транспортных средств (task2_transport_hierarchy.py)")
    add_code_block(doc, load_code("part3/task2_transport_hierarchy.py"))

    add_listing_header("Листинг 4.13 – Система классов Книга - Отдел - Библиотека (task3_library_system.py)")
    add_code_block(doc, load_code("part3/task3_library_system.py"))

    add_listing_header("Листинг 4.14 – Класс StudentAccount с методами разных типов (task4_class_methods_demo.py)")
    add_code_block(doc, load_code("part3/task4_class_methods_demo.py"))

    # =========================================================================
    # 5 СКРИНШОТЫ ВЫПОЛНЕНИЯ ИНДИВИДУАЛЬНОГО ЗАДАНИЯ
    # =========================================================================
    add_sec_h1("5 СКРИНШОТЫ ВЫПОЛНЕНИЯ ИНДИВИДУАЛЬНОГО ЗАДАНИЯ")

    def add_image_item(img_rel_path: str, caption_text: str, width_in: float = 5.6):
        img_full = os.path.join(r"d:\MMO", img_rel_path)
        if os.path.exists(img_full):
            p_img = doc.add_paragraph()
            p_img.paragraph_format.first_line_indent = Mm(0)
            p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_full, width=Inches(width_in))
            add_figure_caption(caption_text)
        else:
            p_err = doc.add_paragraph(f"[Изображение не найдено: {img_rel_path}]")
            p_err.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_sec_h2("5.1 Результаты выполнения заданий Части 1")
    doc.add_paragraph(
        "На рисунке 5.1 представлен результат вычисления суммы нечетных цифр для контрольных чисел."
    )
    add_image_item("screenshots/p1_t1.png", "Рисунок 5.1 – Результат выполнения задания 1.1")

    doc.add_paragraph(
        "На рисунке 5.2 продемонстрирован результат подсчета пар соседних букв верхнего и нижнего регистров, "
        "а также согласных букв для слова 'HjkLM' и других тестовых строк."
    )
    add_image_item("screenshots/p1_t2.png", "Рисунок 5.2 – Результат выполнения задания 1.2")

    doc.add_paragraph(
        "На рисунке 5.3 приведен результат обработки списка: замена нечетных чисел на 1, вычисление суммы цифр "
        "четных чисел и подсчет гласных и согласных букв в словах."
    )
    add_image_item("screenshots/p1_t3.png", "Рисунок 5.3 – Результат выполнения задания 1.3")

    doc.add_paragraph(
        "На рисунке 5.4 продемонстрирована сортировка словаря по значениям в порядке возрастания и убывания."
    )
    add_image_item("screenshots/p1_t4.png", "Рисунок 5.4 – Результат выполнения задания 1.4")

    doc.add_paragraph(
        "На рисунках 5.5 и 5.6 отображена работа программы «Кондитерская»: просмотр полного ассортимента "
        "продукции (рисунок 5.5) и процесс покупки с вычислением стоимости чека и выводом остатков (рисунок 5.6)."
    )
    add_image_item("screenshots/p1_t5_catalog.png", "Рисунок 5.5 – Каталог продукции программы «Кондитерская»", width_in=5.6)
    add_image_item("screenshots/p1_t5_purchase.png", "Рисунок 5.6 – Оформление покупки и итоговый чек", width_in=5.6)

    doc.add_paragraph(
        "На рисунке 5.7 показана сортировка кортежа целых чисел по убыванию и вывод его первого и последнего элементов."
    )
    add_image_item("screenshots/p1_t6.png", "Рисунок 5.7 – Результат выполнения задания 1.6")

    add_sec_h2("5.2 Результаты выполнения заданий Части 2")
    doc.add_paragraph(
        "На рисунке 5.8 представлено тестирование функции is_password_good на различных наборах паролей "
        "с фиксацией результатов в обязательном блоке finally."
    )
    add_image_item("screenshots/p2_t1.png", "Рисунок 5.8 – Тестирование функции is_password_good")

    doc.add_paragraph(
        "На рисунке 5.9 приведен результат работы универсальной функции обработки кортежа, списка, чисел и строки "
        "с перехватом неподдерживаемого типа в блоке try...except."
    )
    add_image_item("screenshots/p2_t2.png", "Рисунок 5.9 – Обработка различных типов данных")

    doc.add_paragraph(
        "На рисунке 5.10 показана работа функции перестановки столбцов матрицы и перехват ошибки выхода индекса за пределы диапазона."
    )
    add_image_item("screenshots/p2_t3.png", "Рисунок 5.10 – Перестановка столбцов двумерного массива")

    doc.add_paragraph(
        "На рисунке 5.11 продемонстрирована работа конструкции try / except / else / finally при делении чисел, "
        "вызове пользовательского исключения и попытке открытия файла."
    )
    add_image_item("screenshots/p2_t4.png", "Рисунок 5.11 – Демонстрация работы try / except / else / finally")

    add_sec_h2("5.3 Результаты выполнения заданий Части 3")
    doc.add_paragraph(
        "На рисунке 5.12 отображена работа разработанного класса CustomList (добавление, удаление, реверс, сортировка, "
        "min/max, уникальные элементы, фильтрация, подсчет частот)."
    )
    add_image_item("screenshots/p3_t1.png", "Рисунок 5.12 – Работа с классом CustomList")

    doc.add_paragraph(
        "На рисунке 5.13 представлен расчет времени и стоимости поездок для классов Самолёт, Поезд, Автомобиль по различным маршрутам, "
        "автоматический выбор быстрейшей и экономичной поездки и сохранение отчета в файл."
    )
    add_image_item("screenshots/p3_t2.png", "Рисунок 5.13 – Иерархия классов транспортных средств")

    doc.add_paragraph(
        "На рисунке 5.14 приведен результат работы системы библиотеки: добавление, изменение названия, удаление книг, "
        "проверка свойств и экспорт каталога в текстовый файл."
    )
    add_image_item("screenshots/p3_t3.png", "Рисунок 5.14 – Система управления библиотекой")

    doc.add_paragraph(
        "На рисунке 5.15 показана работа класса StudentAccount с методами экземпляра, методами класса "
        "(@classmethod from_string, get_honor_students) и статическими методами-утилитами (@staticmethod validate_student_id, convert_grade_to_ects)."
    )
    add_image_item("screenshots/p3_t4.png", "Рисунок 5.15 – Методы экземпляра, класса и статические методы")

    # =========================================================================
    # 6 ВЫВОДЫ (цельный связанный текст без 1, 2, 3)
    # =========================================================================
    add_sec_h1("6 ВЫВОДЫ")

    doc.add_paragraph(
        "В ходе выполнения комплексной лабораторной работы по дисциплине «Методы машинного обучения» "
        "были всесторонне изучены и практически закреплены ключевые аспекты программирования на языке Python. "
        "При выполнении начального раздела работы были освоены базовые типы данных, арифметические операции "
        "и конструкции управления потоком выполнения. Разработаны алгоритмы нахождения суммы нечетных цифр "
        "натурального числа, контекстного анализа регистра смежных символов и подсчета согласных букв. "
        "Были изучены операции над гетерогенными динамическими списками, сортировка словарей по значению "
        "в прямом и обратном порядке, а также сортировка неизменяемых кортежей с извлечением экстремальных "
        "значений. Спроектированная интерактивная программа управления ассортиментом кондитерской наглядно "
        "продемонстрировала эффективное применение словарей со сложной структурой значений для хранения "
        "характеристик продукции, обработки пользовательских заказов и пересчета складских остатков."
    )

    doc.add_paragraph(
        "Второй этап исследований позволил освоить принципы модульной декомпозиции алгоритмов "
        "и построения отказоустойчивого программного обеспечения. Реализованная функция валидации паролей "
        "обеспечила надежную проверку критериев безопасности с протоколированием статуса завершения в блоке finally. "
        "Разработанный универсальный обработчик структур данных продемонстрировал корректное ветвление "
        "логики в зависимости от динамического типа входного аргумента, включая вычисление длины строк кортежа, "
        "суммирование элементов списка после первого отрицательного значения с удалением дубликатов, "
        "подсчет четных разрядов чисел и парсинг числовых подстрок. Алгоритм поэлементного обмена столбцов матрицы "
        "подтвердил практические навыки манипуляции двумерными массивами. На примере комплексного сценария "
        "было доказано преимущество конструкции try / except / else / finally, которая гарантирует "
        "корректное освобождение файловых дескрипторов и перехват исключений времени выполнения."
    )

    doc.add_paragraph(
        "Заключительный этап работы был посвящен практической реализации принципов объектно-ориентированного "
        "программирования. Спроектированный класс CustomList предоставил расширенный интерфейс для управления "
        "списковыми структурами, включая фильтрацию, частотный анализ и поиск экстремумов. Построенная иерархия "
        "классов транспортных средств на базе общего суперкласса обеспечила гибкий полиморфный расчет параметров "
        "перевозки по заданным маршрутам, автоматический выбор оптимального по времени и стоимости варианта "
        "с экспортом результатов во внешний файл. В информационной системе библиотеки была продемонстрирована "
        "строгая инкапсуляция атрибутов с помощью декораторов @property и сеттеров с валидацией данных. "
        "Разработанный класс студенческого аккаунта наглядно продемонстрировал четкое функциональное "
        "разграничение методов экземпляра, методов класса с фабричным созданием объектов и независимых "
        "статических методов-утилит. Все разработанные программы успешно протестированы, а структура отчета "
        "полностью соответствует требованиям стандарта СТП 01-2017."
    )

    out_docx = r"d:\MMO\report\Отчет_ЛР01_Власовец_Вариант7.docx"
    doc.save(out_docx)
    print(f"Отчет DOCX успешно сгенерирован: {out_docx}")
    return out_docx


if __name__ == "__main__":
    create_report()
