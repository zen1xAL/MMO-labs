"""
Генератор официального отчета по Лабораторной работе №3 по курсу «Методы машинного обучения».
Тема: «Градиентный спуск, стохастический градиентный спуск и регуляризация».
Студент: гр. 351002 Власовец А. И. (Вариант 7 - нечетный: L2-регуляризация).
Преподаватель: Лебедевич А. В.
Оформление строго соответствует стандарту БГУИР СТП 01-2017.
"""

import os
import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"d:\MMO\lab3"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORT_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORT_DIR, exist_ok=True)
DOCX_PATH = os.path.join(REPORT_DIR, "Отчет_ЛР03_Власовец_Вариант7.docx")

def add_code_block(doc, code_text: str):
    """Добавляет код моноширинным шрифтом Courier New 9.0 пт без рамок по стандарту БГУИР."""
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

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.first_line_indent = Mm(0)
    p_sp.paragraph_format.line_spacing = 1.0
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

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

    # 1. Настройка полей страницы А4 (Приложение Л)
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)

    section.different_first_page_header_footer = True
    add_page_number_to_footer(section.footer)

    # 2. Стиль основного текста по СТП 01-2017
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

    for _ in range(5):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    p_title = doc.add_paragraph()
    p_title.paragraph_format.first_line_indent = Mm(0)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.3

    r1 = p_title.add_run("ОТЧЕТ\nПО ЛАБОРАТОРНОЙ РАБОТЕ № 3\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(16)
    r1.font.bold = False

    r2 = p_title.add_run(
        "по дисциплине «Методы машинного обучения»\n\n"
        "Тема: «Градиентный спуск, стохастический градиентный спуск\n"
        "и регуляризация»\n"
        "Вариант № 7 (L2-регуляризация)"
    )
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = False

    for _ in range(5):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    # Таблица для подписей (2 колонки)
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

    for _ in range(5):
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

    doc.add_page_break()

    # Функции добавления заголовков и рисунков
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

    def add_figure(img_filename: str, caption_text: str, width_inches: float = 6.2):
        img_path = os.path.join(PLOTS_DIR, img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.paragraph_format.first_line_indent = Mm(0)
            p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(width_inches))

            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.first_line_indent = Mm(0)
            p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(caption_text)
            run_cap.font.name = "Times New Roman"
            run_cap.font.size = Pt(13)
            run_cap.font.italic = False

    # =========================================================================
    # 1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ (цельный связный текст)
    # =========================================================================
    add_sec_h1("1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ")
    doc.add_paragraph(
        "Целью выполнения лабораторной работы является глубокое изучение теоретических основ и практическое "
        "освоение базовых численных методов безусловной оптимизации первого порядка в машинном обучении. "
        "В процессе выполнения работы решаются задачи самостоятельной алгоритмической реализации классического "
        "пакетного градиентного спуска (Batch Gradient Descent, BGD) и стохастического градиентного спуска "
        "(Stochastic Gradient Descent, SGD) для обучения модели линейной регрессии, экспериментального исследования "
        "динамики сходимости при варьировании темпа обучения, сравнительного анализа детерминированного и стохастического "
        "подходов на едином графике потерь, а также программной реализации L2-регуляризации (Ridge Regression) "
        "для индивидуального нечетного варианта № 7 с построением регуляризационных путей для 20 коэффициентов "
        "штрафа в широком диапазоне масштабов."
    )

    # =========================================================================
    # 2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ
    # =========================================================================
    add_sec_h1("2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ")
    doc.add_paragraph(
        "Линейная регрессия моделирует функциональную зависимость скалярного целевого признака y от вектора "
        "входных характеристик x посредством линейной комбинации с весовыми коэффициентами w. "
        "С учетом фиктивного единичного признака x0 = 1 для свободного члена (bias) модель принимает матричный вид: "
        "y_hat = X * w. Обучение модели сводится к поиску вектора параметров w, минимизирующего эмпирический "
        "риск — среднеквадратичную ошибку (Mean Squared Error, MSE):"
    )
    doc.add_paragraph(
        "Q(w, X) = (1 / l) * ||X * w - y||^2 = (1 / l) * sum_{i=1}^l (x_i^T * w - y_i)^2."
    )
    doc.add_paragraph(
        "Вектор антиградиента квадратичной функции потерь определяет направление наискорейшего локального убывания ошибки: "
        "grad Q(w, X) = (2 / l) * X^T * (X * w - y). Метод пакетного градиентного спуска осуществляет шаги по правилу: "
        "w^k = w^(k-1) - eta_k * grad Q(w^(k-1), X). Итерационный процесс завершается при выполнении условия малости изменения "
        "параметров: ||w^k - w^(k-1)|| < epsilon, где ||.|| обозначает евклидову норму разности векторов, либо при исчерпании "
        "лимита итераций K_max."
    )
    doc.add_paragraph(
        "В отличие от BGD, требующего вычисления градиента по всем l обучающим объектам, стохастический градиентный спуск "
        "на каждой итерации случайным образом выбирает один объект i in {1, ..., l} и рассчитывает несмещенную оценку градиента: "
        "grad Q_i(w, x_i) = 2 * (x_i^T * w - y_i) * x_i. Вычислительная сложность одной итерации снижается с O(l * d) до O(d). "
        "Для гарантии сходимости к точке минимума скорость обучения стохастического спуска должна монотонно убывать "
        "в соответствии с условиями Роббинса–Монро: sum eta_k = infty, sum eta_k^2 < infty."
    )
    doc.add_paragraph(
        "Регуляризация предназначена для предотвращения переобучения модели и борьбы с мультиколлинеарностью признаков. "
        "При L2-регуляризации (Ridge регрессия) к функционалу ошибки добавляется квадратичный штраф: "
        "Q_L2(w) = (1 / l) * ||X * w - y||^2 + lambda * ||w_{1:d}||^2. Градиент L2-штрафа пропорционален весам, "
        "что приводит к плавному и равномерному стягиванию (shrinkage) коэффициентов к нулю при росте lambda без их строгого зануления."
    )

    # =========================================================================
    # 3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ
    # =========================================================================
    add_sec_h1("3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ")
    doc.add_paragraph(
        "В соответствии с заданием сгенерирован синтетический набор данных с помощью генератора "
        "sklearn.datasets.make_regression. Выборка содержит 1000 наблюдений, 2 независимых признака (Feature_1 и Feature_2), "
        "а также аддитивный нормально распределенный шум со стандартным отклонением sigma = 10.0 (дисперсия шума sigma^2 = 100). "
        "Число искомых параметров модели составляет 3 (с учетом свободного члена w0). Все признаки предварительно стандартизированы "
        "(среднее mu = 0, дисперсия sigma^2 = 1)."
    )

    table_data = doc.add_table(rows=1, cols=4)
    table_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cells = table_data.rows[0].cells
    h_cells[0].text = "Признак"
    h_cells[1].text = "Тип шкалы"
    h_cells[2].text = "Параметры распределения"
    h_cells[3].text = "Истинный вес w*"
    for c in h_cells:
        for p in c.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(11)

    meta_rows = [
        ("x0 (Intercept / Bias)", "Константа 1.0", "Фиктивный признак сдвига", "w0 = 1.7660"),
        ("Feature_1 (x1)", "Непрерывный z-score", "mu = 0.00, sigma = 1.00", "w1 = 39.4725"),
        ("Feature_2 (x2)", "Непрерывный z-score", "mu = 0.00, sigma = 1.00", "w2 = 6.8970"),
        ("Target_y (y)", "Непрерывный отклик", "mu = 1.77, sigma = 40.85", "—")
    ]
    for row in meta_rows:
        r_cells = table_data.add_row().cells
        for idx, val in enumerate(row):
            r_cells[idx].text = val
            for p in r_cells[idx].paragraphs:
                p.runs[0].font.size = Pt(10)

    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.first_line_indent = Mm(0)
    p_tbl.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tbl = p_tbl.add_run("Таблица 3.1 – Параметры синтезированного набора данных")
    r_tbl.font.name = "Times New Roman"
    r_tbl.font.size = Pt(12)
    r_tbl.font.italic = True

    add_figure("01_dataset_regression_structure.png", "Рисунок 3.1 – Структура и распределение признаков синтетического регрессионного датасета")

    # =========================================================================
    # 4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ
    # =========================================================================
    add_sec_h1("4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ")

    add_sec_h2("4.1 Реализация и сходимость пакетного градиентного спуска (BGD)")
    doc.add_paragraph(
        "Разработан алгоритм пакетного градиентного спуска с контролем евклидовой нормы изменения параметров на каждом шаге. "
        "В качестве критерия останова задан порог epsilon = 10^-5. При базовом темпе обучения eta = 0.05 алгоритм успешно "
        "сошелся за 124 итерации, достигнув значения MSE = 96.85, что полностью соответствует теоретической дисперсии шума "
        "генератора (sigma^2 = 100). Итоговый вектор весов составил w = [1.7660, 39.4724, 6.8970], совпав с точным решением МНК "
        "с погрешностью порядка 8.4 * 10^-5."
    )

    add_figure("02_bgd_convergence_trajectory.png", "Рисунок 3.2 – Сходимость градиентного спуска (BGD), норма шага весов и траектория оптимизации")

    doc.add_paragraph("Ниже приведен листинг функции пакетного градиентного спуска:")
    code_bgd = (
        "def batch_gradient_descent(X, y, eta=0.05, eps=1e-5, max_iter=1000):\n"
        "    l, d = X.shape\n"
        "    w = np.zeros(d, dtype=float)\n"
        "    w_history = [w.copy()]\n"
        "    mse_history = [float(np.mean((X @ w - y) ** 2))]\n"
        "    diff_norms = []\n\n"
        "    for k in range(1, max_iter + 1):\n"
        "        # 1. Расчет градиента MSE\n"
        "        grad = (2.0 / l) * (X.T @ (X @ w - y))\n"
        "        # 2. Шаг обновления весов: w^k = w^(k-1) - eta * grad\n"
        "        w_new = w - eta * grad\n"
        "        diff_norm = float(np.linalg.norm(w_new - w))\n"
        "        diff_norms.append(diff_norm)\n\n"
        "        w = w_new\n"
        "        w_history.append(w.copy())\n"
        "        mse_history.append(float(np.mean((X @ w - y) ** 2)))\n\n"
        "        # 3. Завершить цикл, если ||w^k - w^(k-1)|| < eps\n"
        "        if diff_norm < eps:\n"
        "            break\n\n"
        "    return w, w_history, mse_history, diff_norms"
    )
    add_code_block(doc, code_bgd)

    add_sec_h2("4.2 Исследование влияния скорости обучения (Learning Rate)")
    doc.add_paragraph(
        "Проведено экспериментальное исследование динамики сходимости при пяти различных значениях скорости обучения eta in {0.001, 0.01, 0.05, 0.1, 0.5}. "
        "Результаты эксперимента сведены в Таблицу 4.1 и проиллюстрированы на Рисунке 3.3. При eta = 0.001 за 300 итераций алгоритм не успевает "
        "достичь окрестности минимума (MSE = 174.66). При увеличении шага до eta = 0.05 сходимость достигается за 124 шага, а при eta = 0.1 — всего за 60 шагов. "
        "При eta = 0.5 наблюдаются выраженные осцилляции вокруг траектории спуска."
    )

    table_lr = doc.add_table(rows=1, cols=4)
    table_lr.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_lr = table_lr.rows[0].cells
    h_lr[0].text = "Темп обучения (eta)"
    h_lr[1].text = "Итераций до сходимости"
    h_lr[2].text = "Финальное MSE"
    h_lr[3].text = "Характер сходимости"
    for c in h_lr:
        for p in c.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10)

    lr_data = [
        ("eta = 0.001", "300 (лимит)", "174.6599", "Сверхмедленное убывание ошибки"),
        ("eta = 0.010", "300 (лимит)", "97.0270", "Устойчивое, монотонное движение"),
        ("eta = 0.050", "124", "96.8544", "Оптимальная плавная сходимость"),
        ("eta = 0.100", "60", "96.8544", "Быстрая сходимость с минимальными затратами"),
        ("eta = 0.500", "20", "96.8544", "Пограничный режим с осцилляциями")
    ]
    for row in lr_data:
        r_cells = table_lr.add_row().cells
        for idx, val in enumerate(row):
            r_cells[idx].text = val
            for p in r_cells[idx].paragraphs:
                p.runs[0].font.size = Pt(9.5)

    p_tbl2 = doc.add_paragraph()
    p_tbl2.paragraph_format.first_line_indent = Mm(0)
    p_tbl2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tbl2 = p_tbl2.add_run("Таблица 4.1 – Зависимость характеристик сходимости от скорости обучения")
    r_tbl2.font.name = "Times New Roman"
    r_tbl2.font.size = Pt(12)
    r_tbl2.font.italic = True

    add_figure("03_learning_rate_experiments.png", "Рисунок 3.3 – Влияние скорости обучения на динамику сходимости градиентного спуска")

    add_sec_h2("4.3 Стохастический градиентный спуск (SGD) и его сопоставление с BGD")
    doc.add_paragraph(
        "В функцию оптимизации внедрен выбор случайного обучающего прецедента на каждой итерации. "
        "Для подавления флуктуаций применен график затухания темпа обучения eta_k = eta0 / (1 + 0.001 * k). "
        "На Рисунке 3.4 представлено сопоставление функций потерь BGD и SGD на одном графике. "
        "Пакетный спуск движется строго детерминированно и монотонно, требуя 1000 операций вычисления ошибки на каждый шаг. "
        "Стохастический спуск совершает стохастические колебания вокруг траектории антиградиента, однако достигает аналогичного "
        "качества (MSE = 100.52) при несоизмеримо меньших вычислительных затратах на одну итерацию."
    )

    add_figure("04_bgd_vs_sgd_comparison.png", "Рисунок 3.4 – Сравнительный анализ сходимости пакетного (BGD) и стохастического (SGD) спуска")

    doc.add_paragraph("Ниже приведен листинг функции стохастического градиентного спуска:")
    code_sgd = (
        "def stochastic_gradient_descent(X, y, eta0=0.015, max_iter=1500, seed=42):\n"
        "    np.random.seed(seed)\n"
        "    l, d = X.shape\n"
        "    w = np.zeros(d, dtype=float)\n"
        "    w_history, mse_history = [w.copy()], [float(np.mean((X @ w - y) ** 2))]\n\n"
        "    for k in range(1, max_iter + 1):\n"
        "        idx = np.random.randint(0, l) # выбор случайного объекта\n"
        "        xi, yi = X[idx], y[idx]\n"
        "        grad_i = 2.0 * (xi @ w - yi) * xi\n"
        "        eta_k = eta0 / (1.0 + 0.001 * k) # затухающий шаг\n"
        "        w = w - eta_k * grad_i\n"
        "        w_history.append(w.copy())\n"
        "        mse_history.append(float(np.mean((X @ w - y) ** 2)))\n\n"
        "    return w, w_history, mse_history"
    )
    add_code_block(doc, code_sgd)

    add_sec_h2("4.4 Исследование L2-регуляризации (Вариант 7)")
    doc.add_paragraph(
        "Для индивидуального нечетного варианта № 7 реализована L2-регуляризация (Ridge регрессия). "
        "В соответствии с заданием сформирована логарифмическая сетка из 20 коэффициентов регуляризации в диапазоне от 0.001 до 1000. "
        "На Рисунке 3.5 отображены регуляризационные пути параметров w. При увеличении коэффициента штрафа lambda от 0.001 до 1000 "
        "евклидова норма весов информативных признаков монотонно сжимается от 40.03 до 0.04 (эффект Ridge Shrinkage), "
        "в то время как свободный член w0 сохраняет стабильное значение 1.77, гарантируя центрированность прогнозов."
    )

    add_figure("05_l2_regularization_paths.png", "Рисунок 3.5 – Регуляризационные пути весов при L2-регуляризации (Ridge Regression) для 20 коэффициентов")

    doc.add_paragraph(
        "Для углубленного анализа на Рисунке 3.6 представлено сопоставление L2 (Ridge) и L1 (Lasso) регуляризаторов. "
        "В то время как L2 плавно уменьшает величину коэффициентов, сохраняя их строго ненулевыми, L1 регуляризация "
        "при lambda > 50 полностью зануляет веса (w1 = 0, w2 = 0), выполняя автоматический отбор признаков."
    )

    add_figure("06_l1_vs_l2_comparison.png", "Рисунок 3.6 – Сравнительный анализ поведения весов при L2 (Ridge) и L1 (Lasso) регуляризации")

    add_sec_h2("4.5 Верификация модели и сопоставление с эталоном МНК")
    doc.add_paragraph(
        "На Рисунке 3.7 приведены результаты проверки построенной линейной модели. Коэффициент детерминации составил R^2 = 0.9419, "
        "средняя абсолютная ошибка MAE = 7.96, корень из среднеквадратичной ошибки RMSE = 9.84. "
        "Гистограмма остатков e = y - y_hat симметрична и подчиняется нормальному закону с нулевым центром. "
        "Сравнение весовых коэффициентов показало строгое совпадение решения градиентного спуска с нормальным уравнением МНК "
        "и библиотечной моделью LinearRegression из пакета Scikit-Learn."
    )

    add_figure("07_model_evaluation_residuals.png", "Рисунок 3.7 – Верификация модели: сопоставление прогнозов, остатки регрессии и сравнение с МНК")

    # =========================================================================
    # 5 ВЫВОДЫ (цельный связный текст)
    # =========================================================================
    add_sec_h1("5 ВЫВОДЫ")
    doc.add_paragraph(
        "В ходе выполнения лабораторной работы были всесторонне исследованы математические принципы, особенности реализации "
        "и практические свойства градиентных методов оптимизации в задачах линейной регрессии. Самостоятельно разработанная функция "
        "пакетного градиентного спуска (BGD) подтвердила высокую точность сходимости: при пороге epsilon = 10^-5 алгоритм сошелся за 124 "
        "итерации к оптимальной точке с абсолютным евклидовым расхождением с решением нормального уравнения МНК менее 8.5 * 10^-5. "
        "Экспериментальное исследование скорости обучения доказало критическую важность подбора параметра eta: малые значения приводят к "
        "затягиванию процесса оптимизации, а чрезмерные вызывают неустойчивость процесса."
    )
    doc.add_paragraph(
        "Сравнительный анализ пакетного и стохастического градиентного спуска на совмещенном графике MSE наглядно продемонстрировал "
        "принципиальную разницу их вычислительной природы. BGD обеспечивает строго монотонное уменьшение функции потерь, однако требует "
        "полного прохода по выборке на каждом шаге. SGD вычисляет градиент по единичному случайному прецеденту, сокращая трудоемкость итерации "
        "в l раз, а возникающий стохастический шум эффективно стабилизируется за счет графика затухания темпа обучения."
    )
    doc.add_paragraph(
        "Исследование L2-регуляризации (Ridge Regression), выполненное для нечетного варианта № 7 на сетке из 20 коэффициентов lambda в "
        "диапазоне от 0.001 до 1000, полностью подтвердило теоретические положения о непрерывном сжатии параметров (shrinkage effect). "
        "Норма весов уменьшилась с 40.03 до 0.04 при сохранении несмещенного свободного члена w0 = 1.77. Сопоставление с L1-регуляризацией "
        "продемонстрировало фундаментальное различие: L1 зануляет параметры, формируя разреженную модель, тогда как L2 сохраняет все признаки, "
        "эффективно подавляя их дисперсию. Итоговый коэффициент детерминации R^2 = 0.9419 подтвердил адекватность и высокую точность построенной модели."
    )

    doc.save(DOCX_PATH)
    print(f"Отчет DOCX успешно сохранен в: {DOCX_PATH}")

if __name__ == "__main__":
    create_report()
