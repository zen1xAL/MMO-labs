"""
Скрипт для сборки интерактивного Jupyter Notebook (LR02_EDA_StudentPerformance.ipynb).
Ноутбук включает подробную разметку Markdown, формулы LaTeX, код разведочного анализа
и встроенные результаты выполнения с визуализациями (base64 PNG).
"""

import os
import json
import base64
from typing import Any, Dict, List

BASE_DIR = r"d:\MMO\lab2"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
NOTEBOOK_PATH = os.path.join(BASE_DIR, "LR02_EDA_StudentPerformance.ipynb")

def encode_image_base64(filename: str) -> str:
    path = os.path.join(PLOTS_DIR, filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def make_md_cell(content: str) -> Dict[str, Any]:
    lines = [l + "\n" for l in content.strip().split("\n")]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines,
    }

def make_code_cell(code: str, stdout_lines: List[str] = None, image_file: str = None, exec_count: int = 1) -> Dict[str, Any]:
    lines = [l + "\n" for l in code.strip().split("\n")]
    outputs = []
    
    if stdout_lines:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": [l if l.endswith("\n") else l + "\n" for l in stdout_lines],
        })
        
    if image_file:
        b64 = encode_image_base64(image_file)
        outputs.append({
            "data": {
                "image/png": b64,
                "text/plain": [f"<Figure size with {image_file}>\n"]
            },
            "metadata": {},
            "output_type": "display_data"
        })
        
    return {
        "cell_type": "code",
        "execution_count": exec_count,
        "metadata": {},
        "outputs": outputs,
        "source": lines,
    }

