"""
Скрипт для сборки финального архива LR03_Vlasovets_Variant7.zip со всеми требуемыми материалами:
1. LR03_Gradient_Descent.ipynb (Jupyter Notebook с BGD, SGD, L2-регуляризацией, кодом, Markdown и графиками)
2. Отчет_ЛР03_Власовец_Вариант7.pdf (Итоговый отчет по стандарту БГУИР СТП 01-2017)
3. report/Отчет_ЛР03_Власовец_Вариант7.docx (Отредактированный отчет в формате Word)
4. latex/ (Исходники для Overleaf: main.tex, plots/, README_OVERLEAF.txt)
5. plots/ (7 высококачественных графиков в 300 DPI)
6. data/ (Исходный и масштабированный синтетический датасет регрессии)
7. LAB03_EXPLANATION.md (Полное руководство с формулами, кодом, вопросами защиты и ответами)
8. gd_summary.json (Контрольные численные метрики)
9. Исходные Python-скрипты автоматизации конвейера
"""

import os
import zipfile

def create_archive():
    base_dir = r"d:\MMO\lab3"
    zip_path = os.path.join(base_dir, "LR03_Vlasovets_Variant7.zip")

    # Корневые файлы
    items_to_zip = [
        "LR03_Gradient_Descent.ipynb",
        "Отчет_ЛР03_Власовец_Вариант7.pdf",
        "LAB03_EXPLANATION.md",
        "gd_summary.json",
        "generate_lab3_pipeline.py",
        "build_jupyter_notebook.py",
        "generate_report.py",
        "build_latex_report.py"
    ]

    folders_to_zip = [
        "plots",
        "latex",
        "report",
        "data"
    ]

    print("=" * 70)
    print("ФОРМИРОВАНИЕ ФИНАЛЬНОГО АРХИВА ЛАБОРАТОРНОЙ РАБОТЫ №3 (ВАРИАНТ 7)")
    print("=" * 70)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items_to_zip:
            abs_p = os.path.join(base_dir, item)
            if os.path.exists(abs_p):
                zf.write(abs_p, arcname=item)
                print(f"Добавлен файл: {item}")
            else:
                print(f"ВНИМАНИЕ: файл не найден: {abs_p}")

        for folder in folders_to_zip:
            folder_abs = os.path.join(base_dir, folder)
            for root, dirs, files in os.walk(folder_abs):
                for f in files:
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
