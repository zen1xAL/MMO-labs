"""
Скрипт для сборки финального архива LR04_Vlasovets_Variant7.zip со всеми требуемыми материалами:
1. LR04_Classification.ipynb (Jupyter Notebook с EDA, Logistic Regression, Linear SVM, RBF SVM, CART, ROC/PR кривыми и скорингом)
2. Отчет_ЛР04_Власовец_Вариант7.pdf (Итоговый отчет по стандарту БГУИР СТП 01-2017)
3. report/Отчет_ЛР04_Власовец_Вариант7.docx (Официальный отчет в формате Word)
4. latex/ (Исходники для Overleaf: main.tex, plots/, README_OVERLEAF.txt)
5. plots/ (9 высококачественных графиков в 300 DPI)
6. data/ (Исходный Bankloan_raw.csv, очищенный Bankloan_clean.csv, train/test выборки, скоринговый файл)
7. LAB04_EXPLANATION.md (Архитектурное методическое руководство)
8. LAB4_DEFENSE_GUIDE.md (Полное руководство по защите с формулами, разборами и ответами на 15 вопросов)
9. classification_summary.json (Контрольные численные метрики)
10. Исходные Python-скрипты автоматизации конвейера
"""

import os
import zipfile

def create_archive():
    base_dir = r"d:\MMO\lab4"
    zip_path = os.path.join(base_dir, "LR04_Vlasovets_Variant7.zip")

    # Корневые файлы
    items_to_zip = [
        "LR04_Classification.ipynb",
        "Отчет_ЛР04_Власовец_Вариант7.pdf",
        "LAB04_EXPLANATION.md",
        "LAB4_DEFENSE_GUIDE.md",
        "classification_summary.json",
        "generate_lab4_pipeline.py",
        "build_jupyter_notebook.py",
        "generate_report.py",
        "build_latex_report.py",
        "convert_to_pdf.ps1"
    ]

    folders_to_zip = [
        "plots",
        "latex",
        "report",
        "data"
    ]

    print("=" * 70)
    print("ФОРМИРОВАНИЕ ФИНАЛЬНОГО АРХИВА ЛАБОРАТОРНОЙ РАБОТЫ №4 (ВАРИАНТ 7)")
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
