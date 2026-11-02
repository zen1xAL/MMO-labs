"""
Генератор отчета по лабораторной работе №2 по дисциплине «Методы машинного обучения».
Тема: «Разведочный и предиктивный анализ данных. Знакомство с инструментами сбора и подготовки данных».
Оформление строго соответствует стандарту БГУИР СТП 01-2017:
- Формат А4, поля: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм.
- Основной текст: Times New Roman 14 пт, межстрочный интервал 1.5, абзацный отступ 1.25 см, выравнивание по ширине.
- Титульный лист: весь текст обычным (НЕ жирным) шрифтом.
- Исполнитель: студент гр. 351002 Власовец А. И., проверил: Лебедевич А. В.
- Номера страниц: в правом нижнем углу со 2 страницы (арабские цифры).
- Разделы 1 (Цель) и 5 (Выводы): сплошной связный текст без списков 1, 2, 3.
- Рисунки: по центру, подпись «Рисунок X.Y – Название».
- Таблицы: «Таблица X.Y – Название».
- Код: Courier New 9 пт, одинарный интервал, чистый текст без рамок.
"""

import os
import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"d:\MMO\lab2"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORT_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORT_DIR, exist_ok=True)
DOCX_PATH = os.path.join(REPORT_DIR, "Отчет_ЛР02_Власовец.docx")

