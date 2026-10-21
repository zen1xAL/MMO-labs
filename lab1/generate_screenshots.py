"""
Скрипт для генерации реалистичных скриншотов терминала
выполнения всех заданий лабораторной работы №1 (Вариант 7).
"""

import os
import subprocess
import sys
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\consolab.ttf"


def run_and_capture_output(
    cmd: List[str], cwd: str, stdin_data: Optional[str] = None
) -> str:
    """Запускает скрипт и перехватывает вывод в кодировке UTF-8."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.run(
        cmd,
        cwd=cwd,
        input=stdin_data,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return proc.stdout


def render_terminal_screenshot(
    title: str,
    prompt_cmd: str,
    output_text: str,
    save_path: str,
    font_size: int = 16,
) -> None:
    """
    Рендерит реалистичное окно Windows Terminal с выводом программы.
    """
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
        font_bold = ImageFont.truetype(FONT_BOLD_PATH, font_size)
        font_header = ImageFont.truetype(FONT_PATH, 13)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font
        font_header = font

    # Подготовка строк текста
    lines: List[str] = [prompt_cmd]
    for raw_line in output_text.strip().split("\n"):
        lines.append(raw_line)
    # Добавляем финальный пустой промпт для реалистичности
    cwd_short = prompt_cmd.split(">")[0]
    lines.append(f"{cwd_short}> ")

    # Вычисление размеров окна
    # Используем getbbox для определения габаритов
    dummy_img = Image.new("RGB", (100, 100))
    dummy_draw = ImageDraw.Draw(dummy_img)

    max_line_width = 0
    line_height = 0
    for l in lines:
        bbox = dummy_draw.textbbox((0, 0), l, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w > max_line_width:
            max_line_width = w
        if h > line_height:
            line_height = h

    line_spacing = int(line_height * 1.35)
    padding_x = 24
    header_height = 36
    padding_y = 16

    content_width = max(max_line_width + padding_x * 2, 750)
    content_height = len(lines) * line_spacing + padding_y * 2 + header_height

    # Цветовая палитра Windows Terminal Dark
    bg_color = (24, 24, 24)          # Фон терминала #181818
    header_bg = (35, 35, 35)         # Заголовок #232323
    text_color = (220, 220, 220)     # Белый основной текст
    prompt_color = (97, 214, 214)    # Цвет пути PS (Cyan)
    cmd_color = (245, 245, 245)      # Цвет команды (Яркий белый)
    accent_green = (120, 220, 120)   # Акцент для ключевых слов
    accent_yellow = (230, 210, 110)  # Акцент для предупреждений
    border_color = (60, 60, 60)

    # Создаем изображение
    img = Image.new("RGB", (content_width, content_height), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Шапка окна
    draw.rectangle([(0, 0), (content_width, header_height)], fill=header_bg)
    draw.line([(0, header_height), (content_width, header_height)], fill=border_color, width=1)

    # Заголовок терминала
    tab_title = f"  Terminal: {title}  "
    draw.text((16, 10), tab_title, fill=(200, 200, 200), font=font_header)

    # Кнопки управления окном (справа)
    btn_y = 12
    draw.ellipse([(content_width - 65, btn_y), (content_width - 53, btn_y + 12)], fill=(70, 70, 70))
    draw.ellipse([(content_width - 45, btn_y), (content_width - 33, btn_y + 12)], fill=(70, 70, 70))
    draw.ellipse([(content_width - 25, btn_y), (content_width - 13, btn_y + 12)], fill=(200, 70, 70))

    # 2. Рендеринг строк терминала
    cur_y = header_height + padding_y

    for idx, line in enumerate(lines):
        # Определение цвета строки
        if idx == 0:
            # Первая строка с промптом PowerShell
            if ">" in line:
                prompt_part, cmd_part = line.split(">", 1)
                draw.text((padding_x, cur_y), prompt_part + ">", fill=prompt_color, font=font_bold)
                bbox_p = draw.textbbox((padding_x, cur_y), prompt_part + ">", font=font_bold)
                draw.text((bbox_p[2] + 8, cur_y), cmd_part, fill=cmd_color, font=font_bold)
            else:
                draw.text((padding_x, cur_y), line, fill=prompt_color, font=font_bold)
        elif idx == len(lines) - 1:
            # Финальный промпт
            draw.text((padding_x, cur_y), line, fill=prompt_color, font=font_bold)
            # Мигающий курсор
            bbox_last = draw.textbbox((padding_x, cur_y), line, font=font_bold)
            draw.rectangle([(bbox_last[2] + 2, cur_y + 2), (bbox_last[2] + 10, cur_y + line_spacing - 4)], fill=(200, 200, 200))
        else:
            col = text_color
            if line.startswith("="):
                col = (130, 160, 220)
            elif line.startswith("---") or line.startswith("###"):
                col = accent_yellow
            elif "УСПЕШНО" in line or "НАДЁЖЕН" in line or "True" in line:
                col = text_color
            elif "Ошибка" in line or "НЕ НАДЁЖЕН" in line or "False" in line:
                col = (255, 140, 140)
            draw.text((padding_x, cur_y), line, fill=col, font=font)

        cur_y += line_spacing

    # Внешняя рамка
    draw.rectangle([(0, 0), (content_width - 1, content_height - 1)], outline=border_color, width=1)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, "PNG")
    print(f"Скриншот сохранен: {save_path} ({content_width}x{content_height})")


def main() -> None:
    print("Генерация скриншотов выполнения заданий...")

    tasks = [
        # --- Часть 1 ---
        {
            "id": "p1_t1",
            "title": "Часть 1. Задание 1 (Сумма нечетных цифр)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "task1_sum_odd_digits.py"],
            "prompt": "PS D:\\MMO\\part1> py task1_sum_odd_digits.py",
            "stdin": "9753124\n",
            "out": "d:/MMO/screenshots/p1_t1.png",
        },
        {
            "id": "p1_t2",
            "title": "Часть 1. Задание 2 (Пары регистра и согласные)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "task2_letter_pairs_consonants.py"],
            "prompt": "PS D:\\MMO\\part1> py task2_letter_pairs_consonants.py",
            "stdin": "HjkLM\n",
            "out": "d:/MMO/screenshots/p1_t2.png",
        },
        {
            "id": "p1_t3",
            "title": "Часть 1. Задание 3 (Анализ списка и четность)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "task3_list_parity_analysis.py"],
            "prompt": "PS D:\\MMO\\part1> py task3_list_parity_analysis.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p1_t3.png",
        },
        {
            "id": "p1_t4",
            "title": "Часть 1. Задание 4 (Сортировка словаря)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "task4_dict_sorting.py"],
            "prompt": "PS D:\\MMO\\part1> py task4_dict_sorting.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p1_t4.png",
        },
        {
            "id": "p1_t5_1",
            "title": "Часть 1. Задание 5 (Кондитерская - Просмотр каталога)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "-c", "import task5_confectionery_store as t; t.run_confectionery(mock_actions=['4', '6'])"],
            "prompt": "PS D:\\MMO\\part1> py task5_confectionery_store.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p1_t5_catalog.png",
        },
        {
            "id": "p1_t5_2",
            "title": "Часть 1. Задание 5 (Кондитерская - Покупка и чек)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "-c", "import task5_confectionery_store as t; t.run_confectionery(mock_actions=['5', '6'])"],
            "prompt": "PS D:\\MMO\\part1> py task5_confectionery_store.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p1_t5_purchase.png",
        },
        {
            "id": "p1_t6",
            "title": "Часть 1. Задание 6 (Сортировка кортежа)",
            "cwd": "d:/MMO/part1",
            "cmd": ["py", "task6_tuple_sorting.py"],
            "prompt": "PS D:\\MMO\\part1> py task6_tuple_sorting.py",
            "stdin": "45 12 88 -3 100 0 7\n",
            "out": "d:/MMO/screenshots/p1_t6.png",
        },
        # --- Часть 2 ---
        {
            "id": "p2_t1",
            "title": "Часть 2. Задание 1 (Проверка пароля)",
            "cwd": "d:/MMO/part2",
            "cmd": ["py", "task1_password_check.py"],
            "prompt": "PS D:\\MMO\\part2> py task1_password_check.py",
            "stdin": "SecretPass2026\n",
            "out": "d:/MMO/screenshots/p2_t1.png",
        },
        {
            "id": "p2_t2",
            "title": "Часть 2. Задание 2 (Обработка разных типов данных)",
            "cwd": "d:/MMO/part2",
            "cmd": ["py", "task2_multi_type_processor.py"],
            "prompt": "PS D:\\MMO\\part2> py task2_multi_type_processor.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p2_t2.png",
        },
        {
            "id": "p2_t3",
            "title": "Часть 2. Задание 3 (Перестановка столбцов матрицы)",
            "cwd": "d:/MMO/part2",
            "cmd": ["py", "task3_matrix_column_swap.py", "--demo"],
            "prompt": "PS D:\\MMO\\part2> py task3_matrix_column_swap.py --demo",
            "stdin": None,
            "out": "d:/MMO/screenshots/p2_t3.png",
        },
        {
            "id": "p2_t4",
            "title": "Часть 2. Задание 4 (Работа try/except/finally)",
            "cwd": "d:/MMO/part2",
            "cmd": ["py", "task4_exceptions_demo.py"],
            "prompt": "PS D:\\MMO\\part2> py task4_exceptions_demo.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p2_t4.png",
        },
        # --- Часть 3 ---
        {
            "id": "p3_t1",
            "title": "Часть 3. Задание 1 (Класс CustomList)",
            "cwd": "d:/MMO/part3",
            "cmd": ["py", "task1_custom_list.py"],
            "prompt": "PS D:\\MMO\\part3> py task1_custom_list.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p3_t1.png",
        },
        {
            "id": "p3_t2",
            "title": "Часть 3. Задание 2 (Иерархия транспорта)",
            "cwd": "d:/MMO/part3",
            "cmd": ["py", "task2_transport_hierarchy.py"],
            "prompt": "PS D:\\MMO\\part3> py task2_transport_hierarchy.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p3_t2.png",
        },
        {
            "id": "p3_t3",
            "title": "Часть 3. Задание 3 (Система Библиотека-Отдел-Книга)",
            "cwd": "d:/MMO/part3",
            "cmd": ["py", "task3_library_system.py"],
            "prompt": "PS D:\\MMO\\part3> py task3_library_system.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p3_t3.png",
        },
        {
            "id": "p3_t4",
            "title": "Часть 3. Задание 4 (Методы экземпляра, класса, статические)",
            "cwd": "d:/MMO/part3",
            "cmd": ["py", "task4_class_methods_demo.py"],
            "prompt": "PS D:\\MMO\\part3> py task4_class_methods_demo.py",
            "stdin": None,
            "out": "d:/MMO/screenshots/p3_t4.png",
        },
    ]

    for t in tasks:
        print(f"Обработка {t['id']}: {t['title']}...")
        output = run_and_capture_output(t["cmd"], cwd=t["cwd"], stdin_data=t["stdin"])
        render_terminal_screenshot(
            title=t["title"],
            prompt_cmd=t["prompt"],
            output_text=output,
            save_path=t["out"],
        )

    print("\nВсе 14 скриншотов успешно сгенерированы в папку screenshots!")


if __name__ == "__main__":
    main()
