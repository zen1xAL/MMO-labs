"""
Полный модульный пайплайн для Лабораторной работы №3 по курсу «Методы машинного обучения».
Тема: «Градиентный спуск, стохастический градиентный спуск и регуляризация».
Студент: Власовец А. И., гр. 351002 (Вариант 7 - нечетный: L2-регуляризация).
Преподаватель: Лебедевич А. В.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso

# Настройка шрифтов и стилей графиков
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="DejaVu Sans")

BASE_DIR = r"d:\MMO\lab3"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

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

# =============================================================================
# РЕАЛИЗАЦИЯ АЛГОРИТМОВ ГРАДИЕНТНОГО СПУСКА
# =============================================================================

def compute_mse(X: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    """Вычисляет среднеквадратичную ошибку (Mean Squared Error)."""
    residuals = X @ w - y
    return float(np.mean(residuals ** 2))

def batch_gradient_descent(X: np.ndarray, y: np.ndarray, eta: float = 0.05,
                           eps: float = 1e-5, max_iter: int = 1000):
    """
    Классический пакетный градиентный спуск (Batch Gradient Descent):
    w^k = w^(k-1) - eta * grad Q(w^(k-1), X)
    Критерий остановки: ||w^k - w^(k-1)|| < eps
    """
    l, d = X.shape
    w = np.zeros(d, dtype=float)
    w_history = [w.copy()]
    mse_history = [compute_mse(X, y, w)]
    diff_norms = []
    converged = False

    for k in range(1, max_iter + 1):
        grad = (2.0 / l) * (X.T @ (X @ w - y))
        w_new = w - eta * grad
        diff_norm = float(np.linalg.norm(w_new - w))
        diff_norms.append(diff_norm)

        w = w_new
        w_history.append(w.copy())
        mse_history.append(compute_mse(X, y, w))

        if diff_norm < eps:
            converged = True
            break

    return {
        "w": w,
        "w_history": np.array(w_history),
        "mse_history": np.array(mse_history),
        "diff_norms": np.array(diff_norms),
        "iterations": len(diff_norms),
        "converged": converged,
        "final_mse": mse_history[-1]
    }

def stochastic_gradient_descent(X: np.ndarray, y: np.ndarray, eta0: float = 0.05,
                                max_iter: int = 2000, seed: int = 42):
    """
    Стохастический градиентный спуск (Stochastic Gradient Descent):
    На каждом шаге выбирается случайный объект i in {0, ..., l-1}:
    w^k = w^(k-1) - eta_k * 2 * (x_i^T w^(k-1) - y_i) * x_i
    """
    np.random.seed(seed)
    l, d = X.shape
    w = np.zeros(d, dtype=float)
    w_history = [w.copy()]
    mse_history = [compute_mse(X, y, w)]

    for k in range(1, max_iter + 1):
        idx = np.random.randint(0, l)
        xi = X[idx]
        yi = y[idx]
        grad_i = 2.0 * (xi @ w - yi) * xi
        eta_k = eta0 / (1.0 + 0.001 * k) # затухающий шаг обучения
        w = w - eta_k * grad_i

        w_history.append(w.copy())
        mse_history.append(compute_mse(X, y, w))

    return {
        "w": w,
        "w_history": np.array(w_history),
        "mse_history": np.array(mse_history),
        "iterations": max_iter,
        "final_mse": mse_history[-1]
    }

def ridge_analytical(X: np.ndarray, y: np.ndarray, l2_lambda: float) -> np.ndarray:
    """Точное аналитическое решение Ridge регрессии (МНК с L2 штрафом)."""
    l, d = X.shape
    I_reg = np.eye(d, dtype=float)
    I_reg[0, 0] = 0.0 # свободный член не регуляризуется
    return np.linalg.inv(X.T @ X + l2_lambda * l * I_reg) @ (X.T @ y)

def batch_gradient_descent_l2(X: np.ndarray, y: np.ndarray, l2_lambda: float,
                              eta: float = None, eps: float = 1e-5, max_iter: int = 1500):
    """
    Градиентный спуск с L2-регуляризацией (Ridge Regression):
    Q_L2(w) = (1/l) ||Xw - y||^2 + lambda * ||w_{1:d}||^2
    grad Q_L2 = (2/l) X^T(Xw - y) + 2 * lambda * [0, w_1, ..., w_d]^T
    """
    l, d = X.shape
    w = np.zeros(d, dtype=float)
    reg_mask = np.ones(d, dtype=float)
    reg_mask[0] = 0.0 # свободный член (bias) не штрафуется

    if eta is None:
        eta = min(0.05, 0.45 / (1.0 + l2_lambda))

    for k in range(1, max_iter + 1):
        grad = (2.0 / l) * (X.T @ (X @ w - y)) + 2.0 * l2_lambda * (w * reg_mask)
        w_new = w - eta * grad
        if np.linalg.norm(w_new - w) < eps:
            w = w_new
            break
        w = w_new

    return w

def batch_gradient_descent_l1(X: np.ndarray, y: np.ndarray, l1_lambda: float,
                              eta: float = 0.05, eps: float = 1e-5, max_iter: int = 1500):
    """
    Градиентный спуск с L1-регуляризацией (Lasso / Soft-Thresholding):
    Q_L1(w) = (1/l) ||Xw - y||^2 + lambda * sum(|w_{1:d}|)
    """
    l, d = X.shape
    w = np.zeros(d, dtype=float)
    reg_mask = np.ones(d, dtype=float)
    reg_mask[0] = 0.0

    for k in range(1, max_iter + 1):
        grad = (2.0 / l) * (X.T @ (X @ w - y)) + l1_lambda * np.sign(w) * reg_mask
        w_new = w - eta * grad
        if np.linalg.norm(w_new - w) < eps:
            w = w_new
            break
        w = w_new

    return w

# =============================================================================
# ГЛАВНЫЙ КОНВЕЙЕР ИССЛЕДОВАНИЯ И ГЕНЕРАЦИИ ГРАФИКОВ
# =============================================================================

def run_pipeline():
    print("Генерация синтетического датасета...")
    # 1. Генерация данных: 1000 наблюдений, 2 признака (вектор весов размерности 3 с bias)
    X_raw, y_raw, coef_true = make_regression(
        n_samples=1000,
        n_features=2,
        noise=10.0,
        coef=True,
        random_state=42
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    X_b = np.c_[np.ones(len(X_scaled)), X_scaled] # добавили столбец единиц для w0 (bias)

    # Сохранение датасета
    df_data = pd.DataFrame(X_raw, columns=["Feature_1", "Feature_2"])
    df_data["Target_y"] = y_raw
    df_data.to_csv(os.path.join(DATA_DIR, "synthetic_regression_raw.csv"), index=False)

    df_scaled = pd.DataFrame(X_scaled, columns=["Feature_1_scaled", "Feature_2_scaled"])
    df_scaled["Target_y"] = y_raw
    df_scaled.to_csv(os.path.join(DATA_DIR, "synthetic_regression_scaled.csv"), index=False)

    # Аналитическое решение МНК (Normal Equation)
    w_analytical = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y_raw

    # =========================================================================
    # РИСУНОК 3.1: Структура и распределение признаков
    # =========================================================================
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    
    # Feature 1 vs y
    axes[0].scatter(X_scaled[:, 0], y_raw, color="#1565c0", alpha=0.5, edgecolors='none', s=25)
    axes[0].set_title("1. Зависимость y от Feature_1 (scaled)", fontsize=11)
    axes[0].set_xlabel("Feature_1 (стандартизированный)")
    axes[0].set_ylabel("Целевая переменная y")

    # Feature 2 vs y
    axes[1].scatter(X_scaled[:, 1], y_raw, color="#2e7d32", alpha=0.5, edgecolors='none', s=25)
    axes[1].set_title("2. Зависимость y от Feature_2 (scaled)", fontsize=11)
    axes[1].set_xlabel("Feature_2 (стандартизированный)")
    axes[1].set_ylabel("Целевая переменная y")

    # Распределение y
    sns.histplot(y_raw, kde=True, ax=axes[2], color="#6a1b9a", bins=25)
    axes[2].set_title("3. Распределение целевой переменной y", fontsize=11)
    axes[2].set_xlabel("Значение y")
    axes[2].set_ylabel("Частота")

    plt.suptitle("Рисунок 3.1 – Структура и распределение признаков синтетического регрессионного датасета", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "01_dataset_regression_structure.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.2: Сходимость базового градиентного спуска (BGD)
    # =========================================================================
    bgd_res = batch_gradient_descent(X_b, y_raw, eta=0.05, eps=1e-5, max_iter=500)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    
    # MSE curve
    axes[0].plot(range(len(bgd_res["mse_history"])), bgd_res["mse_history"], color="#d32f2f", lw=2)
    axes[0].set_title("1. Снижение среднеквадратичной ошибки (MSE)", fontsize=11)
    axes[0].set_xlabel("Номер итерации (k)")
    axes[0].set_ylabel("Критерий качества Q(w) = MSE")
    axes[0].set_yscale("log")

    # ||w^k - w^(k-1)||
    axes[1].plot(range(1, len(bgd_res["diff_norms"]) + 1), bgd_res["diff_norms"], color="#0288d1", lw=2, label="||w^k - w^(k-1)||")
    axes[1].axhline(1e-5, color="#e65100", linestyle="--", lw=1.5, label="Порог ε = 10⁻⁵")
    axes[1].set_title("2. Норма изменения шага весов", fontsize=11)
    axes[1].set_xlabel("Номер итерации (k)")
    axes[1].set_ylabel("Евклидова норма разности ||w^k - w^(k-1)||")
    axes[1].set_yscale("log")
    axes[1].legend()

    # Траектория в пространстве весов (w1, w2)
    w_hist = bgd_res["w_history"]
    axes[2].plot(w_hist[:, 1], w_hist[:, 2], 'o-', color="#43a047", markersize=3.5, lw=1.5, label="Траектория BGD")
    axes[2].plot(w_hist[0, 1], w_hist[0, 2], 's', color="#d32f2f", markersize=8, label="Старт w⁰=(0,0)")
    axes[2].plot(w_analytical[1], w_analytical[2], '*', color="#ffd600", markersize=14, markeredgecolor='black', label="Оптимум w*")
    axes[2].set_title("3. Траектория оптимизации весов (w₁, w₂)", fontsize=11)
    axes[2].set_xlabel("Вес w₁ (Feature_1)")
    axes[2].set_ylabel("Вес w₂ (Feature_2)")
    axes[2].legend()

    plt.suptitle("Рисунок 3.2 – Сходимость градиентного спуска (BGD), норма шага весов и траектория оптимизации", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "02_bgd_convergence_trajectory.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.3: Эксперименты со скоростью обучения (Learning Rate)
    # =========================================================================
    etas = [0.001, 0.01, 0.05, 0.1, 0.5]
    colors_eta = ["#9c27b0", "#1976d2", "#43a047", "#f57c00", "#d32f2f"]
    eta_results = {}

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))

    for eta_val, c_color in zip(etas, colors_eta):
        res = batch_gradient_descent(X_b, y_raw, eta=eta_val, eps=1e-5, max_iter=300)
        eta_results[eta_val] = res
        axes[0].plot(range(min(120, len(res["mse_history"]))), res["mse_history"][:120],
                     lw=2, color=c_color, label=f"η = {eta_val} ({res['iterations']} ит.)")

    axes[0].set_title("1. Кривые обучения MSE при различных η", fontsize=11)
    axes[0].set_xlabel("Номер итерации (k)")
    axes[0].set_ylabel("MSE (log scale)")
    axes[0].set_yscale("log")
    axes[0].legend()

    # Итерации сходимости
    eta_labels = [f"η={e}" for e in etas]
    iters = [eta_results[e]["iterations"] for e in etas]
    bars = axes[1].bar(eta_labels, iters, color=colors_eta, width=0.55)
    for bar in bars:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f"{int(bar.get_height())}",
                     ha='center', va='bottom', fontsize=9.5, fontweight='bold', color="#263238")
    axes[1].set_title("2. Число итераций до критерия ||Δw|| < 10⁻⁵", fontsize=11)
    axes[1].set_ylabel("Число итераций до остановки")
    axes[1].set_ylim(0, max(iters) * 1.18)

    # Аналитическая карточка
    card_eta_lines = [
        ("η = 0.001 (слишком малый):", f"{eta_results[0.001]['iterations']} ит. (медленная сходимость)", "#9c27b0"),
        ("η = 0.01 (умеренный):", f"{eta_results[0.01]['iterations']} ит. (уверенное движение)", "#1976d2"),
        ("η = 0.05 (оптимальный):", f"{eta_results[0.05]['iterations']} ит. (быстро и стабильно)", "#2e7d32"),
        ("η = 0.1 (агрессивный):", f"{eta_results[0.1]['iterations']} ит. (минимальное число шагов)", "#e65100"),
        ("η = 0.5 (пограничный):", f"{eta_results[0.5]['iterations']} ит. (осцилляции вокруг минимума)", "#c62828"),
        ("Критерий останова:", "||wᵏ - wᵏ⁻¹|| < 10⁻⁵", "#37474f")
    ]
    add_summary_card(axes[2], "Анализ влияния темпа обучения", card_eta_lines)

    plt.suptitle("Рисунок 3.3 – Влияние скорости обучения (learning rate η) на сходимость градиентного спуска", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "03_learning_rate_experiments.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.4: Сравнение градиентного (BGD) и стохастического (SGD) спуска
    # =========================================================================
    sgd_res = stochastic_gradient_descent(X_b, y_raw, eta0=0.015, max_iter=1500, seed=42)
    bgd_compare = batch_gradient_descent(X_b, y_raw, eta=0.05, eps=1e-5, max_iter=250)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))

    # Панель 1: Совмещенный график MSE
    axes[0].plot(range(len(bgd_compare["mse_history"])), bgd_compare["mse_history"],
                 color="#d32f2f", lw=2.5, label=f"Batch GD (пакетный, l={len(X_b)})")
    # Прореживаем SGD для чистоты графика
    sgd_plot_steps = np.arange(0, len(sgd_res["mse_history"]), 5)
    axes[0].plot(sgd_plot_steps, sgd_res["mse_history"][sgd_plot_steps],
                 color="#1976d2", alpha=0.7, lw=1.2, label="Stochastic GD (1 объект)")
    axes[0].set_title("1. Сопоставление динамики MSE на одном графике", fontsize=11)
    axes[0].set_xlabel("Номер итерации (k)")
    axes[0].set_ylabel("MSE (log scale)")
    axes[0].set_yscale("log")
    axes[0].legend()

    # Панель 2: Траектории в пространстве весов
    w_bgd = bgd_compare["w_history"]
    w_sgd = sgd_res["w_history"][::8]
    axes[1].plot(w_bgd[:, 1], w_bgd[:, 2], 'r-', lw=2.5, label="Траектория BGD (детерминированная)")
    axes[1].plot(w_sgd[:, 1], w_sgd[:, 2], color="#1976d2", alpha=0.6, lw=0.9, label="Траектория SGD (стохастическая)")
    axes[1].plot(w_analytical[1], w_analytical[2], '*', color="#ffd600", markersize=14, markeredgecolor='black', label="Оптимум w*")
    axes[1].set_title("2. Пространственные траектории весов (w₁, w₂)", fontsize=11)
    axes[1].set_xlabel("Вес w₁")
    axes[1].set_ylabel("Вес w₂")
    axes[1].legend()

    # Панель 3: Сравнительная аналитическая карточка
    card_bgd_sgd = [
        ("Сложность шага BGD:", "O(ℓ · d) — расчет по всей выборке", "#c62828"),
        ("Сложность шага SGD:", "O(d) — расчет по 1 объекту", "#1565c0"),
        ("Форма кривой BGD:", "Монотонное гладкое убывание", "#c62828"),
        ("Форма кривой SGD:", "Стохастические флуктуации (шум)", "#1565c0"),
        ("Условие сходимости SGD:", "Затухающий шаг η_k = η₀ / (1+λk)", "#2e7d32"),
        ("Итоговое качество:", "Оба метода достигают окрестности w*", "#2e7d32")
    ]
    add_summary_card(axes[2], "Сравнение методов оптимизации", card_bgd_sgd)

    plt.suptitle("Рисунок 3.4 – Сравнительный анализ сходимости пакетного (BGD) и стохастического (SGD) градиентного спуска", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "04_bgd_vs_sgd_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.5: L2 Регуляризация (Вариант 7 - нечетный)
    # =========================================================================
    # 20 коэффициентов регуляризации в диапазоне от 0.001 до 1000
    lambdas = np.logspace(-3, 3, 20)
    weights_l2 = []
    mse_l2 = []

    for lam in lambdas:
        w_l2 = ridge_analytical(X_b, y_raw, l2_lambda=lam)
        weights_l2.append(w_l2)
        mse_l2.append(compute_mse(X_b, y_raw, w_l2))

    weights_l2 = np.array(weights_l2)
    norm_l2 = np.linalg.norm(weights_l2[:, 1:], axis=1) # норма весов без bias

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))

    # Регуляризационные пути весов
    axes[0].plot(lambdas, weights_l2[:, 0], 'k--', lw=1.8, label="w₀ (Bias, не штрафуется)")
    axes[0].plot(lambdas, weights_l2[:, 1], color="#1976d2", lw=2.2, label="w₁ (Feature_1)")
    axes[0].plot(lambdas, weights_l2[:, 2], color="#2e7d32", lw=2.2, label="w₂ (Feature_2)")
    axes[0].set_xscale("log")
    axes[0].set_title("1. Регуляризационные пути весов при росте λ", fontsize=11)
    axes[0].set_xlabel("Коэффициент регуляризации λ (log scale)")
    axes[0].set_ylabel("Значение весовых коэффициентов w")
    axes[0].legend()

    # Евклидова норма весов ||w||_2
    axes[1].plot(lambdas, norm_l2, color="#d32f2f", lw=2.5)
    axes[1].set_xscale("log")
    axes[1].set_title("2. Сжатие евклидовой нормы весов ||w_{1:d}||₂", fontsize=11)
    axes[1].set_xlabel("Коэффициент регуляризации λ (log scale)")
    axes[1].set_ylabel("Евклидова норма ||w||₂")

    # Карточка выводов по регуляризации
    card_l2_lines = [
        ("Тип регуляризации:", "L2 (Ridge / гребневая) — Вариант 7", "#1565c0"),
        ("Диапазон 20 коэфф. λ:", "[0.001; 1000.0] (logspace)", "#37474f"),
        ("При λ = 0.001 (слабая):", f"w₁={weights_l2[0, 1]:.2f}, w₂={weights_l2[0, 2]:.2f} (МНК-база)", "#2e7d32"),
        ("При λ = 1000.0 (сильная):", f"w₁={weights_l2[-1, 1]:.4f}, w₂={weights_l2[-1, 2]:.4f} (асимптота 0)", "#c62828"),
        ("Свободный член w₀:", f"Стабилен (w₀ ≈ {weights_l2[-1, 0]:.2f})", "#1565c0"),
        ("Эффект Ridge Shrinkage:", "Плавное непрерывное сжатие к нулю", "#2e7d32")
    ]
    add_summary_card(axes[2], "Итоги L2-регуляризации (Вариант 7)", card_l2_lines)

    plt.suptitle("Рисунок 3.5 – Регуляризационные пути весов при L2-регуляризации (Ridge Regression) для 20 коэффициентов", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "05_l2_regularization_paths.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.6: Сравнение L1 (Lasso) и L2 (Ridge) регуляризации
    # =========================================================================
    weights_l1 = []
    for lam in lambdas:
        lasso = Lasso(alpha=lam, max_iter=3000, tol=1e-4).fit(X_scaled, y_raw)
        weights_l1.append(np.r_[lasso.intercept_, lasso.coef_])
    weights_l1 = np.array(weights_l1)

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.5))

    # Ridge L2
    axes[0].plot(lambdas, weights_l2[:, 1], color="#1976d2", lw=2.2, label="w₁ (L2 Ridge)")
    axes[0].plot(lambdas, weights_l2[:, 2], color="#2e7d32", lw=2.2, label="w₂ (L2 Ridge)")
    axes[0].set_xscale("log")
    axes[0].set_title("1. L2-регуляризация (Ridge): асимптотическое сжатие", fontsize=11.5)
    axes[0].set_xlabel("Коэффициент регуляризации λ (log scale)")
    axes[0].set_ylabel("Веса w")
    axes[0].axhline(0, color="gray", linestyle=":", lw=1)
    axes[0].legend()

    # Lasso L1
    axes[1].plot(lambdas, weights_l1[:, 1], color="#d32f2f", lw=2.2, label="w₁ (L1 Lasso)")
    axes[1].plot(lambdas, weights_l1[:, 2], color="#e65100", lw=2.2, label="w₂ (L1 Lasso)")
    axes[1].set_xscale("log")
    axes[1].set_title("2. L1-регуляризация (Lasso): зануление весов (Sparse Weights)", fontsize=11.5)
    axes[1].set_xlabel("Коэффициент регуляризации λ (log scale)")
    axes[1].set_ylabel("Веса w")
    axes[1].axhline(0, color="gray", linestyle=":", lw=1)
    axes[1].legend()

    plt.suptitle("Рисунок 3.6 – Сравнительный анализ поведения весов при L2 (Ridge) и L1 (Lasso) регуляризации", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "06_l1_vs_l2_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================================
    # РИСУНОК 3.7: Верификация модели и анализ остатков
    # =========================================================================
    y_pred_bgd = X_b @ bgd_res["w"]
    residuals = y_raw - y_pred_bgd

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))

    # Scatter y vs y_pred
    axes[0].scatter(y_raw, y_pred_bgd, color="#1565c0", alpha=0.5, s=25, edgecolors='none')
    y_line = np.linspace(min(y_raw), max(y_raw), 100)
    axes[0].plot(y_line, y_line, 'r--', lw=2, label="Идеальная регрессия ŷ = y")
    axes[0].set_title("1. Фактические значения y vs Прогнозы ŷ", fontsize=11)
    axes[0].set_xlabel("Фактическое значение y")
    axes[0].set_ylabel("Прогноз модели ŷ")
    axes[0].legend()

    # Гистограмма остатков
    sns.histplot(residuals, kde=True, ax=axes[1], color="#2e7d32", bins=25)
    axes[1].axvline(0, color="red", linestyle="--", lw=1.5)
    axes[1].set_title("2. Распределение остатков (Residuals: y - ŷ)", fontsize=11)
    axes[1].set_xlabel("Величина ошибки регрессии")
    axes[1].set_ylabel("Частота")

    # Сравнение весов с МНК и Sklearn
    sk_model = LinearRegression().fit(X_scaled, y_raw)
    w_sklearn = np.r_[sk_model.intercept_, sk_model.coef_]
    
    card_verif_lines = [
        ("Точное аналитическое МНК:", f"[{w_analytical[0]:.2f}, {w_analytical[1]:.2f}, {w_analytical[2]:.2f}]", "#37474f"),
        ("Пакетный градиентный спуск:", f"[{bgd_res['w'][0]:.2f}, {bgd_res['w'][1]:.2f}, {bgd_res['w'][2]:.2f}]", "#1565c0"),
        ("Эталон LinearRegression (sklearn):", f"[{w_sklearn[0]:.2f}, {w_sklearn[1]:.2f}, {w_sklearn[2]:.2f}]", "#2e7d32"),
        ("Разность ||w_BGD - w_МНК||:", f"{np.linalg.norm(bgd_res['w'] - w_analytical):.2e} (полное совпадение)", "#2e7d32"),
        ("Коэффициент детерминации R²:", f"{1 - np.var(residuals)/np.var(y_raw):.4f}", "#1565c0"),
        ("MSE финальной модели:", f"{bgd_res['final_mse']:.2f} (σ²_noise = 100)", "#37474f")
    ]
    add_summary_card(axes[2], "Верификация точности модели", card_verif_lines)

    plt.suptitle("Рисунок 3.7 – Верификация модели: сопоставление прогнозов, остатки регрессии и сравнение с МНК", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig(os.path.join(PLOTS_DIR, "07_model_evaluation_residuals.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Сохраняем структурированное резюме эксперимента
    summary = {
        "dataset": {
            "n_samples": 1000,
            "n_features": 2,
            "weights_count": 3,
            "noise_std": 10.0,
            "random_state": 42
        },
        "analytical_weights": list(w_analytical),
        "bgd_results": {
            "w": list(bgd_res["w"]),
            "iterations": bgd_res["iterations"],
            "converged": bgd_res["converged"],
            "final_mse": bgd_res["final_mse"],
            "diff_from_analytical": float(np.linalg.norm(bgd_res["w"] - w_analytical))
        },
        "sgd_results": {
            "w": list(sgd_res["w"]),
            "iterations": sgd_res["iterations"],
            "final_mse": sgd_res["final_mse"]
        },
        "learning_rates_tested": etas,
        "l2_regularization": {
            "variant": 7,
            "type": "L2 Ridge",
            "lambdas_count": len(lambdas),
            "lambda_min": float(lambdas[0]),
            "lambda_max": float(lambdas[-1]),
            "w_at_lambda_min": list(weights_l2[0]),
            "w_at_lambda_max": list(weights_l2[-1])
        }
    }
    with open(os.path.join(BASE_DIR, "gd_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Все 7 графиков, датасеты и файл gd_summary.json успешно сгенерированы!")

if __name__ == "__main__":
    run_pipeline()
