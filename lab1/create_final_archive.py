"""
Скрипт для сборки финального архива LR01_Vlasovets_Variant7.zip со всеми требуемыми материалами:
1. LR01_Variant7.ipynb (Jupyter Notebook со всеми 14 заданиями и сохраненными выполненными ячейками)
2. Отчет_ЛР01_Власовец_Вариант7.pdf (Итоговый отчет по СТП 01-2017)
3. latex/ (Исходники для Overleaf: main.tex, скриншоты, инструкция README_OVERLEAF.txt)
4. part1/, part2/, part3/ (Исходные скрипты Python для всех 14 заданий)
5. screenshots/ (15 консольных снимков терминала выполнения)
"""

import os
import zipfile

def create_archive():
    base_dir = r"d:\MMO"
    zip_path = os.path.join(base_dir, "LR01_Vlasovets_Variant7.zip")
    
    # Копируем PDF в корень d:\MMO для удобства доступа
    pdf_src = os.path.join(base_dir, "report", "Отчет_ЛР01_Власовец_Вариант7.pdf")
    pdf_root = os.path.join(base_dir, "Отчет_ЛР01_Власовец_Вариант7.pdf")
    if os.path.exists(pdf_src):
        with open(pdf_src, "rb") as fsrc, open(pdf_root, "wb") as fdst:
            fdst.write(fsrc.read())
        print(f"Скопирован PDF: {pdf_root}")

    # Список файлов и папок для добавления в архив
    items_to_zip = [
        ("LR01_Variant7.ipynb", "LR01_Variant7.ipynb"),
        ("Отчет_ЛР01_Власовец_Вариант7.pdf", "Отчет_ЛР01_Власовец_Вариант7.pdf"),
        ("Отчет_ЛР01_Власовец_Вариант7.pdf", "Report_LR01_Vlasovets_Variant7.pdf"),
    ]

    folders_to_zip = [
        "latex",
        "part1",
        "part2",
        "part3",
        "screenshots"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Добавляем корневые файлы
        for local_rel, arc_name in items_to_zip:
            abs_p = os.path.join(base_dir, local_rel)
            if os.path.exists(abs_p):
                zf.write(abs_p, arcname=arc_name)
                print(f"Добавлен файл: {arc_name}")
            else:
                print(f"ВНИМАНИЕ: файл не найден: {abs_p}")

        # Добавляем папки рекурсивно
        for folder in folders_to_zip:
            folder_abs = os.path.join(base_dir, folder)
            for root, dirs, files in os.walk(folder_abs):
                for f in files:
                    # Исключаем временные файлы или pycache
                    if f.endswith((".pyc", ".tmp", ".log")) or "__pycache__" in root:
                        continue
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, base_dir)
                    zf.write(full_p, arcname=rel_p)
            print(f"Добавлена папка: {folder}")

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\nАрхив успешно создан: {zip_path} ({zip_size_mb:.2f} МБ)")

if __name__ == "__main__":
    create_archive()
