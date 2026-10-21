"""
Скрипт для сборки финального архива LR02_Vlasovets.zip со всеми требуемыми материалами:
1. LR02_EDA_StudentPerformance.ipynb (Jupyter Notebook с EDA, кодом, Markdown и сохраненными графиками)
2. Отчет_ЛР02_Власовец.pdf (Итоговый отчет по стандарту БГУИР СТП 01-2017)
3. report/Отчет_ЛР02_Власовец.docx (Отредактированный отчет в формате Word)
4. latex/ (Исходники для Overleaf: main.tex, plots/, README_OVERLEAF.txt)
5. plots/ (9 высококачественных графиков в 300 DPI)
6. LAB02_EXPLANATION.md (Полное руководство с формулами, кодом и примерами)
7. StudentPerformance_Preprocessed.csv (Итоговый очищенный и масштабированный датасет)
8. Исходные Python-скрипты автоматизации конвейера
"""

import os
import zipfile

def create_archive():
    base_dir = r"d:\MMO\lab2"
    zip_path = os.path.join(base_dir, "LR02_Vlasovets.zip")

    # Корневые файлы
    items_to_zip = [
        "LR02_EDA_StudentPerformance.ipynb",
        "Отчет_ЛР02_Власовец.pdf",
        "LAB02_EXPLANATION.md",
        "StudentPerformance_Preprocessed.csv",
        "eda_summary.json",
        "generate_eda_pipeline.py",
        "build_jupyter_notebook.py",
        "generate_report.py",
        "build_latex_report.py"
    ]

    folders_to_zip = [
        "plots",
        "latex",
        "report",
        "StudentPerformanceFactors"
    ]

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
