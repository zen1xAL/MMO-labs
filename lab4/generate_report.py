"""
Генератор официального отчета по Лабораторной работе №4 по курсу «Методы машинного обучения».
Тема: «Бинарная классификация данных (Логистическая регрессия, SVM, CART)».
Студент: гр. 351002 Власовец А. И. (Вариант 7).
Преподаватель: Лебедевич А. В.
Датасет: Bankloan.csv (Кредитный скоринг заемщиков).
Оформление строго соответствует стандарту БГУИР СТП 01-2017.
"""

import os
import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"d:\MMO\lab4"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORT_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORT_DIR, exist_ok=True)
DOCX_PATH = os.path.join(REPORT_DIR, "Отчет_ЛР04_Власовец_Вариант7.docx")

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
    print("=" * 70)
    print("ГЕНЕРАЦИЯ ОТЧЕТА ПО СТП 01-2017: Отчет_ЛР04_Власовец_Вариант7.docx")
    print("=" * 70)

    doc = docx.Document()

    # 1. Настройка полей страницы А4 (Приложение Л СТП 01-2017)
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
    style_normal.paragraph_format.first_line_indent = Mm(12.5)
    style_normal.paragraph_format.space_after = Pt(0)
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # -------------------------------------------------------------------------
    # ТИТУЛЬНЫЙ ЛИСТ (СТП 01-2017 Приложение Л)
    # -------------------------------------------------------------------------
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Mm(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Министерство образования Республики Беларусь\n"
                  "Белорусский государственный университет информатики и радиоэлектроники\n"
                  "Факультет компьютерных систем и сетей\n"
                  "Кафедра программного обеспечения информационных технологий")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = False

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(80)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.first_line_indent = Mm(0)
    p_title.paragraph_format.line_spacing = 1.5
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("ОТЧЕТ\nПО ЛАБОРАТОРНОЙ РАБОТЕ № 4\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(16)
    r_t1.font.bold = False

    r_t2 = p_title.add_run("«БИНАРНАЯ КЛАССИФИКАЦИЯ ДАННЫХ\n(ЛОГИСТИЧЕСКАЯ РЕГРЕССИЯ, SVM, CART)»\n")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(14)
    r_t2.font.bold = False

    r_t3 = p_title.add_run("Дисциплина: «Методы машинного обучения»\nВариант 7")
    r_t3.font.name = "Times New Roman"
    r_t3.font.size = Pt(13)
    r_t3.font.bold = False

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(80)

    # Таблица исполнителя и преподавателя (без рамок)
    tbl_auth = doc.add_table(rows=2, cols=2)
    tbl_auth.alignment = WD_TABLE_ALIGNMENT.RIGHT
    tbl_auth.autofit = False
    tbl_auth.columns[0].width = Mm(90)
    tbl_auth.columns[1].width = Mm(75)

    c00 = tbl_auth.cell(0, 0).paragraphs[0]
    c00.paragraph_format.first_line_indent = Mm(0)
    c00.paragraph_format.line_spacing = 1.15
    c00.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = c00.add_run("Выполнил:\nстудент гр. 351002")
    r.font.size = Pt(12)
    r.font.bold = False

    c01 = tbl_auth.cell(0, 1).paragraphs[0]
    c01.paragraph_format.first_line_indent = Mm(0)
    c01.paragraph_format.line_spacing = 1.15
    c01.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = c01.add_run("А. И. Власовец")
    r.font.size = Pt(12)
    r.font.bold = False

    c10 = tbl_auth.cell(1, 0).paragraphs[0]
    c10.paragraph_format.first_line_indent = Mm(0)
    c10.paragraph_format.line_spacing = 1.15
    c10.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = c10.add_run("Проверил:\nпреподаватель")
    r.font.size = Pt(12)
    r.font.bold = False

    c11 = tbl_auth.cell(1, 1).paragraphs[0]
    c11.paragraph_format.first_line_indent = Mm(0)
    c11.paragraph_format.line_spacing = 1.15
    c11.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = c11.add_run("А. В. Лебедевич")
    r.font.size = Pt(12)
    r.font.bold = False

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(80)

    p_city = doc.add_paragraph()
    p_city.paragraph_format.first_line_indent = Mm(0)
    p_city.paragraph_format.line_spacing = 1.0
    p_city.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_city.add_run("Минск 2026")
    r_city.font.name = "Times New Roman"
    r_city.font.size = Pt(12)
    r_city.font.bold = False

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # СОДЕРЖАТЕЛЬНАЯ ЧАСТЬ ОТЧЕТА
    # -------------------------------------------------------------------------

    # ЦЕЛЬ РАБОТЫ
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("ЦЕЛЬ РАБОТЫ")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("Приобретение практических навыков решения прикладных задач бинарной классификации, предварительной обработки и стандартизации данных, построения и тонкой настройки математических моделей классификации: логистической регрессии, метода опорных векторов (SVM) и дерева решений (CART), а также сравнительного анализа их обобщающей способности с помощью матриц ошибок (Confusion Matrix), ROC и Precision-Recall кривых.")

    # ЗАДАНИЕ
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ (ВАРИАНТ 7)")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("1. Импортировать датасет для бинарной классификации (выбран Bankloan.csv — 1150 анкет заемщиков банка, целевой бинарный признак default).\n"
                          "2. Очистить датасет от пропусков и выбросов, разделить выборку на историческую обучающую и неразмеченную для скоринга, выполнить стандартизацию признаков StandardScaler.\n"
                          "3. Сформировать предиктивный набор из 8 финансовых факторов риска.\n"
                          "4. Построить модели бинарной классификации: логистическую регрессию, SVM (с линейным и RBF ядрами) и дерево решений CART.\n"
                          "5. Оценить качество моделей по метрикам Accuracy, Precision, Recall, F1-Score, ROC-AUC, PR-AUC, построить матрицы ошибок и провести кредитный скоринг 450 новых соискателей.")

    # 1. АНАЛИЗ ДАТАСЕТА
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("1. СТРУКТУРА ДАТАСЕТА И ПРЕДОБРАБОТКА ДАННЫХ")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("В качестве объекта исследования выбран реальный массив данных коммерческого банка Bankloan.csv, содержащий информацию о 1150 заемщиках по 8 ключевым числовым экономическим характеристикам:")
    p = doc.add_paragraph("- age — возраст клиента в годах (от 20 до 56 лет, среднее 34.9 года);\n"
                          "- ed — уровень образования по шкале от 1 (базовое) до 5 (послевузовское);\n"
                          "- employ — стаж непрерывной работы на текущем месте в годах (от 0 до 31 года, среднее 8.4 года);\n"
                          "- address — срок проживания по текущему месту жительства в годах (от 0 до 34 лет, среднее 8.3 года);\n"
                          "- income — годовой доход клиента в тыс. долларов (от 14 до 446 тыс. долл., среднее 45.6 тыс. долл.);\n"
                          "- debtinc — коэффициент долговой нагрузки (Debt-to-Income, DTI) в процентах (от 0.4% до 41.3%, среднее 10.3%);\n"
                          "- creddebt — задолженность по кредитным картам в тыс. долларов (от 0.01 до 20.56 тыс. долл., среднее 1.55 тыс. долл.);\n"
                          "- othdebt — прочие непогашенные долговые обязательства в тыс. долларов (от 0.05 до 27.03 тыс. долл., среднее 3.06 тыс. долл.);\n"
                          "- default — целевой бинарный признак: 0 — благонадежный заемщик, вернувший кредит в срок; 1 — проблемный заемщик, допустивший дефолт.")

    p = doc.add_paragraph("При аудите пропущенных значений установлено, что во всех 8 признаках пропуски отсутствуют (100% заполненность). Пропуски присутствуют только в целевой колонке default в объеме ровно 450 строк. Это обусловлено спецификой кредитной организации: 700 строк представляют собой исторический кредитный портфель банка с известной платежной историей, а 450 строк — пул новых кандидатов, ожидающих скоринговой оценки для принятия решения о выдаче кредита.")

    # Вставка Рис 4.1
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "01_dataset_and_missing_analysis.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.1 – Структура базы данных заемщиков, распределение целевого класса и аудит выборок")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("В обучающей выборке из 700 размеченных заемщиков 517 клиентов являются платежеспособными (73.86%, класс 0), а 183 клиента допустили дефолт (26.14%, класс 1). Соотношение классов составляет примерно 3:1, что типично для финансового скоринга и требует обязательной стратификации при разбиении на обучающую и тестовую выборки.")

    # Вставка Рис 4.2
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "02_features_distributions_and_boxplots.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.2 – Гистограммы распределений финансовых признаков с ядерной оценкой плотности (KDE)")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("Анализ гистограмм и плотностей вероятности (KDE) показывает выраженную правостороннюю асимметрию признаков доходов и долгов (income, creddebt, othdebt, debtinc). По правилу Тьюки (1.5×IQR) выявлены отдельные высокодоходные и сильно закредитованные заемщики, представляющие естественную вариативность рыночной выборки.")

    # 2. КОРРЕЛЯЦИОННЫЙ АНАЛИЗ
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("2. КОРРЕЛЯЦИОННЫЙ АНАЛИЗ ФАКТОРОВ КРЕДИТНОГО РИСКА")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("На рисунке 4.3 представлена корреляционная матрица Пирсона между признаками и целевым индикатором неплатежа. Наибольшую линейную связь с дефолтом демонстрирует коэффициент долговой нагрузки debtinc (r = +0.39), а также задолженность по кредитным картам creddebt (r = +0.24). Напротив, длительный трудовой стаж employ (r = -0.28) и оседлость заемщика address (r = -0.16) выступают сильнейшими стабилизирующими факторами.")

    # Вставка Рис 4.3
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "03_outliers_and_correlation_heatmap.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.3 – Линейные взаимосвязи признаков и разделение долговой нагрузки по классам заемщиков")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("Выборка из 700 клиентов разделена на обучающую (80%, 560 записей) и тестовую (20%, 140 записей) со стратификацией (stratify=y, random_state=42). Выполнена Z-стандартизация признаков алгоритмом StandardScaler, вычисленным строго на обучающей подвыборке, что исключает утечку данных (Data Leakage).")

    # 3. ПОСТРОЕНИЕ И ОЦЕНКА МОДЕЛЕЙ
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("3. ПОСТРОЕНИЕ И СРАВНИТЕЛЬНЫЙ АНАЛИЗ КЛАССИФИКАТОРОВ")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("В соответствии с заданием построены и исследованы три фундаментальных класса моделей бинарной классификации:")

    p = doc.add_paragraph("1. Логистическая регрессия (Logistic Regression). Моделирует апостериорную вероятность дефолта через логистическую функцию сигмоиды:\n"
                          "P(y=1|x) = 1 / (1 + exp(-w^T x))\n"
                          "Коэффициенты модели имеют строгую интерпретацию логарифма отношения шансов (Log-Odds). На рисунке 4.4 приведены веса признаков и мультипликаторы шансов OR = exp(w). Увеличение долговой нагрузки debtinc на 1 стандартное отклонение увеличивает шансы дефолта в 2.44 раза (OR = 2.443x), а рост долга по кредиткам creddebt — в 1.77 раза (OR = 1.774x). Напротив, стаж работы employ снижает шансы дефолта более чем в 2 раза (OR = 0.476x).")

    # Вставка Рис 4.4
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "04_logistic_regression_analysis.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.4 – Интерпретация модели логистической регрессии: логистические веса и отношение шансов дефолта")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("2. Метод опорных векторов (Support Vector Machine, SVM). Построен на принципе максимизации разделяющей полосы (зазора) шириной M = 2 / ||w|| между классами заемщиков. Исследованы линейное ядро (Linear SVM, гиперплоскость с 236 опорными векторами) и нелинейное радиально-базисное ядро (RBF SVM, 265 опорных векторов). На рисунке 4.5 представлена 2D-проекция разделяющих поверхностей в пространстве наиболее значимых признаков employ и debtinc.")

    # Вставка Рис 4.5
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "05_svm_decision_boundary_and_margins.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.5 – Разделяющие границы решений и опорные векторы метода SVM (Linear vs RBF ядра)")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("3. Дерево решений (CART). Выполняет иерархическое разбиение признакового пространства ортогональными гиперплоскостями на основе минимизации критерия неопределенности Джини: G = 1 - p_0^2 - p_1^2. Для предотвращения переобучения глубина дерева ограничена значением max_depth = 4, а минимальный размер листа min_samples_leaf = 5. Структура дерева приведена на рисунке 4.6.")

    # Вставка Рис 4.6
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "06_cart_decision_tree_visualization.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.6 – Структура дерева решений CART (глубина max_depth = 4, критерий Gini)")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("В корневом узле дерева решений первым предикатом выступает долговая нагрузка (debtinc <= 0.655σ, что соответствует 14.7% порогу). При низком долге и стаже работы свыше 2.5 лет клиент попадает в надежный лист с вероятностью возврата более 93%.")

    # 4. СРАВНЕНИЕ МЕТРИК И КРИВЫЕ КАЧЕСТВА
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("4. СРАВНИТЕЛЬНАЯ ОЦЕНКА КАЧЕСТВА КЛАССИФИКАЦИИ")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("Комплексная оценка моделей выполнена на тестовой выборке из 140 клиентов. В таблице 4.1 сведены ключевые метрики классификации.")

    # ТАБЛИЦА 4.1
    p_t = doc.add_paragraph("Таблица 4.1 – Метрики качества моделей бинарной классификации на тестовой выборке")
    p_t.paragraph_format.first_line_indent = Mm(0)
    p_t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = doc.add_table(rows=5, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    headers = ["Модель", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.paragraphs[0].paragraph_format.first_line_indent = Mm(0)
        cell.paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(h)
        r.font.size = Pt(11)
        r.font.bold = True

    data_rows = [
        ["Logistic Regression", "0.8143", "0.6571", "0.6216", "0.6389", "0.8670"],
        ["SVM (Linear Kernel)", "0.8357", "0.7333", "0.5946", "0.6567", "0.8699"],
        ["SVM (RBF Kernel)", "0.8071", "0.6923", "0.4865", "0.5714", "0.8066"],
        ["CART (Decision Tree)", "0.7357", "0.5000", "0.3514", "0.4127", "0.7825"]
    ]

    for row_idx, r_data in enumerate(data_rows, start=1):
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx, col_idx)
            cell.paragraphs[0].paragraph_format.first_line_indent = Mm(0)
            cell.paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = cell.paragraphs[0].add_run(val)
            r.font.size = Pt(11)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)

    # Вставка Рис 4.7
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "07_confusion_matrices_comparison.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.7 – Сопоставление матриц ошибок (Confusion Matrices) исследуемых алгоритмов классификации")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("Анализ матриц ошибок показывает, что в банковском кредитовании ключевой является ошибка II рода (False Negative — выдача кредита дефолтному заемщику). Модель логистической регрессии продемонстрировала наименьшее количество таких критических ошибок (FN = 14), обеспечив максимальную полноту выявления дефолтов Recall = 62.16%. Модель Linear SVM показала максимальную общую точность (Accuracy = 83.57%) и минимальное количество ложных отказов благонадежным клиентам (FP = 8, Precision = 73.33%).")

    # Вставка Рис 4.8
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "08_roc_and_pr_curves_comparison.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.8 – Сравнительный анализ интегральных кривых качества классификации: ROC-кривые и PR-кривые")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("На рисунке 4.8 приведены интегральные кривые качества. Площадь под ROC-кривой (ROC-AUC) для Linear SVM и логистической регрессии достигает 0.8699 и 0.8670 соответственно, что свидетельствует об отличном качестве разделения классов. На Precision-Recall кривых обе непрерывные модели существенно превосходят базовый уровень случайного угадывания (P_pos = 0.264), достигая площади PR-AUC свыше 0.73.")

    # Вставка Рис 4.9
    p_img = doc.add_paragraph()
    p_img.paragraph_format.first_line_indent = Mm(0)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(os.path.join(PLOTS_DIR, "09_model_metrics_and_feature_importances.png"), width=Mm(160))
    p_cap = doc.add_paragraph("Рисунок 4.9 – Итоговое сопоставление метрик классификаторов и ключевые факторы риска кредитования")
    p_cap.paragraph_format.first_line_indent = Mm(0)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph("На основе полученной лучшей модели Linear SVM проведен автоматизированный скоринг 450 новых соискателей кредита с порогом отсечения дефолтного риска 35%: 336 анкет (74.7%) получили рекомендацию на одобрение, а 114 анкет (25.3%) отклонены как высокорисковые.")

    # ЗАКЛЮЧЕНИЕ
    p_h = doc.add_paragraph()
    p_h.paragraph_format.first_line_indent = Mm(0)
    p_h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run("ЗАКЛЮЧЕНИЕ")
    r.font.size = Pt(14)
    r.font.bold = False

    p = doc.add_paragraph("В ходе выполнения лабораторной работы решена задача бинарной классификации банковских заемщиков:\n"
                          "1. Проведен разведочный анализ данных 1150 клиентов, выявлены ключевые финансовые маркеры риска невозврата: долговая нагрузка debtinc и стаж работы employ.\n"
                          "2. Построены и исследованы три алгоритма классификации. Наилучшие результаты продемонстрировали модель опорных векторов Linear SVM (Accuracy 83.57%, ROC-AUC 0.8699, F1 0.6567) и логистическая регрессия (Accuracy 81.43%, ROC-AUC 0.8670, Recall 62.16%).\n"
                          "3. Дерево решений CART показало более скромные интегральные метрики (Accuracy 73.57%, ROC-AUC 0.7825), однако обеспечило прозрачные пороговые решающие правила, удобные для комплаенс-контроля банка.\n"
                          "4. Разработанный алгоритм успешно применен для скоринговой классификации 450 неразмеченных анкет, сформировав файл рекомендаций Bankloan_unlabeled_scored.csv.")

    doc.save(DOCX_PATH)
    doc_size_mb = os.path.getsize(DOCX_PATH) / (1024 * 1024)
    print(f"\n[OK] Документ DOCX успешно сохранен: {DOCX_PATH} ({doc_size_mb:.2f} МБ)")

if __name__ == "__main__":
    create_report()
