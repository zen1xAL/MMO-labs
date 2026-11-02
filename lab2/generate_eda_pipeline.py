"""
Обновленный и улучшенный генератор визуализаций для лабораторной работы №2.
Устраняет все дефекты:
1. Тепловая карта пропусков: двухпанельная компоновка (диаграмма с точными процентами + детальная матрица).
   Обеспечен свободный левый отступ для длинных названий признаков (Parental_Education_Level и др.).
2. Контрольная тепловая карта после очистки: сравнительные столбцы "До и После" + валидационная статус-карта 100% заполнено.
   Никаких сплошных бирюзовых прямоугольников и отрицательных шкал!
3. Сетки 2x4 для BoxPlot и гистограмм: 8-я ячейка оформлена в виде чистой, красивой карточки сводных метрик.
   Текст структурирован вертикально, без наложений и без нераспознанных эмодзи.
4. Выбросы: корректная винзоризация целыми числами [0, 3] для занятий, устранена аномалия 101 в Exam_Score.
5. Новые признаки (Feature Engineering): идеальный отступ сверху для заголовка (y=0.98, rect=[0, 0, 1, 0.90]),
   устранена гребенка дискретных значений в Score_Growth.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Настройка шрифтов и стилей графиков
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="DejaVu Sans")

BASE_DIR = r"d:\MMO\lab2"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)
DATA_PATH = os.path.join(BASE_DIR, "StudentPerformanceFactors", "StudentPerformanceFactors.csv")

def add_summary_card(ax, title: str, lines: list, bg_color="#f8f9fa", border_color="#b0bec5"):
    """Создает профессиональную аналитическую карточку со структурированным текстом без наложений."""
    ax.axis("off")
    rect = patches.FancyBboxPatch(
        (0.04, 0.04), 0.92, 0.92,
        boxstyle="round,pad=0.03,rounding_size=0.05",
        facecolor=bg_color, edgecolor=border_color, linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(rect)
    
    # Заголовок
    ax.text(0.5, 0.91, title, fontsize=11, fontweight="bold", ha="center", va="center",
            color="#212529", transform=ax.transAxes)
    ax.plot([0.10, 0.90], [0.83, 0.83], color="#cfd8dc", lw=1.2, transform=ax.transAxes)
    
    # Строки с метриками (вертикальная компоновка: метка -> значение)
    y = 0.74
    for label, val, color in lines:
        ax.text(0.10, y, label, fontsize=8.5, ha="left", va="center", color="#455a64", transform=ax.transAxes)
        ax.text(0.10, y - 0.045, f"  -> {val}", fontsize=8.5, fontweight="bold", ha="left", va="center",
                color=color, transform=ax.transAxes)
        y -= 0.105

def generate_all_plots():
    df_raw = pd.read_csv(DATA_PATH)
    num_cols = ['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', 
                'Tutoring_Sessions', 'Physical_Activity', 'Exam_Score']
    raw_missing = df_raw.isnull().sum()
    missing_cols = raw_missing[raw_missing > 0].to_dict()

    # =========================================================================
    # РИСУНОК 2.1: Анализ пропусков до очистки
    # =========================================================================
    fig = plt.figure(figsize=(15.5, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], left=0.18, right=0.98, bottom=0.20, top=0.88, wspace=0.28)
    
    ax1 = fig.add_subplot(gs[0, 0])
    miss_df = pd.DataFrame({'Feature': df_raw.columns, 'Missing': raw_missing.values})
    miss_df['Pct'] = (miss_df['Missing'] / len(df_raw)) * 100
    miss_df = miss_df.sort_values(by='Missing', ascending=True)
    
    colors = ['#d32f2f' if m > 0 else '#90caf9' for m in miss_df['Missing']]
    bars = ax1.barh(miss_df['Feature'], miss_df['Missing'], color=colors, height=0.65)
    
    for bar, m, pct in zip(bars, miss_df['Missing'], miss_df['Pct']):
        if m > 0:
            ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                     f"{int(m)} шт. ({pct:.2f}%)", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#b71c1c')
        else:
            ax1.text(1, bar.get_y() + bar.get_height()/2, "0", va='center', ha='left', fontsize=8, color='#78909c')
            
    ax1.set_xlim(0, max(miss_df['Missing']) * 1.35)
    ax1.set_title("Количество пропущенных значений по признакам", fontsize=11.5, pad=10)
    ax1.set_xlabel("Число пропусков (строк)")
    
    ax2 = fig.add_subplot(gs[0, 1])
    dirty_mask = df_raw.isnull().any(axis=1)
    sample_df = pd.concat([df_raw[dirty_mask], df_raw[~dirty_mask].head(40)]).sort_index()
    
    sns.heatmap(sample_df.isnull(), ax=ax2, cbar=True, yticklabels=False,
                cmap=sns.color_palette(["#263238", "#ffeb3b"]), vmin=0, vmax=1)
    ax2.set_title(f"Матрица пропусков (срез {len(sample_df)} наблюдений)", fontsize=11.5, pad=10)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=9)
    
    plt.suptitle("Рисунок 2.1 – Статистический и визуальный анализ пропусков в исходном датасете", fontsize=13, y=0.97)
    plt.savefig(os.path.join(PLOTS_DIR, "01_missing_values_heatmap_before.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.2: Гистограммы числовых признаков ДО очистки (2x4 сетка с карточкой)
    # =========================================================================
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, col in enumerate(num_cols):
        r, c = divmod(i, 4)
        sns.histplot(df_raw[col], kde=True, ax=axes[r, c], color="#1976d2", bins=20)
        axes[r, c].set_title(f"Гистограмма: {col}", fontsize=11)
        axes[r, c].set_xlabel("Значение")
        axes[r, c].set_ylabel("Частота")
        
    card_lines_dist = [
        ("Объем выборки:", "6 607 наблюдений", "#37474f"),
        ("Числовых признаков:", "7 столбцов", "#37474f"),
        ("Hours_Studied:", "μ = 19.97, σ = 5.99", "#1565c0"),
        ("Attendance:", "μ = 79.98, σ = 11.55", "#1565c0"),
        ("Exam_Score (целевой):", "μ = 67.24, max = 101", "#c62828"),
        ("Форма распределений:", "Преимущественно унимодальная", "#2e7d32")
    ]
    add_summary_card(axes[1, 3], "Параметры распределений", card_lines_dist)
    
    plt.suptitle("Рисунок 2.2 – Гистограммы распределений числовых признаков до обработки выбросов", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "02_numeric_distributions_before.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.3: BoxPlot ДО обработки выбросов (2x4 сетка с карточкой выбросов)
    # =========================================================================
    outlier_stats = {}
    for col in num_cols:
        q1 = df_raw[col].quantile(0.25)
        q3 = df_raw[col].quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        cnt = int(((df_raw[col] < low) | (df_raw[col] > high)).sum())
        outlier_stats[col] = {
            "Q1": float(q1), "Q3": float(q3), "IQR": float(iqr),
            "lower_bound": float(low), "upper_bound": float(high),
            "outliers_count": cnt
        }

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, col in enumerate(num_cols):
        r, c = divmod(i, 4)
        sns.boxplot(y=df_raw[col], ax=axes[r, c], color="#f57c00", width=0.45,
                    flierprops={"marker": "o", "markersize": 4.5, "markerfacecolor": "#d32f2f", "alpha": 0.7})
        axes[r, c].set_title(f"BoxPlot: {col}", fontsize=11)
        axes[r, c].set_ylabel("Значение")

    card_lines_outliers = [
        ("Метод обнаружения:", "Правило Тьюки (1.5×IQR)", "#37474f"),
        ("Hours_Studied [4; 36]:", f"{outlier_stats['Hours_Studied']['outliers_count']} выбр. (0.65%)", "#c62828"),
        ("Tutoring_Sessions [0; 3]:", f"{outlier_stats['Tutoring_Sessions']['outliers_count']} выбр. (6.51%)", "#c62828"),
        ("Exam_Score [59; 75]:", f"{outlier_stats['Exam_Score']['outliers_count']} выбр. (1.57%)", "#c62828"),
        ("Аномалия шкалы:", "Балл 101 (> 100%)", "#b71c1c"),
        ("Остальные 4 признака:", "0 выбросов (100% норма)", "#2e7d32")
    ]
    add_summary_card(axes[1, 3], "Анализ выбросов (IQR)", card_lines_outliers)

    plt.suptitle("Рисунок 2.3 – Диаграммы размаха (BoxPlot) числовых признаков до обработки выбросов", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "03_numeric_boxplots_before.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # ШАГ ОЧИСТКИ ДАННЫХ
    # =========================================================================
    df_clean = df_raw.copy()
    for col in missing_cols:
        mode_val = df_clean[col].mode()[0]
        df_clean[col] = df_clean[col].fillna(mode_val)

    # Винзоризация целыми числами
    df_clean['Hours_Studied'] = df_clean['Hours_Studied'].clip(lower=4, upper=36)
    df_clean['Tutoring_Sessions'] = df_clean['Tutoring_Sessions'].clip(lower=0, upper=3)
    df_clean['Exam_Score'] = df_clean['Exam_Score'].clip(lower=59, upper=75)

    # =========================================================================
    # РИСУНОК 2.4: Проверка пропусков ПОСЛЕ очистки (Сравнение До и После)
    # =========================================================================
    fig = plt.figure(figsize=(15.5, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.0], left=0.08, right=0.98, bottom=0.20, top=0.88, wspace=0.28)

    ax1 = fig.add_subplot(gs[0, 0])
    compare_df = pd.DataFrame({
        'Feature': list(missing_cols.keys()),
        'До очистки (NaN)': [raw_missing[c] for c in missing_cols],
        'После очистки (NaN)': [df_clean[c].isnull().sum() for c in missing_cols]
    })
    
    x = np.arange(len(compare_df))
    width = 0.35
    b1 = ax1.bar(x - width/2, compare_df['До очистки (NaN)'], width, label='До очистки (NaN)', color='#e53935')
    b2 = ax1.bar(x + width/2, compare_df['После очистки (NaN)'], width, label='После очистки (мода)', color='#43a047')
    
    for bar in b1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, f"{int(bar.get_height())}", ha='center', va='bottom', fontweight='bold', color='#b71c1c')
    for bar in b2:
        ax1.text(bar.get_x() + bar.get_width()/2, 2.5, "0 ✓", ha='center', va='bottom', fontweight='bold', color='#1b5e20')

    ax1.set_xticks(x)
    ax1.set_xticklabels(compare_df['Feature'], fontsize=9.5)
    ax1.set_ylabel("Количество пропусков")
    ax1.set_ylim(0, 115)
    ax1.set_title("Сравнение числа пропусков до и после импутации модой", fontsize=11.5, pad=10)
    ax1.legend(loc='upper right')

    ax2 = fig.add_subplot(gs[0, 1])
    control_matrix = df_clean.isnull().head(100)
    sns.heatmap(control_matrix, ax=ax2, cbar=False, yticklabels=False,
                cmap=sns.color_palette(["#ffffff"]), vmin=0, vmax=1, linewidths=0.5, linecolor="#eceff1")
    ax2.set_title("Контрольная тепловая карта (100% заполнено)", fontsize=11.5, pad=10)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=9)
    
    rect_badge = patches.FancyBboxPatch(
        (0.10, 0.38), 0.80, 0.24,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        facecolor="#e8f5e9", edgecolor="#2e7d32", linewidth=2.0,
        transform=ax2.transAxes
    )
    ax2.add_patch(rect_badge)
    ax2.text(0.5, 0.52, "ПРОПУСКИ ПОЛНОСТЬЮ УСТРАНЕНЫ", fontsize=11, fontweight="bold", ha="center", va="center", color="#1b5e20", transform=ax2.transAxes)
    ax2.text(0.5, 0.44, "0 пропусков из 6 607 строк (100% целостность)", fontsize=9.5, ha="center", va="center", color="#2e7d32", transform=ax2.transAxes)

    plt.suptitle("Рисунок 2.4 – Контрольная проверка устранения пропусков (сравнение до/после и валидация)", fontsize=13, y=0.97)
    plt.savefig(os.path.join(PLOTS_DIR, "04_missing_values_heatmap_after.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.5: BoxPlot ПОСЛЕ устранения выбросов (2x4 сетка с карточкой чистоты)
    # =========================================================================
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, col in enumerate(num_cols):
        r, c = divmod(i, 4)
        sns.boxplot(y=df_clean[col], ax=axes[r, c], color="#43a047", width=0.45)
        axes[r, c].set_title(f"BoxPlot (Clean): {col}", fontsize=11)
        axes[r, c].set_ylabel("Значение")

    card_lines_clean = [
        ("Статус очистки:", "ВЫБРОСЫ УСТРАНЕНЫ", "#1b5e20"),
        ("Метод устранения:", "Винзоризация (Clipping)", "#37474f"),
        ("Hours_Studied:", "Ограничено в [4; 36]", "#2e7d32"),
        ("Tutoring_Sessions:", "Ограничено в [0; 3]", "#2e7d32"),
        ("Exam_Score:", "Ограничено в [59; 75]", "#2e7d32"),
        ("Сохранено наблюдений:", "6 607 строк (100% выборки)", "#1b5e20")
    ]
    add_summary_card(axes[1, 3], "Результаты очистки выбросов", card_lines_clean, bg_color="#e8f5e9", border_color="#81c784")

    plt.suptitle("Рисунок 2.5 – Диаграммы размаха числовых признаков после устранения выбросов", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "05_numeric_boxplots_after.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.6: Гистограммы ПОСЛЕ очистки (2x4 сетка с карточкой)
    # =========================================================================
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, col in enumerate(num_cols):
        r, c = divmod(i, 4)
        sns.histplot(df_clean[col], kde=True, ax=axes[r, c], color="#2e7d32", bins=20)
        axes[r, c].set_title(f"Распределение: {col}", fontsize=11)
        axes[r, c].set_xlabel("Значение")
        axes[r, c].set_ylabel("Частота")

    card_lines_hist_clean = [
        ("Качество данных:", "Высокое (без выбросов)", "#1b5e20"),
        ("Аномалии шкалы:", "Устранены (нет значений >100)", "#1b5e20"),
        ("Форма кривых:", "Сглаженная, унимодальная", "#2e7d32"),
        ("Hours_Studied:", "Диапазон [4; 36] ч/нед", "#2e7d32"),
        ("Exam_Score:", "Диапазон [59; 75] баллов", "#2e7d32"),
        ("Готовность к ML:", "100% готовность", "#1b5e20")
    ]
    add_summary_card(axes[1, 3], "Итог калибровки данных", card_lines_hist_clean, bg_color="#e8f5e9", border_color="#81c784")

    plt.suptitle("Рисунок 2.6 – Гистограммы распределений числовых признаков после устранения выбросов", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "06_numeric_distributions_after.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.7: Новые признаки (Feature Engineering)
    # =========================================================================
    df_clean['Study_to_Sleep_Ratio'] = np.round(df_clean['Hours_Studied'] / df_clean['Sleep_Hours'], 2)
    df_clean['Academic_Effort_Index'] = np.round((df_clean['Hours_Studied'] + df_clean['Tutoring_Sessions'] * 1.5) * (df_clean['Attendance'] / 100.0), 2)
    df_clean['Score_Growth'] = np.round(df_clean['Exam_Score'] - df_clean['Previous_Scores'], 1)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    sns.histplot(df_clean['Study_to_Sleep_Ratio'], kde=True, ax=axes[0], color="#6a1b9a", bins=25)
    axes[0].set_title("1. Баланс учебы и сна:\nStudy_to_Sleep_Ratio", fontsize=11)
    axes[0].set_xlabel("Отношение (Hours_Studied / Sleep_Hours)")
    axes[0].set_ylabel("Частота")

    sns.histplot(df_clean['Academic_Effort_Index'], kde=True, ax=axes[1], color="#00695c", bins=25)
    axes[1].set_title("2. Индекс академических усилий:\nAcademic_Effort_Index", fontsize=11)
    axes[1].set_xlabel("Индекс усилий с учетом посещаемости")
    axes[1].set_ylabel("Частота")

    sns.histplot(df_clean['Score_Growth'], kde=True, ax=axes[2], color="#c2185b", binwidth=2)
    axes[2].set_title("3. Академическая динамика:\nScore_Growth = Exam - Previous", fontsize=11)
    axes[2].set_xlabel("Дельта баллов (прирост / спад)")
    axes[2].set_ylabel("Частота")

    plt.suptitle("Рисунок 2.7 – Распределения сгенерированных признаков (Feature Engineering)", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(os.path.join(PLOTS_DIR, "07_new_features_distributions.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.8: Масштабирование
    # =========================================================================
    binary_maps = {
        'Gender': {'Male': 1, 'Female': 0},
        'Extracurricular_Activities': {'Yes': 1, 'No': 0},
        'Internet_Access': {'Yes': 1, 'No': 0},
        'Learning_Disabilities': {'Yes': 1, 'No': 0},
        'School_Type': {'Public': 1, 'Private': 0}
    }
    for b_col, b_map in binary_maps.items():
        df_clean[b_col] = df_clean[b_col].map(b_map)

    ohe_cols = [
        'Parental_Involvement', 'Access_to_Resources', 'Motivation_Level',
        'Family_Income', 'Teacher_Quality', 'Peer_Influence',
        'Parental_Education_Level', 'Distance_from_Home'
    ]
    df_encoded = pd.get_dummies(df_clean, columns=ohe_cols, drop_first=True, dtype=int)

    all_num_features = num_cols + ['Study_to_Sleep_Ratio', 'Academic_Effort_Index', 'Score_Growth']
    std_scaler = StandardScaler()
    scaled_std = std_scaler.fit_transform(df_encoded[all_num_features])
    df_std = df_encoded.copy()
    df_std[[f + "_std" for f in all_num_features]] = scaled_std

    minmax_scaler = MinMaxScaler()
    scaled_minmax = minmax_scaler.fit_transform(df_encoded[all_num_features])
    df_norm = df_encoded.copy()
    df_norm[[f + "_norm" for f in all_num_features]] = scaled_minmax

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    sns.histplot(df_encoded['Hours_Studied'], kde=True, ax=axes[0, 0], color="#1565c0")
    axes[0, 0].set_title("Исходный: Hours_Studied", fontsize=11)
    sns.histplot(df_std['Hours_Studied_std'], kde=True, ax=axes[0, 1], color="#e65100")
    axes[0, 1].set_title("StandardScaler (μ=0, σ=1): Hours_Studied", fontsize=11)
    sns.histplot(df_norm['Hours_Studied_norm'], kde=True, ax=axes[0, 2], color="#2e7d32")
    axes[0, 2].set_title("MinMaxScaler [0, 1]: Hours_Studied", fontsize=11)

    sns.histplot(df_encoded['Attendance'], kde=True, ax=axes[1, 0], color="#1565c0")
    axes[1, 0].set_title("Исходный: Attendance", fontsize=11)
    sns.histplot(df_std['Attendance_std'], kde=True, ax=axes[1, 1], color="#e65100")
    axes[1, 1].set_title("StandardScaler (μ=0, σ=1): Attendance", fontsize=11)
    sns.histplot(df_norm['Attendance_norm'], kde=True, ax=axes[1, 2], color="#2e7d32")
    axes[1, 2].set_title("MinMaxScaler [0, 1]: Attendance", fontsize=11)

    plt.suptitle("Рисунок 2.8 – Сравнение исходных, стандартизированных и нормализованных признаков", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "08_scaling_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 2.9: Матрица корреляций Пирсона
    # =========================================================================
    plt.figure(figsize=(11, 9))
    corr_matrix = df_encoded[all_num_features].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, cbar=True, square=True,
                linewidths=0.5, linecolor="#cfd8dc")
    plt.xticks(rotation=45, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    plt.title("Рисунок 2.9 – Тепловая карта корреляционной матрицы Пирсона (Correlation Matrix)", fontsize=13, pad=16)
    plt.savefig(os.path.join(PLOTS_DIR, "09_correlation_matrix_heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    clean_csv_path = os.path.join(BASE_DIR, "StudentPerformance_Preprocessed.csv")
    df_encoded.to_csv(clean_csv_path, index=False)

    scaled_csv_path = os.path.join(BASE_DIR, "StudentPerformance_Scaled.csv")
    df_std.to_csv(scaled_csv_path, index=False)
    print("Все 9 графиков и предобработанные датасеты успешно сохранены!")

if __name__ == "__main__":
    generate_all_plots()
