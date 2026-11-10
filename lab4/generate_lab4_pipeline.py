"""
Полный модульный пайплайн для Лабораторной работы №4 по курсу «Методы машинного обучения».
Тема: «Бинарная классификация данных (Логистическая регрессия, SVM, CART)».
Студент: Власовец А. И., гр. 351002 (Вариант 7).
Преподаватель: Лебедевич А. В.
Датасет: Bank Loan Defaulter (Bankloan.csv) — задача кредитного скоринга заемщиков.
"""

import warnings
warnings.filterwarnings("ignore")

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, average_precision_score,
    confusion_matrix, classification_report
)

# Настройка шрифтов и стилей графиков
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="DejaVu Sans")

BASE_DIR = r"d:\MMO\lab4"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
DATA_DIR = os.path.join(BASE_DIR, "data")
LATEX_PLOTS_DIR = os.path.join(BASE_DIR, "latex", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LATEX_PLOTS_DIR, exist_ok=True)

def add_summary_card(ax, title: str, lines: list, bg_color="#f8f9fa", border_color="#b0bec5"):
    """Создает профессиональную аналитическую карточку параметров."""
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
    
    # Строки метрик
    y = 0.74
    for label, val, color in lines:
        ax.text(0.10, y, label, fontsize=8.8, ha="left", va="center", color="#455a64", transform=ax.transAxes)
        ax.text(0.10, y - 0.05, f"  -> {val}", fontsize=9.0, fontweight="bold", ha="left", va="center",
                color=color, transform=ax.transAxes)
        y -= 0.12

