"""
Скрипт для сборки исходного проекта LaTeX (main.tex) для сервиса Overleaf.
Оформление строго соответствует стандарту БГУИР СТП 01-2017:
- Формат А4, поля: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм.
- Шрифт 14 пт, межстрочный интервал 1.5, абзацный отступ 1.25 см.
- Титульный лист: весь текст обычным (НЕ жирным) шрифтом.
- Исполнитель: студент гр. 351002 Власовец А. И., проверил: Лебедевич А. В.
- Номера страниц: в правом нижнем углу со 2 страницы (арабские цифры).
- Разделы 1 (Цель) и 5 (Выводы): сплошной связный текст без списков 1, 2, 3.
- Рисунки: по центру, подпись «Рисунок X.Y – Название».
- Код программ: шрифт 9 пт, одинарный интервал, чистый текст без рамок и таблиц.
"""

import os

BASE_DIR = r"d:\MMO\lab2"
LATEX_DIR = os.path.join(BASE_DIR, "latex")
os.makedirs(LATEX_DIR, exist_ok=True)
TEX_PATH = os.path.join(LATEX_DIR, "main.tex")
README_PATH = os.path.join(LATEX_DIR, "README_OVERLEAF.txt")

def build_latex():
    content = r"""\documentclass[14pt,a4paper]{extarticle}

% Поддержка различных компиляторов (pdfLaTeX, XeLaTeX, LuaLaTeX) на Overleaf
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T2A]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage[russian]{babel}
  \usepackage{tempora}
  \usepackage{courier}
\else
  \usepackage{fontspec}
  \defaultfontfeatures{Ligatures=TeX}
  \setmainfont{Times New Roman}
  \setmonofont{Courier New}
  \usepackage{polyglossia}
  \setmainlanguage{russian}
\fi

\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{indentfirst}
\usepackage{fancyhdr}
\usepackage{microtype}
\usepackage{tabularx}
\usepackage{float}

% Поля страницы по стандарту БГУИР СТП 01-2017 (Приложение Л)
\geometry{
  a4paper,
  left=30mm,
  right=15mm,
  top=20mm,
  bottom=20mm,
  footskip=12mm
}

% Межстрочный интервал 1.5, абзацный отступ 1.25 см
\setstretch{1.5}
\setlength{\parindent}{12.5mm}
\setlength{\parskip}{0pt}

% Нумерация страниц: в правом нижнем углу со 2-й страницы арабскими цифрами
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Форматирование подписей к рисункам и таблицам по СТП 01-2017
\DeclareCaptionLabelSeparator{emdash}{\ --- }
\captionsetup[figure]{
  name=Рисунок,
  labelsep=emdash,
  justification=centering,
  font={normalsize},
  skip=6pt
}
\captionsetup[table]{
  name=Таблица,
  labelsep=emdash,
  justification=raggedleft,
  singlelinecheck=false,
  font={normalsize},
  skip=6pt
}

% Настройка оформления кода программ: Courier New 9 пт, без рамок
\lstset{
  basicstyle=\fontsize{9pt}{10pt}\ttfamily,
  breaklines=true,
  breakatwhitespace=true,
  frame=none,
  backgroundcolor=\color{white},
  numbers=none,
  tabsize=4,
  showstringspaces=false,
  inputencoding=utf8,
  extendedchars=true,
  keepspaces=true
}

\begin{document}

% =========================================================================
% ТИТУЛЬНЫЙ ЛИСТ (весь текст НЕ жирным шрифтом)
% =========================================================================
\begin{titlepage}
  \thispagestyle{empty}
  \begin{center}
    {\fontsize{11pt}{13pt}\selectfont
      МИНИСТЕРСТВО ОБРАЗОВАНИЯ РЕСПУБЛИКИ БЕЛАРУСЬ\\[4pt]
      БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ\\[4pt]
      ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ\\[4pt]
      Факультет компьютерных систем и сетей\\[4pt]
      Кафедра программного обеспечения информационных технологий\par
    }

    \vspace{60mm}

    {\fontsize{16pt}{20pt}\selectfont
      ОТЧЕТ\\
      ПО ЛАБОРАТОРНОЙ РАБОТЕ № 2\par
    }
    \vspace{6mm}
    {\fontsize{14pt}{18pt}\selectfont
      по дисциплине «Методы машинного обучения»\\[8pt]
      Тема: «Разведочный и предиктивный анализ данных.\\
      Знакомство с инструментами сбора и подготовки данных»\par
    }

    \vspace{45mm}

    \begin{flushright}
      \begin{minipage}{0.48\textwidth}
        {\fontsize{13pt}{16pt}\selectfont
          Выполнил:\\[4pt]
          студент гр. 351002\\[4pt]
          Власовец А. И.\\[12pt]
          Проверил:\\[4pt]
          преподаватель\\[4pt]
          Лебедевич А. В.\par
        }
      \end{minipage}
    \end{flushright}

    \vfill

    {\fontsize{12pt}{14pt}\selectfont Минск 2026\par}
  \end{center}
\end{titlepage}

\setcounter{page}{2}

% =========================================================================
% 1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ (цельный связный текст)
% =========================================================================
\section*{1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ}
\addcontentsline{toc}{section}{1 ЦЕЛЬ ВЫПОЛНЕНИЯ РАБОТЫ}

Целью выполнения лабораторной работы является приобретение практических навыков первичного исследования, разведочного анализа (Exploratory Data Analysis, EDA), очистки и подготовки структурированных табличных наборов данных для последующего применения в алгоритмах машинного обучения. В рамках работы осуществляется комплексное освоение методов идентификации и обработки пропущенных значений, статистического обнаружения и устранения аномалий и выбросов с использованием визуализации распределений и диаграмм размаха (BoxPlot), конструирования новых информативных признаков (Feature Engineering), преобразования качественных категориальных переменных посредством бинарного и прямого кодирования (One-Hot Encoding), а также математического масштабирования признаков методами стандартизации и нормализации.

% =========================================================================
% 2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ
% =========================================================================
\section*{2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ}
\addcontentsline{toc}{section}{2 КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ}

Разведочный анализ данных представляет собой фундаментальный начальный этап разработки систем машинного обучения, ориентированный на выявление внутренней структуры набора данных, проверку статистических гипотез и обнаружение дефектов исходной выборки. Качество исходных данных напрямую определяет предельную точность предиктивных моделей.

При обработке пропущенных значений применяются методы удаления либо подстановки (Imputation). Для числовых признаков используется математическое ожидание или медиана, а для категориальных признаков стандартной практикой является заполнение модой --- наиболее часто встречающейся категорией, что минимизирует смещение выборочных вероятностей при незначительной доле пропусков.

Для обнаружения выбросов широко применяется непараметрический метод межквартильного размаха (IQR, правило Тьюки). Интерквартильный размах вычисляется как разность третьего и первого квартилей:
\begin{equation}
IQR = Q_3 - Q_1.
\end{equation}
Границами допустимых значений признака являются пределы:
\begin{equation}
[Q_1 - 1.5 \cdot IQR, \; Q_3 + 1.5 \cdot IQR].
\end{equation}
На диаграмме размаха (BoxPlot) эти границы определяют длину «усов», а точки за их пределами идентифицируются как выбросы. Для их устранения применяется винзоризация (clipping), сохраняющая исходный объем выборки.

Конструирование признаков (Feature Engineering) направлено на синтез новых переменных на основе предметной логики. Кодирование категориальных признаков переводит качественные данные в числовой векторный вид: бинарное кодирование отображает дихотомические значения в $\{0, 1\}$, а прямое раздельное кодирование (One-Hot Encoding) создает индикаторные бинарные столбцы с исключением ловушки фиктивных переменных (\texttt{drop\_first=True}).

Масштабирование признаков необходимо для выравнивания весов параметров в моделях. Стандартизация (\texttt{StandardScaler}) преобразует признак в $z$-оценку с нулевым средним и единичной дисперсией:
\begin{equation}
z = \frac{x - \mu}{\sigma}, \quad \mu = 0, \; \sigma = 1.
\end{equation}
Нормализация (\texttt{MinMaxScaler}) выполняет сжатие в отрезок $[0, 1]$:
\begin{equation}
x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}.
\end{equation}

% =========================================================================
% 3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ
% =========================================================================
\section*{3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ}
\addcontentsline{toc}{section}{3 ОПИСАНИЕ ИССЛЕДУЕМОГО НАБОРА ДАННЫХ}

В качестве объекта исследования выбран датасет \texttt{StudentPerformanceFactors.csv}, содержащий 6607 записей об успеваемости студентов и факторах их социально-академической среды. Набор включает 20 разнотипных признаков: 7 числовых и 13 категориальных. Структура набора данных приведена в таблице 3.1.

\begin{table}[H]
\caption{Структура признаков датасета StudentPerformanceFactors}
\centering
\small
\begin{tabularx}{\textwidth}{|l|l|X|}
\hline
\textbf{Признак} & \textbf{Тип} & \textbf{Описание} \\
\hline
Hours\_Studied & int64 & Часы самостоятельной учебы в неделю (1--44) \\
Attendance & int64 & Процент посещаемости занятий (60--100\%) \\
Parental\_Involvement & object & Вовлеченность родителей (Low, Medium, High) \\
Access\_to\_Resources & object & Доступ к учебным ресурсам (Low, Medium, High) \\
Extracurricular\_Activities & object & Участие во внеклассных секциях (Yes, No) \\
Sleep\_Hours & int64 & Количество часов сна в сутки (4--10) \\
Previous\_Scores & int64 & Баллы за предыдущие тесты (40--100) \\
Motivation\_Level & object & Уровень учебной мотивации (Low, Medium, High) \\
Internet\_Access & object & Наличие доступа в Интернет (Yes, No) \\
Tutoring\_Sessions & int64 & Занятия с репетитором в месяц (0--8) \\
Family\_Income & object & Уровень дохода семьи (Low, Medium, High) \\
Teacher\_Quality & object & Оценка качества преподавания (Low, Medium, High) \\
School\_Type & object & Тип школы (Public, Private) \\
Peer\_Influence & object & Влияние окружения (Negative, Neutral, Positive) \\
Physical\_Activity & int64 & Часов физической активности в неделю (0--6) \\
Learning\_Disabilities & object & Наличие трудностей в учебе (Yes, No) \\
Parental\_Education\_Level & object & Образование родителей (High School, College, Postgraduate) \\
Distance\_from\_Home & object & Удаленность дома от места учебы (Near, Moderate, Far) \\
Gender & object & Пол обучающегося (Male, Female) \\
Exam\_Score & int64 & Целевая переменная: экзаменационный балл \\
\hline
\end{tabularx}
\end{table}

% =========================================================================
% 4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ
% =========================================================================
\section*{4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ}
\addcontentsline{toc}{section}{4 ХОД ВЫПОЛНЕНИЯ РАБОТЫ И АНАЛИЗ РЕЗУЛЬТАТОВ}

\subsection*{4.1 Первичный анализ и выявление пропущенных значений}

Первичный статистический анализ выявил наличие пропусков в трех категориальных столбцах: \texttt{Teacher\_Quality} (78 пропусков, 1.18\%), \texttt{Parental\_Education\_Level} (90 пропусков, 1.36\%) и \texttt{Distance\_from\_Home} (67 пропусков, 1.01\%). Тепловая карта распределения пропусков представлена на рисунке 4.1.

\begin{figure}[H]
\centering
\includegraphics[width=0.88\textwidth]{plots/01_missing_values_heatmap_before.png}
\caption{Тепловая карта пропущенных значений в исходном датасете}
\end{figure}

Листинг программного кода загрузки и поиска дефектов:
\begin{lstlisting}[language=Python]
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('StudentPerformanceFactors/StudentPerformanceFactors.csv')
missing = df.isnull().sum()
print(missing[missing > 0])

plt.figure(figsize=(12, 5))
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
plt.title('Тепловая карта пропущенных значений')
plt.show()
\end{lstlisting}

\subsection*{4.2 Анализ распределений и идентификация выбросов}

Для непрерывных числовых признаков были построены гистограммы распределений с ядерной оценкой плотности (рисунок 4.2) и диаграммы размаха BoxPlot (рисунок 4.3).

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/02_numeric_distributions_before.png}
\caption{Гистограммы распределений числовых признаков до очистки}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/03_numeric_boxplots_before.png}
\caption{Диаграммы размаха (BoxPlot) числовых признаков до устранения выбросов}
\end{figure}

По формуле Тьюки рассчитаны квартильные интервалы и выявлены выбросы (таблица 4.2). В признаке \texttt{Hours\_Studied} обнаружено 43 выброса, в \texttt{Tutoring\_Sessions} --- 430 значений, в целевом показателе \texttt{Exam\_Score} --- 104 выброса (включая ошибочное значение 101 балл).

\begin{table}[H]
\caption{Статистика межквартильного размаха и выбросов}
\centering
\small
\begin{tabular}{|l|c|c|c|c|c|}
\hline
\textbf{Признак} & \textbf{Q1} & \textbf{Q3} & \textbf{IQR} & \textbf{Границы Тьюки} & \textbf{Выбросов} \\
\hline
Hours\_Studied & 16.0 & 24.0 & 8.0 & [4.0, 36.0] & 43 \\
Attendance & 70.0 & 90.0 & 20.0 & [40.0, 120.0] & 0 \\
Sleep\_Hours & 6.0 & 8.0 & 2.0 & [3.0, 11.0] & 0 \\
Previous\_Scores & 63.0 & 88.0 & 25.0 & [25.5, 125.5] & 0 \\
Tutoring\_Sessions & 1.0 & 2.0 & 1.0 & [-0.5, 3.5] & 430 \\
Physical\_Activity & 2.0 & 4.0 & 2.0 & [-1.0, 7.0] & 0 \\
Exam\_Score & 65.0 & 69.0 & 4.0 & [59.0, 75.0] & 104 \\
\hline
\end{tabular}
\end{table}

\subsection*{4.3 Заполнение пропусков и устранение аномальных значений}

Пропуски в качественных признаках заполнены статистической модой: \texttt{Teacher\_Quality} --- «Medium», \texttt{Parental\_Education\_Level} --- «High School», \texttt{Distance\_from\_Home} --- «Near». Выбросы устранены методом винзоризации (clipping) по границам допустимого интервала Тьюки. Контрольные графики подтверждают полное устранение дефектов (рисунки 4.4, 4.5, 4.6).

\begin{figure}[H]
\centering
\includegraphics[width=0.88\textwidth]{plots/04_missing_values_heatmap_after.png}
\caption{Тепловая карта после заполнения пропущенных значений (0 пропусков)}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/05_numeric_boxplots_after.png}
\caption{Диаграммы размаха после устранения выбросов}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/06_numeric_distributions_after.png}
\caption{Гистограммы распределений числовых признаков после очистки}
\end{figure}

Листинг кода импутации и винзоризации:
\begin{lstlisting}[language=Python]
# 1. Заполнение пропусков модой
for col in ['Teacher_Quality', 'Parental_Education_Level', 'Distance_from_Home']:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# 2. Винзоризация выбросов по границам IQR
df_clean['Hours_Studied'] = df_clean['Hours_Studied'].clip(lower=4.0, upper=36.0)
df_clean['Tutoring_Sessions'] = df_clean['Tutoring_Sessions'].clip(lower=0.0, upper=3.5)
df_clean['Exam_Score'] = df_clean['Exam_Score'].clip(lower=59.0, upper=75.0)
\end{lstlisting}

\subsection*{4.4 Конструирование новых признаков (Feature Engineering)}

Сконструированы три новых аналитических признака:
\begin{enumerate}
\item \texttt{Study\_to\_Sleep\_Ratio} $= \text{Hours\_Studied} / \text{Sleep\_Hours}$ --- соотношение времени самостоятельной учебы ко сну;
\item \texttt{Academic\_Effort\_Index} $= (\text{Hours\_Studied} + 1.5 \cdot \text{Tutoring\_Sessions}) \cdot (\text{Attendance} / 100)$ --- комплексный показатель академических усилий;
\item \texttt{Score\_Growth} $= \text{Exam\_Score} - \text{Previous\_Scores}$ --- индивидуальная динамика успеваемости.
\end{enumerate}

Распределения синтезированных признаков приведены на рисунке 4.7.

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/07_new_features_distributions.png}
\caption{Распределения сконструированных признаков}
\end{figure}

Листинг программного кода генерации признаков:
\begin{lstlisting}[language=Python]
df_clean['Study_to_Sleep_Ratio'] = np.round(df_clean['Hours_Studied'] / df_clean['Sleep_Hours'], 3)
df_clean['Academic_Effort_Index'] = np.round((df_clean['Hours_Studied'] + df_clean['Tutoring_Sessions'] * 1.5) * (df_clean['Attendance'] / 100.0), 3)
df_clean['Score_Growth'] = np.round(df_clean['Exam_Score'] - df_clean['Previous_Scores'], 3)
\end{lstlisting}

\subsection*{4.5 Кодирование категориальных признаков}

Пять бинарных признаков (\texttt{Gender}, \texttt{Extracurricular\_Activities}, \texttt{Internet\_Access}, \texttt{Learning\_Disabilities}, \texttt{School\_Type}) преобразованы в индикаторы $\{0, 1\}$. Восемь полиномиальных категорий с тремя уровнями закодированы прямым методом One-Hot Encoding с параметром \texttt{drop\_first=True}. В результате матрица признаков расширена с 23 до 31 столбца.

Листинг кодирования категорий:
\begin{lstlisting}[language=Python]
binary_map = {'Male': 1, 'Female': 0, 'Yes': 1, 'No': 0, 'Public': 1, 'Private': 0}
for col in ['Gender', 'Extracurricular_Activities', 'Internet_Access', 'Learning_Disabilities', 'School_Type']:
    df_clean[col] = df_clean[col].map(binary_map)

df_encoded = pd.get_dummies(df_clean, columns=ohe_cols, drop_first=True, dtype=int)
\end{lstlisting}

\subsection*{4.6 Масштабирование признаков}

Для всех числовых признаков проведено масштабирование методами \texttt{StandardScaler} ($\mu=0, \sigma=1$) и \texttt{MinMaxScaler} ($[0, 1]$). Сравнительные гистограммы исходных и масштабированных шкал представлены на рисунке 4.8.

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{plots/08_scaling_comparison.png}
\caption{Сравнение распределений до и после масштабирования}
\end{figure}

\subsection*{4.7 Корреляционный анализ}

Построена тепловая карта матрицы парных линейных коэффициентов корреляции Пирсона (рисунок 4.9). Зафиксирована сильная прямая корреляция итогового балла \texttt{Exam\_Score} с синтезированным индексом усилий \texttt{Academic\_Effort\_Index} ($r = 0.77$), посещаемостью \texttt{Attendance} ($r = 0.66$), часами учебы \texttt{Hours\_Studied} ($r = 0.50$) и отношением времени учебы ко сну \texttt{Study\_to\_Sleep\_Ratio} ($r = 0.40$).

\begin{figure}[H]
\centering
\includegraphics[width=0.72\textwidth]{plots/09_correlation_matrix_heatmap.png}
\caption{Матрица парных коэффициентов корреляции Пирсона}
\end{figure}

% =========================================================================
% 5 ВЫВОДЫ (цельный связный текст)
% =========================================================================
\section*{5 ВЫВОДЫ}
\addcontentsline{toc}{section}{5 ВЫВОДЫ}

В процессе выполнения лабораторной работы были успешно освоены современные методы и инструментальные средства первичного сбора, разведочного анализа (EDA) и предобработки табличных данных на языке Python с использованием библиотек Pandas, NumPy, Matplotlib, Seaborn и Scikit-Learn. В ходе исследования набора данных StudentPerformanceFactors.csv были детально идентифицированы пропущенные значения в категориальных столбцах Teacher\_Quality, Parental\_Education\_Level и Distance\_from\_Home, успешно устраненные посредством подстановки статистической моды без деформации исходной структуры выборочных распределений.

Применение статистического правила Тьюки на основе межквартильного размаха позволило выявить и скорректировать выбросы в переменных Hours\_Studied, Tutoring\_Sessions и Exam\_Score (включая устранение недопустимого артефакта в 101 балл). Метод винзоризации позволил сохранить исходный объем выборки в 6607 наблюдений, исключив искажение оценок дисперсии. Разработка трех новых содержательных признаков (Study\_to\_Sleep\_Ratio, Academic\_Effort\_Index, Score\_Growth), проведение бинаризации пяти дихотомических признаков и прямого кодирования восьми категорий с параметром drop\_first=True расширили матричное представление датасета до 31 признака. Выполненное масштабирование методами StandardScaler и MinMaxScaler обеспечило полную пригодность подготовленного массива данных для обучения высокоточных метрических, линейных и нейросетевых моделей машинного обучения.

\end{document}
"""
    with open(TEX_PATH, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"LaTeX исходник успешно создан: {TEX_PATH}")

    readme_content = """ИНСТРУКЦИЯ ПО СБОРКЕ И ЗАПУСКУ НА OVERLEAF:
1. Зайдите на сайт https://www.overleaf.com/ и создайте новый проект ("New Project" -> "Blank Project").
2. Загрузите файлы:
   - Файл 'main.tex' в корень проекта.
   - Папку 'plots' со всеми 9 изображениями (01_...png по 09_...png).
3. В меню Overleaf (кнопка 'Menu' в верхнем левом углу):
   - Compiler: выберите 'pdfLaTeX' (или 'XeLaTeX' / 'LuaLaTeX').
4. Нажмите зеленую кнопку 'Recompile'. Отчет скомпилируется строго по стандарту БГУИР СТП 01-2017.
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README для Overleaf успешно создан: {README_PATH}")

if __name__ == "__main__":
    build_latex()