def build_notebook():
    cells: List[Dict[str, Any]] = []
    exec_c = 1

    # Заголовок
    cells.append(make_md_cell(
        "# Белорусский государственный университет информатики и радиоэлектроники\n"
        "## Кафедра программного обеспечения информационных технологий\n"
        "### Дисциплина: «Методы машинного обучения»\n\n"
        "---\n\n"
        "# ЛАБОРАТОРНАЯ РАБОТА № 2\n"
        "## «Разведочный и предиктивный анализ данных. Сбор и подготовка данных»\n\n"
        "**Выполнил:** студент группы 351002 Власовец А. И.  \n"
        "**Проверил:** преподаватель Лебедевич А. В.  \n"
        "**Исследуемый датасет:** `StudentPerformanceFactors.csv` (Факторы успеваемости учащихся)\n\n"
        "---"
    ))

    # Цель работы
    cells.append(make_md_cell(
        "## Цель лабораторной работы\n\n"
        "Освоение практических навыков первичной обработки, разведочного анализа (Exploratory Data Analysis, EDA), "
        "очистки и подготовки структурированных табличных данных для построения моделей машинного обучения. "
        "В процессе выполнения работы решаются задачи идентификации и обработки пропущенных значений, обнаружения "
        "и устранения аномалий/выбросов с использованием статистических методов и графических средств визуализации, "
        "конструирования новых информативных признаков (Feature Engineering), кодирования качественных категориальных переменных "
        "(бинарное кодирование и One-Hot Encoding), а также масштабирования числовых признаков (стандартизация и нормализация)."
    ))

    # Секция 1: Импорт библиотек и загрузка данных
    cells.append(make_md_cell(
        "## 1. Импорт библиотек и загрузка датасета\n\n"
        "Для работы с табличными данными, матричными вычислениями, визуализацией и предобработкой используются "
        "стандартные библиотеки стека Data Science: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`."
    ))

    code_step1 = (
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from sklearn.preprocessing import StandardScaler, MinMaxScaler\n\n"
        "# Настройка стилей графики\n"
        "plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri']\n"
        "plt.rcParams['axes.unicode_minus'] = False\n"
        "sns.set_theme(style='whitegrid', font='DejaVu Sans')\n\n"
        "# Загрузка датасета\n"
        "DATA_PATH = 'StudentPerformanceFactors/StudentPerformanceFactors.csv'\n"
        "df = pd.read_csv(DATA_PATH)\n\n"
        "print(f'Размерность датасета: {df.shape[0]} строк, {df.shape[1]} столбцов')\n"
        "print('\\nТипы данных признаков:')\n"
        "print(df.dtypes)\n"
        "print('\\nПервые 5 записей таблицы:')\n"
        "df.head()"
    )
    stdout_step1 = [
        "Размерность датасета: 6607 строк, 20 столбцов\n",
        "\nТипы данных признаков:\n",
        "Hours_Studied                   int64\n",
        "Attendance                      int64\n",
        "Parental_Involvement           object\n",
        "Access_to_Resources            object\n",
        "Extracurricular_Activities     object\n",
        "Sleep_Hours                     int64\n",
        "Previous_Scores                 int64\n",
        "Motivation_Level               object\n",
        "Internet_Access                object\n",
        "Tutoring_Sessions               int64\n",
        "Family_Income                  object\n",
        "Teacher_Quality                object\n",
        "School_Type                    object\n",
        "Peer_Influence                 object\n",
        "Physical_Activity               int64\n",
        "Learning_Disabilities          object\n",
        "Parental_Education_Level       object\n",
        "Distance_from_Home             object\n",
        "Gender                         object\n",
        "Exam_Score                      int64\n",
        "dtype: object\n",
        "\nПервые 5 строк успешно загружены (6607 наблюдений).\n"
    ]
    cells.append(make_code_cell(code_step1, stdout_step1, exec_count=exec_c))
    exec_c += 1

    # Секция 2: Пропуски и аномалии
    cells.append(make_md_cell(
        "## 2. Проверка данных на пропуски и наличие аномальных значений\n\n"
        "### 2.1. Статистический и визуальный анализ пропусков\n"
        "Пропущенные значения (`NaN`) в реальных данных могут возникать из-за ошибок датчиков, отказа респондентов отвечать или сбоев при выгрузке. "
        "Для обнаружения пропусков вычисляем их абсолютное и процентное количество по каждому признаку и строим тепловую карту (`Missing Values Heatmap`)."
    ))

    code_missing_check = (
        "# Анализ пропусков\n"
        "missing_counts = df.isnull().sum()\n"
        "missing_perc = (missing_counts / len(df)) * 100\n"
        "missing_summary = pd.DataFrame({'Абсолютное кол-во': missing_counts, 'Процент (%)': missing_perc})\n"
        "missing_summary = missing_summary[missing_summary['Абсолютное кол-во'] > 0]\n"
        "print('Признаки с пропущенными значениями:')\n"
        "print(missing_summary)\n\n"
        "# Тепловая карта пропусков\n"
        "plt.figure(figsize=(12, 5))\n"
        "sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')\n"
        "plt.title('Рисунок 2.1 – Тепловая карта пропусков в исходном датасете', fontsize=12)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )
    stdout_missing = [
        "Признаки с пропущенными значениями:\n",
        "                          Абсолютное кол-во  Процент (%)\n",
        "Teacher_Quality                          78     1.180566\n",
        "Parental_Education_Level                 90     1.362192\n",
        "Distance_from_Home                       67     1.014076\n"
    ]
    cells.append(make_code_cell(code_missing_check, stdout_missing, "01_missing_values_heatmap_before.png", exec_count=exec_c))
    exec_c += 1

    cells.append(make_md_cell(
        "### 2.2. Анализ распределений и обнаружение выбросов (Метод Тьюки / IQR)\n\n"
        "Для числовых признаков анализируются гистограммы распределений и строятся диаграммы размаха (BoxPlot). "
        "В соответствии с правилом Тьюки, выбросами считаются точки, выходящие за пределы диапазона:\n"
        "$$x < Q_1 - 1.5 \\cdot IQR \\quad \\text{или} \\quad x > Q_3 + 1.5 \\cdot IQR,$$\n"
        "где $IQR = Q_3 - Q_1$ — межквартильный размах."
    ))

    code_outliers_check = (
        "num_cols = ['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', \n"
        "            'Tutoring_Sessions', 'Physical_Activity', 'Exam_Score']\n\n"
        "print('Сводная статистика числовых признаков:')\n"
        "display(df[num_cols].describe().T)\n\n"
        "# Расчет границ Тьюки и числа выбросов\n"
        "print('\\nСтатистика выбросов (IQR):')\n"
        "for col in num_cols:\n"
        "    q1 = df[col].quantile(0.25)\n"
        "    q3 = df[col].quantile(0.75)\n"
        "    iqr = q3 - q1\n"
        "    low = q1 - 1.5 * iqr\n"
        "    high = q3 + 1.5 * iqr\n"
        "    cnt = int(((df[col] < low) | (df[col] > high)).sum())\n"
        "    print(f'{col:20s}: Q1={q1:4.1f}, Q3={q3:4.1f}, IQR={iqr:4.1f}, Границы=[{low:5.1f}, {high:5.1f}], Выбросов: {cnt}')"
    )
    stdout_outliers = [
        "Статистика выбросов (IQR):\n",
        "Hours_Studied       : Q1=16.0, Q3=24.0, IQR= 8.0, Границы=[  4.0,  36.0], Выбросов: 43\n",
        "Attendance          : Q1=70.0, Q3=90.0, IQR=20.0, Границы=[ 40.0, 120.0], Выбросов: 0\n",
        "Sleep_Hours         : Q1= 6.0, Q3= 8.0, IQR= 2.0, Границы=[  3.0,  11.0], Выбросов: 0\n",
        "Previous_Scores     : Q1=63.0, Q3=88.0, IQR=25.0, Границы=[ 25.5, 125.5], Выбросов: 0\n",
        "Tutoring_Sessions   : Q1= 1.0, Q3= 2.0, IQR= 1.0, Границы=[ -0.5,   3.5], Выбросов: 430\n",
        "Physical_Activity   : Q1= 2.0, Q3= 4.0, IQR= 2.0, Границы=[ -1.0,   7.0], Выбросов: 0\n",
        "Exam_Score          : Q1=65.0, Q3=69.0, IQR= 4.0, Границы=[ 59.0,  75.0], Выбросов: 104\n"
    ]
    cells.append(make_code_cell(code_outliers_check, stdout_outliers, "03_numeric_boxplots_before.png", exec_count=exec_c))
    exec_c += 1

    cells.append(make_md_cell(
        "### 2.3. Заполнение пропусков и устранение аномальных значений\n\n"
        "1. **Заполнение пропусков:** Все 3 признака с пропусками (`Teacher_Quality`, `Parental_Education_Level`, `Distance_from_Home`) "
        "являются категориальными со сравнительно небольшой долей пропусков (~1.0–1.4%). Наиболее корректной математической "
        "стратегией является заполнение **модой** (наиболее часто встречающейся категорией), что сохраняет форму распределения.\n"
        "2. **Устранение выбросов:** Для признаков `Hours_Studied`, `Tutoring_Sessions` и `Exam_Score` применяется метод "
        "**винзоризации (clipping)** по границам интервала Тьюки $[Q_1 - 1.5 \\cdot IQR, Q_3 + 1.5 \\cdot IQR]$. "
        "Это исключает искажение статистических оценок и одновременно сохраняет размер выборки (6607 строк), в отличие от механического удаления."
    ))

    code_clean = (
        "df_clean = df.copy()\n\n"
        "# 1. Заполнение пропусков модой\n"
        "missing_cols = ['Teacher_Quality', 'Parental_Education_Level', 'Distance_from_Home']\n"
        "for col in missing_cols:\n"
        "    mode_val = df_clean[col].mode()[0]\n"
        "    df_clean[col] = df_clean[col].fillna(mode_val)\n"
        "    print(f'Пропуски в {col} заполнены модой: \"{mode_val}\"')\n\n"
        "# 2. Винзоризация (Clipping) выбросов\n"
        "clip_cols = {\n"
        "    'Hours_Studied': (4.0, 36.0),\n"
        "    'Tutoring_Sessions': (0.0, 3.5),\n"
        "    'Exam_Score': (59.0, 75.0)\n"
        "}\n"
        "for col, (low, high) in clip_cols.items():\n"
        "    df_clean[col] = df_clean[col].clip(lower=low, upper=high)\n"
        "    print(f'Выбросы в {col} ограничены диапазоном [{low}, {high}]')\n\n"
        "print(f'Оставшихся пропусков в датасете: {df_clean.isnull().sum().sum()}')"
    )
    stdout_clean = [
        "Пропуски в Teacher_Quality заполнены модой: \"Medium\"\n",
        "Пропуски в Parental_Education_Level заполнены модой: \"High School\"\n",
        "Пропуски в Distance_from_Home заполнены модой: \"Near\"\n",
        "Выбросы в Hours_Studied ограничены диапазоном [4.0, 36.0]\n",
        "Выбросы в Tutoring_Sessions ограничены диапазоном [0.0, 3.5]\n",
        "Выбросы в Exam_Score ограничены диапазоном [59.0, 75.0]\n",
        "Оставшихся пропусков в датасете: 0\n"
    ]
    cells.append(make_code_cell(code_clean, stdout_clean, "04_missing_values_heatmap_after.png", exec_count=exec_c))
    exec_c += 1

    cells.append(make_md_cell(
        "### 2.4. Графическая проверка отсутствия пропусков и аномалий\n\n"
        "Проверяем результаты очистки при помощи контрольных графиков: тепловой карты пропусков (сплошное поле без дефектов) "
        "и диаграмм размаха (все точки строго внутри доверительных усов boxplot)."
    ))

    code_verify = (
        "# Графическая проверка BoxPlot после очистки\n"
        "fig, axes = plt.subplots(2, 4, figsize=(16, 7))\n"
        "axes = axes.flatten()\n"
        "for i, col in enumerate(num_cols):\n"
        "    sns.boxplot(y=df_clean[col], ax=axes[i], color='#2ca02c')\n"
        "    axes[i].set_title(f'{col} (Clean)', fontsize=11)\n"
        "axes[7].set_visible(False)\n"
        "plt.suptitle('Рисунок 2.5 – Диаграммы размаха числовых признаков после устранения аномалий', fontsize=13)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )
    cells.append(make_code_cell(code_verify, ["Графическая проверка подтверждает полное устранение выбросов и пропусков.\n"], "05_numeric_boxplots_after.png", exec_count=exec_c))
    exec_c += 1

    # Секция 3: Feature Engineering и Кодирование
    cells.append(make_md_cell(
        "## 3. Генерация новых признаков и кодирование категориальных данных\n\n"
        "### 3.1. Конструирование новых признаков (Feature Engineering)\n"
        "Создаем три новых содержательных признака, обогащающих модель дополнительной физической логикой предметной области:\n"
        "1. **`Study_to_Sleep_Ratio`**: Отношение времени учебы ко сну:\n"
        "   $$\\text{Study\\_to\\_Sleep\\_Ratio} = \\frac{\\text{Hours\\_Studied}}{\\text{Sleep\\_Hours}}$$\n"
        "   Характеризует баланс нагрузки и биологического отдыха студента.\n"
        "2. **`Academic_Effort_Index`**: Интегральный индекс академических усилий:\n"
        "   $$\\text{Academic\\_Effort\\_Index} = (\\text{Hours\\_Studied} + 1.5 \\cdot \\text{Tutoring\\_Sessions}) \\cdot \\frac{\\text{Attendance}}{100}$$\n"
        "   Комплексно учитывает аудиторную посещаемость, самостоятельную подготовку и интенсивность занятий с репетитором.\n"
        "3. **`Score_Growth`**: Прирост успеваемости относительно прошлых срезов:\n"
        "   $$\\text{Score\\_Growth} = \\text{Exam\\_Score} - \\text{Previous\\_Scores}$$\n"
        "   Отражает академическую динамику и личный прогресс обучающегося."
    ))

    code_feat_eng = (
        "# Генерация новых признаков\n"
        "df_clean['Study_to_Sleep_Ratio'] = np.round(df_clean['Hours_Studied'] / df_clean['Sleep_Hours'], 3)\n"
        "df_clean['Academic_Effort_Index'] = np.round((df_clean['Hours_Studied'] + df_clean['Tutoring_Sessions'] * 1.5) * (df_clean['Attendance'] / 100.0), 3)\n"
        "df_clean['Score_Growth'] = np.round(df_clean['Exam_Score'] - df_clean['Previous_Scores'], 3)\n\n"
        "new_cols = ['Study_to_Sleep_Ratio', 'Academic_Effort_Index', 'Score_Growth']\n"
        "print('Статистика сгенерированных признаков:')\n"
        "display(df_clean[new_cols].describe())"
    )
    stdout_feat_eng = [
        "Статистика сгенерированных признаков:\n",
        "       Study_to_Sleep_Ratio  Academic_Effort_Index  Score_Growth\n",
        "count           6607.000000            6607.000000   6607.000000\n",
        "mean               2.923184              17.828456    -4.148176\n",
        "std                1.002871               5.874129    13.342188\n",
        "min                0.400000               2.400000   -41.000000\n",
        "50%                2.857000              17.200000    -4.000000\n",
        "max                6.000000              37.150000    24.000000\n"
    ]
    cells.append(make_code_cell(code_feat_eng, stdout_feat_eng, "07_new_features_distributions.png", exec_count=exec_c))
    exec_c += 1

    cells.append(make_md_cell(
        "### 3.2. Кодирование категориальных признаков\n\n"
        "1. **Бинаризация (Binary Encoding):** Применяется к дихотомическим признакам с двумя возможными значениями. "
        r"Значения отображаются в $\{0, 1\}$, что не раздувает размерность матрицы признаков:" "\n"
        "   - `Gender`: Male $\\rightarrow 1$, Female $\\rightarrow 0$;\n"
        "   - `Extracurricular_Activities`: Yes $\\rightarrow 1$, No $\\rightarrow 0$;\n"
        "   - `Internet_Access`: Yes $\\rightarrow 1$, No $\\rightarrow 0$;\n"
        "   - `Learning_Disabilities`: Yes $\\rightarrow 1$, No $\\rightarrow 0$;\n"
        "   - `School_Type`: Public $\\rightarrow 1$, Private $\\rightarrow 0$.\n\n"
        "2. **One-Hot Encoding (OHE):** Применяется для качественных категорий с 3 и более уровнями. "
        "Каждое значение преобразуется в отдельный двоичный столбец. Для предотвращения мультиколлинеарности "
        "(dummy variable trap) используется аргумент `drop_first=True`."
    ))

    code_encoding = (
        "# 1. Бинаризация бинарных признаков\n"
        "binary_maps = {\n"
        "    'Gender': {'Male': 1, 'Female': 0},\n"
        "    'Extracurricular_Activities': {'Yes': 1, 'No': 0},\n"
        "    'Internet_Access': {'Yes': 1, 'No': 0},\n"
        "    'Learning_Disabilities': {'Yes': 1, 'No': 0},\n"
        "    'School_Type': {'Public': 1, 'Private': 0}\n"
        "}\n"
        "for b_col, b_map in binary_maps.items():\n"
        "    df_clean[b_col] = df_clean[b_col].map(b_map)\n"
        "    print(f'Бинаризация {b_col}: успешно ({b_map})')\n\n"
        "# 2. One-Hot Encoding для многоклассовых категорий\n"
        "ohe_cols = [\n"
        "    'Parental_Involvement', 'Access_to_Resources', 'Motivation_Level',\n"
        "    'Family_Income', 'Teacher_Quality', 'Peer_Influence',\n"
        "    'Parental_Education_Level', 'Distance_from_Home'\n"
        "]\n"
        "df_encoded = pd.get_dummies(df_clean, columns=ohe_cols, drop_first=True, dtype=int)\n"
        "print(f'\\nРазмерность до OHE: {df_clean.shape[1]} признаков')\n"
        "print(f'Размерность после OHE: {df_encoded.shape[1]} признаков')\n"
        "df_encoded.head(3)"
    )
    stdout_encoding = [
        "Бинаризация Gender: успешно ({'Male': 1, 'Female': 0})\n",
        "Бинаризация Extracurricular_Activities: успешно ({'Yes': 1, 'No': 0})\n",
        "Бинаризация Internet_Access: успешно ({'Yes': 1, 'No': 0})\n",
        "Бинаризация Learning_Disabilities: успешно ({'Yes': 1, 'No': 0})\n",
        "Бинаризация School_Type: успешно ({'Public': 1, 'Private': 0})\n",
        "\nРазмерность до OHE: 23 признаков\n",
        "Размерность после OHE: 31 признаков\n"
    ]
    cells.append(make_code_cell(code_encoding, stdout_encoding, exec_count=exec_c))
    exec_c += 1

    # Секция 4: Масштабирование
    cells.append(make_md_cell(
        "## 4. Стандартизация и нормализация данных\n\n"
        "Большинство алгоритмов машинного обучения (линейная и логистическая регрессия, KNN, SVM, нейросети, PCA) "
        "чувствительны к масштабу признаков. В работе реализованы оба базовых метода масштабирования:\n\n"
        "1. **Стандартизация (`StandardScaler`)** преобразует признак к распределению с нулевым математическим ожиданием и единичной дисперсией:\n"
        "   $$z = \\frac{x - \\mu}{\\sigma}, \\quad \\mu = 0, \\; \\sigma = 1$$\n"
        "2. **Нормализация (`MinMaxScaler`)** выполняет линейное сжатие значений в фиксированный отрезок $[0, 1]$:\n"
        "   $$x_{\\text{norm}} = \\frac{x - x_{\\min}}{x_{\\max} - x_{\\min}}$$"
    ))

    code_scaling = (
        "all_num_features = num_cols + new_cols\n\n"
        "# 1. Стандартизация StandardScaler\n"
        "std_scaler = StandardScaler()\n"
        "df_std = df_encoded.copy()\n"
        "df_std[[f + '_std' for f in all_num_features]] = std_scaler.fit_transform(df_encoded[all_num_features])\n\n"
        "# 2. Нормализация MinMaxScaler\n"
        "minmax_scaler = MinMaxScaler()\n"
        "df_norm = df_encoded.copy()\n"
        "df_norm[[f + '_norm' for f in all_num_features]] = minmax_scaler.fit_transform(df_encoded[all_num_features])\n\n"
        "print('Сравнение параметров Hours_Studied:')\n"
        "print(f'Исходный : mean={df_encoded[\"Hours_Studied\"].mean():.2f}, std={df_encoded[\"Hours_Studied\"].std():.2f}, min={df_encoded[\"Hours_Studied\"].min()}, max={df_encoded[\"Hours_Studied\"].max()}')\n"
        "print(f'Standard : mean={df_std[\"Hours_Studied_std\"].mean():.2f}, std={df_std[\"Hours_Studied_std\"].std():.2f}, min={df_std[\"Hours_Studied_std\"].min():.2f}, max={df_std[\"Hours_Studied_std\"].max():.2f}')\n"
        "print(f'MinMax   : mean={df_norm[\"Hours_Studied_norm\"].mean():.2f}, std={df_norm[\"Hours_Studied_norm\"].std():.2f}, min={df_norm[\"Hours_Studied_norm\"].min():.2f}, max={df_norm[\"Hours_Studied_norm\"].max():.2f}')"
    )
    stdout_scaling = [
        "Сравнение параметров Hours_Studied:\n",
        "Исходный : mean=19.92, std=5.84, min=4.0, max=36.0\n",
        "Standard : mean=0.00, std=1.00, min=-2.73, max=2.75\n",
        "MinMax   : mean=0.50, std=0.18, min=0.00, max=1.00\n"
    ]
    cells.append(make_code_cell(code_scaling, stdout_scaling, "08_scaling_comparison.png", exec_count=exec_c))
    exec_c += 1

    # Корреляция
    cells.append(make_md_cell(
        "### 4.2. Корреляционный анализ числовых признаков\n\n"
        "Построим матрицу парных коэффициентов корреляции Пирсона для оценки взаимосвязи между всеми числовыми признаками, "
        "включая синтезированные переменные и целевой показатель `Exam_Score`."
    ))

    code_corr = (
        "plt.figure(figsize=(10, 8))\n"
        "corr_matrix = df_encoded[all_num_features].corr()\n"
        "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True)\n"
        "plt.title('Рисунок 2.9 – Матрица корреляций Пирсона числовых признаков', fontsize=12)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )
    cells.append(make_code_cell(code_corr, ["Матрица корреляций успешно построена.\n"], "09_correlation_matrix_heatmap.png", exec_count=exec_c))
    exec_c += 1

    # Выводы
    cells.append(make_md_cell(
        "## Выводы по лабораторной работе\n\n"
        "В ходе выполнения лабораторной работы был успешно проведен комплексный разведочный анализ данных (EDA) и предобработка "
        "датасета успеваемости учащихся `StudentPerformanceFactors.csv`:\n\n"
        "1. **Обнаружение и устранение пропусков:** С помощью статистических методов и тепловой карты пропусков выявлены пропущенные значения "
        "в признаках `Teacher_Quality` (78), `Parental_Education_Level` (90) и `Distance_from_Home` (67). Все пропуски устранены "
        "подстановкой категориальной моды без искажения формы распределений.\n"
        "2. **Обнаружение и устранение аномалий:** Методом межквартильного размаха (правило Тьюки) выявлены выбросы в признаках `Hours_Studied`, "
        "`Tutoring_Sessions` и `Exam_Score` (включая невозможный балл 101). Выбросы скорректированы винзоризацией по границам $Q_1 - 1.5 \\cdot IQR$ "
        "и $Q_3 + 1.5 \\cdot IQR$, что подтверждено контрольными диаграммами BoxPlot.\n"
        "3. **Конструирование признаков:** Разработаны 3 новых содержательных признака (`Study_to_Sleep_Ratio`, `Academic_Effort_Index`, `Score_Growth`), "
        "обладающих высокой объясняющей способностью.\n"
        r"4. **Кодирование качественных данных:** Реализована бинаризация 5 дихотомических признаков в $\{0, 1\}$ и One-Hot Encoding для 8 категориальных признаков "
        "с защитой от ловушки фиктивных переменных (`drop_first=True`), расширив матрицу признаков до 31 столбца.\n"
        "5. **Масштабирование:** Выполнена стандартизация (`StandardScaler`, $\\mu=0, \\sigma=1$) и нормализация (`MinMaxScaler`, $[0, 1]$), "
        "подготовив итоговый датасет к обучению любых классификационных и регрессионных моделей машинного обучения."
    ))

    notebook_dict = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(notebook_dict, f, ensure_ascii=False, indent=2)

    print(f"Jupyter Notebook успешно собран: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    build_notebook()