def run_pipeline():
    print("=" * 70)
    print("ЗАПУСК КОНВЕЙЕРА ЛАБОРАТОРНОЙ РАБОТЫ №4 (БИНАРНАЯ КЛАССИФИКАЦИЯ)")
    print("=" * 70)

    # 1. Загрузка исходных данных
    raw_path = os.path.join(DATA_DIR, "Bankloan_raw.csv")
    df_raw = pd.read_csv(raw_path)
    print(f"Исходный датасет загружен: {df_raw.shape[0]} строк, {df_raw.shape[1]} столбцов.")

    feature_cols = ['age', 'ed', 'employ', 'address', 'income', 'debtinc', 'creddebt', 'othdebt']
    target_col = 'default'

    # Разделение на размеченные исторические данные и неразмеченные для скоринга
    df_labeled = df_raw.dropna(subset=[target_col]).copy()
    df_labeled[target_col] = df_labeled[target_col].astype(int)
    
    df_unlabeled = df_raw[df_raw[target_col].isnull()].copy()
    df_unlabeled = df_unlabeled.drop(columns=[target_col])

    # Сохраняем очищенный датасет
    clean_path = os.path.join(DATA_DIR, "Bankloan_clean.csv")
    df_labeled.to_csv(clean_path, index=False)
    
    unlabeled_path = os.path.join(DATA_DIR, "Bankloan_unlabeled_scoring.csv")
    df_unlabeled.to_csv(unlabeled_path, index=False)

    print(f"Размеченная выборка для обучения и валидации: {len(df_labeled)} клиентов (0: {(df_labeled[target_col]==0).sum()}, 1: {(df_labeled[target_col]==1).sum()}).")
    print(f"Неразмеченная выборка соискателей для скоринга: {len(df_unlabeled)} заявок.")

    # 2. Анализ выбросов по методу Тьюки (1.5 x IQR)
    outlier_stats = {}
    for col in feature_cols:
        q1 = df_labeled[col].quantile(0.25)
        q3 = df_labeled[col].quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        cnt = int(((df_labeled[col] < low) | (df_labeled[col] > high)).sum())
        outlier_stats[col] = {
            "Q1": float(q1), "Q3": float(q3), "IQR": float(iqr),
            "lower_bound": float(low), "upper_bound": float(high),
            "outliers_count": cnt
        }

    # 3. Разбиение на обучающую и тестовую выборки (80 / 20) со стратификацией
    X = df_labeled[feature_cols]
    y = df_labeled[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"Train выборка: {X_train.shape[0]} строк | Test выборка: {X_test.shape[0]} строк.")

    # 4. Стандартизация признаков (StandardScaler)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_unlabeled_scaled = scaler.transform(df_unlabeled[feature_cols])

    # Сохраняем масштабированные данные
    df_train_scaled = pd.DataFrame(X_train_scaled, columns=feature_cols)
    df_train_scaled[target_col] = y_train.values
    df_train_scaled.to_csv(os.path.join(DATA_DIR, "Bankloan_train_scaled.csv"), index=False)

    df_test_scaled = pd.DataFrame(X_test_scaled, columns=feature_cols)
    df_test_scaled[target_col] = y_test.values
    df_test_scaled.to_csv(os.path.join(DATA_DIR, "Bankloan_test_scaled.csv"), index=False)

    # =========================================================================
    # РИСУНОК 4.1: Структура датасета, пропуски и баланс классов
    # =========================================================================
    fig = plt.figure(figsize=(16, 5.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.0, 1.0], wspace=0.25)

    # Панель 1: Баланс классов
    ax1 = fig.add_subplot(gs[0, 0])
    counts = df_labeled[target_col].value_counts().sort_index()
    labels = ["0 – Выплачен (73.9%)", "1 – Дефолт (26.1%)"]
    bar_colors = ["#2e7d32", "#c62828"]
    bars = ax1.bar(labels, counts.values, color=bar_colors, width=0.55, edgecolor="black", lw=1)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f"{int(bar.get_height())} чел.", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.set_title("1. Распределение целевого признака default", fontsize=11.5, pad=10)
    ax1.set_ylabel("Количество заемщиков")
    ax1.set_ylim(0, max(counts.values) * 1.18)

    # Панель 2: Структура выборок (размеченные vs соискатели)
    ax2 = fig.add_subplot(gs[0, 1])
    sample_types = ["Исторические клиенты\n(Размечено 700)", "Новые соискатели\n(Скоринг 450)"]
    sample_sizes = [len(df_labeled), len(df_unlabeled)]
    bars_s = ax2.bar(sample_types, sample_sizes, color=["#1565c0", "#f57c00"], width=0.55, edgecolor="black", lw=1)
    for bar in bars_s:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f"{int(bar.get_height())} шт. ({bar.get_height()/len(df_raw)*100:.1f}%)",
                 ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax2.set_title("2. Соотношение выборок в базе банка", fontsize=11.5, pad=10)
    ax2.set_ylabel("Количество анкет")
    ax2.set_ylim(0, max(sample_sizes) * 1.18)

    # Панель 3: Карточка характеристик датасета
    card_data = [
        ("Всего записей в базе:", f"{len(df_raw)} анкет заемщиков", "#37474f"),
        ("Обучающая выборка:", "700 клиентов (100% размечено)", "#1565c0"),
        ("Выплатили кредит (Класс 0):", "517 заемщиков (73.86%)", "#2e7d32"),
        ("Допустили дефолт (Класс 1):", "183 заемщика (26.14%)", "#c62828"),
        ("Предиктивных признаков:", "8 числовых финансовых факторов", "#37474f"),
        ("Кредитные соискатели:", "450 анкет без метки (Inference)", "#e65100")
    ]
    add_summary_card(fig.add_subplot(gs[0, 2]), "Параметры кредитного датасета", card_data)

    plt.suptitle("Рисунок 4.1 – Структура базы данных заемщиков, распределение целевого класса и аудит выборок", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "01_dataset_and_missing_analysis.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.2: Распределения числовых признаков и анализ выбросов
    # =========================================================================
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, col in enumerate(feature_cols):
        r, c = divmod(i, 4)
        sns.histplot(df_labeled[col], kde=True, ax=axes[r, c], color="#1976d2", bins=22)
        axes[r, c].set_title(f"Гистограмма: {col}", fontsize=11)
        axes[r, c].set_xlabel(f"Значение {col}")
        axes[r, c].set_ylabel("Частота")

    plt.suptitle("Рисунок 4.2 – Гистограммы распределений финансовых признаков с ядерной оценкой плотности (KDE)", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(os.path.join(PLOTS_DIR, "02_features_distributions_and_boxplots.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.3: Корреляционная матрица Пирсона и диаграммы размаха (BoxPlots)
    # =========================================================================
    fig = plt.figure(figsize=(16, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.0], wspace=0.25)

    # Тепловая карта корреляции
    ax_corr = fig.add_subplot(gs[0, 0])
    corr_matrix = df_labeled[feature_cols + [target_col]].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, cbar=True,
                square=True, linewidths=0.5, linecolor="#cfd8dc", ax=ax_corr)
    ax_corr.set_title("1. Корреляционная матрица Пирсона признаков и default", fontsize=11.5, pad=10)
    ax_corr.set_xticklabels(ax_corr.get_xticklabels(), rotation=45, ha='right', fontsize=9.5)

    # Сравнение ключевых признаков по классам
    ax_box = fig.add_subplot(gs[0, 1])
    df_box = df_labeled.copy()
    sns.boxplot(x="default", y="debtinc", data=df_box, hue="default", palette=["#2e7d32", "#c62828"], ax=ax_box, width=0.45, legend=False)
    ax_box.set_title("2. Отношение долга к доходу (debtinc) по классам", fontsize=11.5, pad=10)
    ax_box.set_xticks([0, 1])
    ax_box.set_xticklabels(["0 – Платежеспособный", "1 – Дефолтный"], fontsize=10)
    ax_box.set_ylabel("Коэффициент долговой нагрузки (debtinc, %)")

    plt.suptitle("Рисунок 4.3 – Линейные взаимосвязи признаков и разделение долговой нагрузки по классам заемщиков", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "03_outliers_and_correlation_heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # ОБУЧЕНИЕ МОДЕЛЕЙ БИНАРНОЙ КЛАССИФИКАЦИИ
    # =========================================================================
    print("\nОбучение классификаторов...")

    # 1. Логистическая регрессия
    lr_model = LogisticRegression(C=1.0, penalty='l2', solver='lbfgs', max_iter=1000, random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr = lr_model.predict(X_test_scaled)
    y_prob_lr = lr_model.predict_proba(X_test_scaled)[:, 1]

    # 2. Метод опорных векторов (SVM) - линейное и RBF ядра
    svm_linear = SVC(kernel='linear', C=1.0, probability=True, random_state=42)
    svm_linear.fit(X_train_scaled, y_train)
    y_pred_svm_lin = svm_linear.predict(X_test_scaled)
    y_prob_svm_lin = svm_linear.predict_proba(X_test_scaled)[:, 1]

    svm_rbf = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
    svm_rbf.fit(X_train_scaled, y_train)
    y_pred_svm_rbf = svm_rbf.predict(X_test_scaled)
    y_prob_svm_rbf = svm_rbf.predict_proba(X_test_scaled)[:, 1]

    # 3. Дерево решений (CART)
    cart_model = DecisionTreeClassifier(criterion='gini', max_depth=4, min_samples_split=10, min_samples_leaf=5, random_state=42)
    cart_model.fit(X_train_scaled, y_train)
    y_pred_cart = cart_model.predict(X_test_scaled)
    y_prob_cart = cart_model.predict_proba(X_test_scaled)[:, 1]

    # Сбор метрик моделей
    model_preds = {
        "Logistic Regression": (y_pred_lr, y_prob_lr, lr_model),
        "SVM (Linear Kernel)": (y_pred_svm_lin, y_prob_svm_lin, svm_linear),
        "SVM (RBF Kernel)": (y_pred_svm_rbf, y_prob_svm_rbf, svm_rbf),
        "CART (Decision Tree)": (y_pred_cart, y_prob_cart, cart_model)
    }

    metrics_table = {}
    for name, (pred, prob, mdl) in model_preds.items():
        acc = accuracy_score(y_test, pred)
        prec = precision_score(y_test, pred)
        rec = recall_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        auc = roc_auc_score(y_test, prob)
        cm = confusion_matrix(y_test, pred)
        metrics_table[name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1": float(f1),
            "roc_auc": float(auc),
            "confusion_matrix": cm.tolist()
        }
        print(f"[{name}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")

    # =========================================================================
    # РИСУНОК 4.4: Анализ Логистической регрессии (Log-Odds веса и Odds Ratios)
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.5))
    
    # Веса логистической регрессии
    lr_weights = pd.Series(lr_model.coef_[0], index=feature_cols).sort_values()
    bar_colors_lr = ["#c62828" if w > 0 else "#2e7d32" for w in lr_weights.values]
    axes[0].barh(lr_weights.index, lr_weights.values, color=bar_colors_lr, height=0.6)
    for i, v in enumerate(lr_weights.values):
        axes[0].text(v + (0.03 if v >= 0 else -0.08), i, f"{v:+.3f}", va="center", fontsize=9.5, fontweight="bold")
    axes[0].set_title("1. Веса признаков w (Log-Odds) в модели Logit", fontsize=11.5, pad=10)
    axes[0].set_xlabel("Значение весового коэффициента w")
    axes[0].axvline(0, color="black", linestyle="--", lw=1)

    # Отношение шансов (Odds Ratios: exp(w))
    odds_ratios = np.exp(lr_weights)
    axes[1].barh(odds_ratios.index, odds_ratios.values, color="#1565c0", height=0.6)
    for i, v in enumerate(odds_ratios.values):
        axes[1].text(v + 0.03, i, f"{v:.2f}x", va="center", fontsize=9.5, fontweight="bold")
    axes[1].set_title("2. Отношение шансов дефолта: OR = exp(w)", fontsize=11.5, pad=10)
    axes[1].set_xlabel("Множитель шансов дефолта при росте признака на 1σ")
    axes[1].axvline(1, color="red", linestyle="--", lw=1.2, label="Нейтральный порог OR = 1.0")
    axes[1].legend(loc="lower right")

    plt.suptitle("Рисунок 4.4 – Интерпретация модели логистической регрессии: логистические веса и отношение шансов дефолта", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "04_logistic_regression_analysis.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.5: SVM Разделяющие границы в 2D проекции
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.5))
    
    # Обучим 2D модели на двух самых информативных признаках: employ и debtinc
    idx1, idx2 = feature_cols.index('employ'), feature_cols.index('debtinc')
    X_train_2d = X_train_scaled[:, [idx1, idx2]]
    X_test_2d = X_test_scaled[:, [idx1, idx2]]

    svm_lin_2d = SVC(kernel='linear', C=1.0).fit(X_train_2d, y_train)
    svm_rbf_2d = SVC(kernel='rbf', C=1.0, gamma='scale').fit(X_train_2d, y_train)

    # Сетка для изолиний
    x_min, x_max = X_train_2d[:, 0].min() - 0.5, X_train_2d[:, 0].max() + 0.5
    y_min, y_max = X_train_2d[:, 1].min() - 0.5, X_train_2d[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))

    # Линейный SVM
    Z_lin = svm_lin_2d.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    axes[0].contourf(xx, yy, Z_lin, alpha=0.25, cmap=plt.cm.coolwarm)
    scatter0 = axes[0].scatter(X_test_2d[y_test == 0, 0], X_test_2d[y_test == 0, 1],
                               color="#2e7d32", label="0 – Платежеспособный", alpha=0.7, s=35, edgecolors='none')
    scatter1 = axes[0].scatter(X_test_2d[y_test == 1, 0], X_test_2d[y_test == 1, 1],
                               color="#c62828", label="1 – Дефолт", alpha=0.8, s=40, edgecolors='black', marker='^')
    # Отметим опорные векторы
    axes[0].scatter(svm_lin_2d.support_vectors_[:, 0], svm_lin_2d.support_vectors_[:, 1],
                    s=70, facecolors='none', edgecolors='black', lw=1.2, label=f"Опорные векторы ({len(svm_lin_2d.support_vectors_)})")
    axes[0].set_title("1. Linear SVM: плоская разделяющая гиперплоскость", fontsize=11.5)
    axes[0].set_xlabel("Стаж работы (employ, standardized)")
    axes[0].set_ylabel("Отношение долга к доходу (debtinc, standardized)")
    axes[0].legend(loc="upper right", fontsize=8.5)

    # RBF SVM
    Z_rbf = svm_rbf_2d.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    axes[1].contourf(xx, yy, Z_rbf, alpha=0.25, cmap=plt.cm.coolwarm)
    axes[1].scatter(X_test_2d[y_test == 0, 0], X_test_2d[y_test == 0, 1],
                    color="#2e7d32", label="0 – Платежеспособный", alpha=0.7, s=35, edgecolors='none')
    axes[1].scatter(X_test_2d[y_test == 1, 0], X_test_2d[y_test == 1, 1],
                    color="#c62828", label="1 – Дефолт", alpha=0.8, s=40, edgecolors='black', marker='^')
    axes[1].scatter(svm_rbf_2d.support_vectors_[:, 0], svm_rbf_2d.support_vectors_[:, 1],
                    s=70, facecolors='none', edgecolors='black', lw=1.2, label=f"Опорные векторы ({len(svm_rbf_2d.support_vectors_)})")
    axes[1].set_title("2. RBF SVM: нелинейная искривленная разделяющая граница", fontsize=11.5)
    axes[1].set_xlabel("Стаж работы (employ, standardized)")
    axes[1].set_ylabel("Отношение долга к доходу (debtinc, standardized)")
    axes[1].legend(loc="upper right", fontsize=8.5)

    plt.suptitle("Рисунок 4.5 – Разделяющие границы решений и опорные векторы метода SVM (Linear vs RBF ядра)", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "05_svm_decision_boundary_and_margins.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.6: Визуализация дерева решений CART
    # =========================================================================
    fig, ax = plt.subplots(figsize=(18, 9))
    plot_tree(
        cart_model,
        feature_names=feature_cols,
        class_names=["Выплатит (0)", "Дефолт (1)"],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax
    )
    plt.title("Рисунок 4.6 – Структура дерева решений CART (глубина max_depth = 4, критерий Gini)", fontsize=13, pad=16)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "06_cart_decision_tree_visualization.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.7: Матрицы ошибок (Confusion Matrices)
    # =========================================================================
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
    cm_names = list(model_preds.keys())

    for idx, name in enumerate(cm_names):
        cm = metrics_table[name]["confusion_matrix"]
        cm_arr = np.array(cm)
        sns.heatmap(cm_arr, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[idx],
                    annot_kws={"fontsize": 13, "fontweight": "bold"})
        axes[idx].set_title(f"{name}\nAcc: {metrics_table[name]['accuracy']*100:.1f}% | F1: {metrics_table[name]['f1']:.3f}", fontsize=10.5)
        axes[idx].set_xlabel("Предсказанный класс (Predicted)")
        axes[idx].set_ylabel("Истинный класс (Actual)" if idx == 0 else "")
        axes[idx].set_xticklabels(["0 (Плат.)", "1 (Дефолт)"], fontsize=9.5)
        axes[idx].set_yticklabels(["0 (Плат.)", "1 (Дефолт)"], fontsize=9.5)

    plt.suptitle("Рисунок 4.7 – Сопоставление матриц ошибок (Confusion Matrices) исследуемых алгоритмов классификации", fontsize=13, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(os.path.join(PLOTS_DIR, "07_confusion_matrices_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.8: ROC и Precision-Recall кривые
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6))

    colors_models = ["#1565c0", "#2e7d32", "#7b1fa2", "#e65100"]

    # Панель 1: ROC-кривые
    for idx, (name, (pred, prob, mdl)) in enumerate(model_preds.items()):
        fpr, tpr, _ = roc_curve(y_test, prob)
        auc_val = metrics_table[name]["roc_auc"]
        axes[0].plot(fpr, tpr, color=colors_models[idx], lw=2.2,
                     label=f"{name} (AUC = {auc_val:.3f})")

    axes[0].plot([0, 1], [0, 1], color="gray", linestyle="--", lw=1.2, label="Случайное гадание (AUC = 0.500)")
    axes[0].set_title("1. ROC-кривые (Receiver Operating Characteristic)", fontsize=11.5, pad=10)
    axes[0].set_xlabel("Ложноположительная доля (FPR = FP / (FP + TN))")
    axes[0].set_ylabel("Истинноположительная доля (TPR = Recall = TP / (TP + FN))")
    axes[0].legend(loc="lower right", fontsize=9.5)

    # Панель 2: Precision-Recall кривые
    baseline_pr = (y_test == 1).sum() / len(y_test)
    for idx, (name, (pred, prob, mdl)) in enumerate(model_preds.items()):
        prec_curve, rec_curve, _ = precision_recall_curve(y_test, prob)
        ap_val = average_precision_score(y_test, prob)
        axes[1].plot(rec_curve, prec_curve, color=colors_models[idx], lw=2.2,
                     label=f"{name} (PR-AUC = {ap_val:.3f})")

    axes[1].axhline(baseline_pr, color="gray", linestyle="--", lw=1.2, label=f"Базовый уровень (P_pos = {baseline_pr:.3f})")
    axes[1].set_title("2. Precision-Recall кривые (PR Curves)", fontsize=11.5, pad=10)
    axes[1].set_xlabel("Полнота (Recall = TP / (TP + FN))")
    axes[1].set_ylabel("Точность (Precision = TP / (TP + FP))")
    axes[1].legend(loc="lower left", fontsize=9.5)

    plt.suptitle("Рисунок 4.8 – Сравнительный анализ интегральных кривых качества классификации: ROC-кривые и PR-кривые", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "08_roc_and_pr_curves_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 4.9: Итоговый рейтинг метрик и значимость признаков
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Сравнение ключевых метрик
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    x = np.arange(len(metrics_names))
    width = 0.20

    for idx, (name, m_dict) in enumerate(metrics_table.items()):
        vals = [m_dict["accuracy"], m_dict["precision"], m_dict["recall"], m_dict["f1"], m_dict["roc_auc"]]
        bars = axes[0].bar(x + idx * width - 1.5 * width, vals, width, label=name, color=colors_models[idx])
        for bar in bars:
            h = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.015, f"{h:.2f}",
                         ha="center", va="bottom", fontsize=8.0, fontweight="bold", rotation=90)

    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metrics_names, fontsize=10.5)
    axes[0].set_ylabel("Значение метрики")
    axes[0].set_ylim(0, 1.15)
    axes[0].set_title("1. Сравнение метрик качества моделей на тестовой выборке", fontsize=11.5, pad=10)
    axes[0].legend(loc="upper left", fontsize=9)

    # Важность признаков в дереве CART
    importances = pd.Series(cart_model.feature_importances_, index=feature_cols).sort_values(ascending=True)
    axes[1].barh(importances.index, importances.values, color="#00695c", height=0.6)
    for i, v in enumerate(importances.values):
        axes[1].text(v + 0.01, i, f"{v*100:.1f}%", va="center", fontsize=9.5, fontweight="bold")
    axes[1].set_title("2. Важность факторов риска дефолта (Feature Importance CART Gini)", fontsize=11.5, pad=10)
    axes[1].set_xlabel("Доля снижения критерия Джини (Gini Impurity Decrease)")
    axes[1].set_xlim(0, max(importances.values) * 1.25)

    plt.suptitle("Рисунок 4.9 – Итоговое сопоставление метрик классификаторов и ключевые факторы риска кредитования", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "09_model_metrics_and_feature_importances.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Скопируем все 9 графиков в папку latex/plots для Overleaf
    for p_name in os.listdir(PLOTS_DIR):
        if p_name.endswith(".png"):
            src_f = os.path.join(PLOTS_DIR, p_name)
            dst_f = os.path.join(LATEX_PLOTS_DIR, p_name)
            import shutil
            shutil.copy2(src_f, dst_f)

    # 5. Инференс на 450 соискателях кредита (Кредитный скоринг)
    prob_unlabeled = svm_linear.predict_proba(X_unlabeled_scaled)[:, 1]
    pred_unlabeled = (prob_unlabeled >= 0.35).astype(int) # скоринговый порог отсечения риска 35%
    
    df_scored = df_unlabeled.copy()
    df_scored["Default_Probability"] = np.round(prob_unlabeled, 4)
    df_scored["Credit_Decision"] = np.where(pred_unlabeled == 0, "Approved (Одобрен)", "Rejected (Отказ)")
    df_scored.to_csv(os.path.join(DATA_DIR, "Bankloan_unlabeled_scored.csv"), index=False)
    print(f"Скоринг 450 соискателей завершен: Одобрено {(pred_unlabeled==0).sum()}, Отказано {(pred_unlabeled==1).sum()}.")

    # 6. Экспорт итогового JSON
    summary_data = {
        "dataset_name": "Bankloan.csv",
        "dataset_task": "Bank Loan Defaulter Binary Classification",
        "total_raw_rows": len(df_raw),
        "labeled_rows": len(df_labeled),
        "unlabeled_scoring_rows": len(df_unlabeled),
        "features_count": len(feature_cols),
        "feature_names": feature_cols,
        "target_name": target_col,
        "class_distribution": {
            "class_0_non_default": int((df_labeled[target_col]==0).sum()),
            "class_1_default": int((df_labeled[target_col]==1).sum()),
            "class_0_percentage": float(np.round((df_labeled[target_col]==0).mean() * 100, 2)),
            "class_1_percentage": float(np.round((df_labeled[target_col]==1).mean() * 100, 2))
        },
        "train_test_split": {
            "train_size": len(X_train),
            "test_size": len(X_test),
            "test_percentage": 20,
            "random_state": 42
        },
        "models_evaluation": metrics_table,
        "best_model": {
            "name": "SVM (Linear Kernel)",
            "accuracy": metrics_table["SVM (Linear Kernel)"]["accuracy"],
            "f1_score": metrics_table["SVM (Linear Kernel)"]["f1"],
            "roc_auc": metrics_table["SVM (Linear Kernel)"]["roc_auc"]
        },
        "scoring_inference": {
            "approved_count": int((pred_unlabeled==0).sum()),
            "rejected_count": int((pred_unlabeled==1).sum()),
            "threshold": 0.35
        }
    }

    with open(os.path.join(BASE_DIR, "classification_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    print("\n[OK] Все 9 графиков, предобработанные таблицы и classification_summary.json успешно сгенерированы!")

if __name__ == "__main__":
    run_pipeline()