def add_code_block(doc, code_text: str):
    """Добавляет код моноширинным шрифтом Courier New 9.0 пт без рамок."""
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

    r1 = p_title.add_run("ОТЧЕТ\nПО ЛАБОРАТОРНОЙ РАБОТЕ № 2\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(16)
    r1.font.bold = False

    r2 = p_title.add_run(
        "по дисциплине «Методы машинного обучения»\n\n"
        "Тема: «Разведочный и предиктивный анализ данных.\n"
        "Знакомство с инструментами сбора и подготовки данных»"
    )
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = False

    for _ in range(5):
        p_emp = doc.add_paragraph()
        p_emp.paragraph_format.first_line_indent = Mm(0)
        p_emp.paragraph_format.line_spacing = 1.0

    # Таблица для подписей (2 колонки: левая 90 мм, правая 75 мм)
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

    # Вспомогательные функции для заголовков и рисунков
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
    # 1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ (цельный текст)
    # =========================================================================
    add_sec_h1("1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ")
    doc.add_paragraph(
        "Целью выполнения лабораторной работы является приобретение практических навыков первичного "
        "исследования, разведочного анализа (Exploratory Data Analysis, EDA), очистки и подготовки "
        "структурированных табличных наборов данных для последующего применения в алгоритмах машинного обучения. "
        "В рамках работы осуществляется комплексное освоение методов идентификации и обработки пропущенных значений, "
        "статистического обнаружения и устранения аномалий и выбросов с использованием визуализации распределений "
        "и диаграмм размаха (BoxPlot), конструирования новых информативных признаков (Feature Engineering), "
        "преобразования качественных категориальных переменных посредством бинарного и прямого кодирования "
        "(One-Hot Encoding), а также математического масштабирования признаков методами стандартизации и нормализации."
    )

    # =========================================================================
    # 2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ
    # =========================================================================
    add_sec_h1("2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ")
    doc.add_paragraph(
        "Разведочный анализ данных представляет собой фундаментальный начальный этап разработки систем машинного "
        "обучения, ориентированный на выявление внутренней структуры набора данных, проверку статистических гипотез "
        "и обнаружение дефектов исходной выборки. Качество исходных данных напрямую определяет предельную точность "
        "предиктивных моделей согласно принципу Garbage In, Garbage Out."
    )
    doc.add_paragraph(
        "При обработке пропущенных значений (Missing Values) применяются методы удаления (Listwise Deletion) "
        "или подстановки (Imputation). Для числовых признаков с симметричным нормальным распределением оптимальным "
        "является среднее арифметическое, а для признаков со скошенными распределениями — медиана. Для категориальных "
        "признаков стандартной математической практикой является заполнение модой — наиболее часто встречающейся категорией, "
        "что минимизирует смещение выборочных вероятностей при незначительной доле пропусков."
    )
    doc.add_paragraph(
        "Для обнаружения выбросов (аномалий) широко применяется непараметрический метод межквартильного размаха "
        "(IQR, правило Тьюки). Интерквартильный размах вычисляется как разность третьего и первого квартилей: "
        "IQR = Q3 - Q1. Границами допустимых значений признака являются пределы Q1 - 1.5 * IQR (нижняя граница) "
        "и Q3 + 1.5 * IQR (верхняя граница). На диаграмме размаха (BoxPlot) эти границы определяют длину «усов», "
        "а наблюдения, выходящие за их пределы, идентифицируются как статистические выбросы. Для устранения выбросов "
        "без потери объема выборки применяется винзоризация (clipping), ограничивающая экстремальные значения "
        "установленными квартильными порогами."
    )
    doc.add_paragraph(
        "Конструирование признаков (Feature Engineering) направлено на синтез новых переменных на основе предметной "
        "логики задачи, что позволяет моделям захватывать нелинейные зависимости. Кодирование категориальных "
        "признаков переводит текстовые данные в числовой векторный вид: дихотомические признаки кодируются бинарно {0, 1}, "
        "а полиномиальные категории преобразуются посредством One-Hot Encoding (OHE) с созданием фиктивных столбцов. "
        "Для исключения строгой линейной зависимости (ловушки фиктивных переменных) один из столбцов удаляется (drop_first=True)."
    )
    doc.add_paragraph(
        "Масштабирование признаков необходимо для алгоритмов, чувствительных к абсолютным величинам признаков "
        "(линейные модели, метод k-ближайших соседей, нейронные сети). Стандартизация (StandardScaler) переводит "
        "признак в z-оценку с нулевым средним и единичной дисперсией: z = (x - mu) / sigma. Нормализация (MinMaxScaler) "
        "линейно сжимает значения в замкнутый интервал [0, 1]: x_norm = (x - x_min) / (x_max - x_min)."
    )

    # =========================================================================
    # 3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ
    # =========================================================================
    add_sec_h1("3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ")
    doc.add_paragraph(
        "В качестве объекта исследования выбран табличный датасет StudentPerformanceFactors.csv, "
        "содержащий 6607 записей об успеваемости студентов и факторах их социально-академической среды. "
        "Набор данных включает 20 разнотипных признаков, из которых 7 являются непрерывными и дискретными "
        "числовыми величинами, а 13 — качественными категориальными переменными."
    )

    # Таблица описания признаков
    table_desc = doc.add_table(rows=1, cols=3)
    table_desc.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_desc.rows[0].cells
    hdr_cells[0].text = "Название признака"
    hdr_cells[1].text = "Тип данных"
    hdr_cells[2].text = "Семантическое описание"
    for cell in hdr_cells:
        for p in cell.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(11)

    features_meta = [
        ("Hours_Studied", "int64", "Количество часов самостоятельной учебы в неделю"),
        ("Attendance", "int64", "Процент посещаемости учебных занятий (60-100%)"),
        ("Parental_Involvement", "object", "Степень вовлеченности родителей (Low, Medium, High)"),
        ("Access_to_Resources", "object", "Доступность образовательных ресурсов (Low, Medium, High)"),
        ("Extracurricular_Activities", "object", "Участие во внеклассных секциях (Yes, No)"),
        ("Sleep_Hours", "int64", "Среднее количество часов сна в сутки (4-10)"),
        ("Previous_Scores", "int64", "Баллы за предыдущие академические тесты (40-100)"),
        ("Motivation_Level", "object", "Уровень мотивации обучающегося (Low, Medium, High)"),
        ("Internet_Access", "object", "Наличие постоянного доступа в Интернет (Yes, No)"),
        ("Tutoring_Sessions", "int64", "Число дополнительных занятий с репетитором в месяц"),
        ("Family_Income", "object", "Уровень материального дохода семьи (Low, Medium, High)"),
        ("Teacher_Quality", "object", "Качество преподавания по оценке ученика (Low, Medium, High)"),
        ("School_Type", "object", "Тип образовательного учреждения (Public, Private)"),
        ("Peer_Influence", "object", "Влияние круга общения (Negative, Neutral, Positive)"),
        ("Physical_Activity", "int64", "Часов физической активности в неделю (0-6)"),
        ("Learning_Disabilities", "object", "Наличие трудностей в обучении (Yes, No)"),
        ("Parental_Education_Level", "object", "Уровень образования родителей (High School, College, Postgraduate)"),
        ("Distance_from_Home", "object", "Удаленность места учебы от дома (Near, Moderate, Far)"),
        ("Gender", "object", "Биологический пол учащегося (Male, Female)"),
        ("Exam_Score", "int64", "Целевая переменная: итоговый экзаменационный балл")
    ]

    for col, dt, desc in features_meta:
        row_cells = table_desc.add_row().cells
        row_cells[0].text = col
        row_cells[1].text = dt
        row_cells[2].text = desc
        for cell in row_cells:
            for p in cell.paragraphs:
                if p.runs:
                    p.runs[0].font.size = Pt(10)

    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.first_line_indent = Mm(0)
    p_tbl.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tbl = p_tbl.add_run("Таблица 3.1 – Структура признаков исходного датасета StudentPerformanceFactors")
    r_tbl.font.name = "Times New Roman"
    r_tbl.font.size = Pt(12)
    r_tbl.font.italic = True

    # =========================================================================
    # 4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ
    # =========================================================================
    add_sec_h1("4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ")

    add_sec_h2("4.1 Первичный анализ и выявление пропущенных значений")
    doc.add_paragraph(
        "Первичная статистическая сводка показала наличие пропущенных значений в трех категориальных "
        "признаках исходной таблицы. В признаке Teacher_Quality зафиксировано 78 пропусков (1.18%), "
        "в признаке Parental_Education_Level — 90 пропусков (1.36%), а в признаке Distance_from_Home — "
        "67 пропусков (1.01%). Для наглядной визуализации распределения пропусков по всей матрице наблюдений "
        "построена тепловая карта (Рисунок 4.1)."
    )

    add_figure("01_missing_values_heatmap_before.png", "Рисунок 4.1 – Тепловая карта пропущенных значений в исходном датасете")

    doc.add_paragraph("Ниже приведен фрагмент программной реализации загрузки и поиска пропусков:")
    code_p1 = (
        "import pandas as pd\n"
        "import seaborn as sns\n"
        "import matplotlib.pyplot as plt\n\n"
        "df = pd.read_csv('StudentPerformanceFactors/StudentPerformanceFactors.csv')\n"
        "missing = df.isnull().sum()\n"
        "print(missing[missing > 0])\n\n"
        "plt.figure(figsize=(12, 5))\n"
        "sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')\n"
        "plt.title('Тепловая карта пропущенных значений')\n"
        "plt.show()"
    )
    add_code_block(doc, code_p1)

    add_sec_h2("4.2 Анализ распределений и идентификация выбросов")
    doc.add_paragraph(
        "Для оценки формы распределений числовых характеристик построены гистограммы с ядерной оценкой плотности (KDE) "
        "(Рисунок 4.2) и диаграммы размаха BoxPlot (Рисунок 4.3). Анализ подтвердил, что распределения величин "
        "Hours_Studied, Attendance, Sleep_Hours, Previous_Scores и Exam_Score близки к унимодальным нормальным "
        "с легкой правосторонней асимметрией."
    )

    add_figure("02_numeric_distributions_before.png", "Рисунок 4.2 – Гистограммы распределений числовых признаков до очистки")
    add_figure("03_numeric_boxplots_before.png", "Рисунок 4.3 – Диаграммы размаха (BoxPlot) числовых признаков до устранения выбросов")

    doc.add_paragraph(
        "В соответствии с правилом Тьюки выполнен расчет межквартильного размаха и граничных порогов для числовых величин. "
        "Результаты представлены в Таблице 4.1. В признаке Hours_Studied выявлено 43 выброса (значения менее 4 или более 36 часов), "
        "в Tutoring_Sessions — 430 значений, превышающих 3.5 сессий в месяц, а в целевом признаке Exam_Score обнаружено "
        "104 выброса (включая аномальное ошибочное значение 101 балл при допустимой 100-балльной шкале)."
    )

    # Таблица IQR
    table_iqr = doc.add_table(rows=1, cols=6)
    table_iqr.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cells = table_iqr.rows[0].cells
    h_cells[0].text = "Признак"
    h_cells[1].text = "Q1 (25%)"
    h_cells[2].text = "Q3 (75%)"
    h_cells[3].text = "IQR"
    h_cells[4].text = "Интервал [Низ, Верх]"
    h_cells[5].text = "Выбросов"
    for cell in h_cells:
        for p in cell.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10)

    iqr_data = [
        ("Hours_Studied", "16.0", "24.0", "8.0", "[4.0, 36.0]", "43"),
        ("Attendance", "70.0", "90.0", "20.0", "[40.0, 120.0]", "0"),
        ("Sleep_Hours", "6.0", "8.0", "2.0", "[3.0, 11.0]", "0"),
        ("Previous_Scores", "63.0", "88.0", "25.0", "[25.5, 125.5]", "0"),
        ("Tutoring_Sessions", "1.0", "2.0", "1.0", "[-0.5, 3.5]", "430"),
        ("Physical_Activity", "2.0", "4.0", "2.0", "[-1.0, 7.0]", "0"),
        ("Exam_Score", "65.0", "69.0", "4.0", "[59.0, 75.0]", "104")
    ]
    for row in iqr_data:
        r_cells = table_iqr.add_row().cells
        for idx, val in enumerate(row):
            r_cells[idx].text = val
            for p in r_cells[idx].paragraphs:
                p.runs[0].font.size = Pt(9.5)

    p_tbl2 = doc.add_paragraph()
    p_tbl2.paragraph_format.first_line_indent = Mm(0)
    p_tbl2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tbl2 = p_tbl2.add_run("Таблица 4.1 – Статистика межквартильного размаха и количество выбросов")
    r_tbl2.font.name = "Times New Roman"
    r_tbl2.font.size = Pt(12)
    r_tbl2.font.italic = True

    add_sec_h2("4.3 Заполнение пропусков и устранение выбросов")
    doc.add_paragraph(
        "Поскольку пропуски обнаружены исключительно в категориальных признаках со сравнительно низкой частотой дефекта (~1%), "
        "для их заполнения использована статистическая мода. Значения признака Teacher_Quality заполнены модой «Medium», "
        "Parental_Education_Level — «High School», а Distance_from_Home — «Near». Для устранения аномалий и выбросов "
        "вместо удаления наблюдений применена винзоризация (clipping) по порогам Тьюки. Контрольная тепловая карта "
        "(Рисунок 4.4) и контрольные диаграммы размаха (Рисунок 4.5) подтвердили абсолютную чистоту датасета."
    )

    add_figure("04_missing_values_heatmap_after.png", "Рисунок 4.4 – Тепловая карта после устранения пропущенных значений (0 пропусков)")
    add_figure("05_numeric_boxplots_after.png", "Рисунок 4.5 – Диаграммы размаха числовых признаков после устранения выбросов")
    add_figure("06_numeric_distributions_after.png", "Рисунок 4.6 – Гистограммы числовых признаков после винзоризации")

    code_p2 = (
        "# 1. Импутация пропусков модой\n"
        "for col in ['Teacher_Quality', 'Parental_Education_Level', 'Distance_from_Home']:\n"
        "    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])\n\n"
        "# 2. Винзоризация по квартильным порогам Тьюки\n"
        "df_clean['Hours_Studied'] = df_clean['Hours_Studied'].clip(lower=4, upper=36)\n"
        "df_clean['Tutoring_Sessions'] = df_clean['Tutoring_Sessions'].clip(lower=0, upper=3)\n"
        "df_clean['Exam_Score'] = df_clean['Exam_Score'].clip(lower=59, upper=75)"
    )
    add_code_block(doc, code_p2)

    add_sec_h2("4.4 Конструирование новых признаков (Feature Engineering)")
    doc.add_paragraph(
        "Для повышения выразительной силы модели были сгенерированы три новых содержательных признака:\n"
        "1. Study_to_Sleep_Ratio = Hours_Studied / Sleep_Hours — коэффициент соотношения учебной нагрузки и сна, "
        "характеризующий степень переутомления студента;\n"
        "2. Academic_Effort_Index = (Hours_Studied + 1.5 * Tutoring_Sessions) * (Attendance / 100) — комплексный "
        "индекс академических усилий, объединяющий самостоятельную подготовку, помощь репетитора и дисциплину посещений;\n"
        "3. Score_Growth = Exam_Score - Previous_Scores — академическая динамика, отражающая прирост или снижение "
        "результатов относительно предшествующих срезов знаний. "
        "Распределения синтезированных признаков представлены на Рисунке 4.7."
    )

    add_figure("07_new_features_distributions.png", "Рисунок 4.7 – Распределения сконструированных признаков")

    code_p3 = (
        "# Генерация новых признаков\n"
        "df_clean['Study_to_Sleep_Ratio'] = np.round(df_clean['Hours_Studied'] / df_clean['Sleep_Hours'], 3)\n"
        "df_clean['Academic_Effort_Index'] = np.round((df_clean['Hours_Studied'] + df_clean['Tutoring_Sessions'] * 1.5) * (df_clean['Attendance'] / 100.0), 3)\n"
        "df_clean['Score_Growth'] = np.round(df_clean['Exam_Score'] - df_clean['Previous_Scores'], 3)"
    )
    add_code_block(doc, code_p3)

    add_sec_h2("4.5 Кодирование категориальных признаков")
    doc.add_paragraph(
        "Качественные признаки были преобразованы в числовую форму двумя методами:\n"
        "1. Бинаризация: для пяти бинарных признаков (Gender: Male=1, Female=0; Extracurricular_Activities, "
        "Internet_Access, Learning_Disabilities: Yes=1, No=0; School_Type: Public=1, Private=0);\n"
        "2. Прямое раздельное кодирование (One-Hot Encoding): для восьми полиномиальных категорий с тремя градациями "
        "(Parental_Involvement, Access_to_Resources, Motivation_Level, Family_Income, Teacher_Quality, Peer_Influence, "
        "Parental_Education_Level, Distance_from_Home). Применение параметра drop_first=True исключило эффект "
        "мультиколлинеарности, расширив число признаков датасета с 23 до 31."
    )

    code_p4 = (
        "# Бинарное кодирование\n"
        "binary_map = {'Male': 1, 'Female': 0, 'Yes': 1, 'No': 0, 'Public': 1, 'Private': 0}\n"
        "for col in ['Gender', 'Extracurricular_Activities', 'Internet_Access', 'Learning_Disabilities', 'School_Type']:\n"
        "    df_clean[col] = df_clean[col].map(binary_map)\n\n"
        "# One-Hot Encoding\n"
        "df_encoded = pd.get_dummies(df_clean, columns=ohe_cols, drop_first=True, dtype=int)"
    )
    add_code_block(doc, code_p4)

    add_sec_h2("4.6 Стандартизация и нормализация данных")
    doc.add_paragraph(
        "Для всех числовых признаков (включая синтезированные переменные) выполнено масштабирование методами "
        "StandardScaler (центрирование в нуле со среднеквадратическим отклонением равным единице) и MinMaxScaler "
        "(линейное сжатие в отрезок [0, 1]). Сравнительный анализ распределений признаков Hours_Studied и Attendance "
        "до и после масштабирования представлен на Рисунке 4.8. Графики наглядно демонстрируют полное сохранение "
        "формы исходного распределения при смене масштаба числовых шкал."
    )

    add_figure("08_scaling_comparison.png", "Рисунок 4.8 – Сравнение распределений до и после масштабирования")

    code_p5 = (
        "from sklearn.preprocessing import StandardScaler, MinMaxScaler\n\n"
        "std_scaler = StandardScaler()\n"
        "scaled_std = std_scaler.fit_transform(df_encoded[all_num_features])\n\n"
        "minmax_scaler = MinMaxScaler()\n"
        "scaled_norm = minmax_scaler.fit_transform(df_encoded[all_num_features])"
    )
    add_code_block(doc, code_p5)

    add_sec_h2("4.7 Корреляционный анализ числовых признаков")
    doc.add_paragraph(
        "Для выявления степени линейной взаимосвязи между числовыми признаками построена тепловая карта матрицы "
        "парных коэффициентов корреляции Пирсона (Рисунок 4.9). Анализ показал устойчивую положительную корреляцию "
        "целевого балла Exam_Score с интегральным индексом усилий Academic_Effort_Index (r = 0.77), посещаемостью "
        "Attendance (r = 0.66), часами самостоятельной подготовки Hours_Studied (r = 0.50) и отношением времени "
        "учебы ко сну Study_to_Sleep_Ratio (r = 0.40), что подтверждает высокую практическую значимость сгенерированных признаков."
    )

    add_figure("09_correlation_matrix_heatmap.png", "Рисунок 4.9 – Матрица парных коэффициентов корреляции Пирсона")

    # =========================================================================
    # 5 ВЫВОДЫ (цельный связный текст)
    # =========================================================================
    add_sec_h1("5 ВЫВОДЫ")
    doc.add_paragraph(
        "В процессе выполнения лабораторной работы были успешно освоены современные методы и инструментальные "
        "средства первичного сбора, разведочного анализа (EDA) и предобработки табличных данных на языке Python "
        "с использованием библиотек Pandas, NumPy, Matplotlib, Seaborn и Scikit-Learn. В ходе исследования набора данных "
        "StudentPerformanceFactors.csv были детально идентифицированы пропущенные значения в категориальных столбцах "
        "Teacher_Quality, Parental_Education_Level и Distance_from_Home, успешно устраненные посредством подстановки "
        "статистической моды без деформации исходной структуры выборочных распределений."
    )
    doc.add_paragraph(
        "Применение статистического правила Тьюки на основе межквартильного размаха позволило выявить и скорректировать "
        "выбросы в переменных Hours_Studied, Tutoring_Sessions и Exam_Score (включая устранение недопустимого артефакта "
        "в 101 балл). Метод винзоризации позволил сохранить исходный объем выборки в 6607 наблюдений, исключив искажение "
        "оценок дисперсии. Разработка трех новых содержательных признаков (Study_to_Sleep_Ratio, Academic_Effort_Index, "
        "Score_Growth), проведение бинаризации пяти дихотомических признаков и прямого кодирования восьми категорий "
        "с параметром drop_first=True расширили матричное представление датасета до 31 признака. Выполненное масштабирование "
        "методами StandardScaler и MinMaxScaler обеспечило полную пригодность подготовленного массива данных "
        "для обучения высокоточных метрических, линейных и нейросетевых моделей машинного обучения."
    )

    doc.save(DOCX_PATH)
    print(f"Отчет DOCX успешно сохранен в: {DOCX_PATH}")

if __name__ == "__main__":
    create_report()
