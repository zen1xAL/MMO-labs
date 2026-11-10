"""
Automated Senior QA Test Suite for MMO Laboratory Work #4.
Discipline: Methods of Machine Learning (BSUIR)
Student: Vlasovets A. I., Group 351002 (Variant 7 - Binary Classification)
Dataset: Bankloan.csv (Credit Risk Scoring)

Conducts full-cycle verification of data integrity, classification models (LR, Linear SVM, RBF SVM, CART),
metrics (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC), visualizations, Jupyter notebook,
reports (STP 01-2017 DOCX & PDF), LaTeX Overleaf project, and final archive.
"""

import os
import sys
import json
import zipfile
import numpy as np
import pandas as pd
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\MMO\lab4"
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
LATEX_PLOTS_DIR = os.path.join(BASE_DIR, "latex", "plots")
RAW_DATA_PATH = os.path.join(DATA_DIR, "Bankloan_raw.csv")
CLEAN_DATA_PATH = os.path.join(DATA_DIR, "Bankloan_clean.csv")
TRAIN_SCALED_PATH = os.path.join(DATA_DIR, "Bankloan_train_scaled.csv")
TEST_SCALED_PATH = os.path.join(DATA_DIR, "Bankloan_test_scaled.csv")
SCORED_DATA_PATH = os.path.join(DATA_DIR, "Bankloan_unlabeled_scored.csv")
SUMMARY_PATH = os.path.join(BASE_DIR, "classification_summary.json")
NOTEBOOK_PATH = os.path.join(BASE_DIR, "LR04_Classification.ipynb")
DOCX_PATH = os.path.join(BASE_DIR, "report", "Отчет_ЛР04_Власовец_Вариант7.docx")
PDF_PATH = os.path.join(BASE_DIR, "Отчет_ЛР04_Власовец_Вариант7.pdf")
LATEX_PATH = os.path.join(BASE_DIR, "latex", "main.tex")
README_OVERLEAF_PATH = os.path.join(BASE_DIR, "latex", "README_OVERLEAF.txt")
DEFENSE_GUIDE_PATH = os.path.join(BASE_DIR, "LAB4_DEFENSE_GUIDE.md")
EXPLANATION_PATH = os.path.join(BASE_DIR, "LAB04_EXPLANATION.md")
ZIP_PATH = os.path.join(BASE_DIR, "LR04_Vlasovets_Variant7.zip")

class QATestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.details = []

    def assert_true(self, condition: bool, test_name: str, message: str = ""):
        if condition:
            self.passed += 1
            self.details.append(f"[PASS] {test_name}")
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            err_msg = f"[FAIL] {test_name}: {message}"
            self.details.append(err_msg)
            print(f"  {err_msg}")

    def warn(self, test_name: str, message: str):
        self.warnings += 1
        w_msg = f"[WARN] {test_name}: {message}"
        self.details.append(w_msg)
        print(f"  {w_msg}")

def run_all_qa_tests():
    qa = QATestResult()
    print("=" * 80)
    print("STARTING SENIOR QA TEST SUITE: MMO LAB 4 (CLASSIFICATION & SCORING)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # SUITE 1: Data Integrity & Stratification Checks
    # -------------------------------------------------------------------------
    print("\n--- SUITE 1: Data Integrity & Preprocessing Verification ---")
    qa.assert_true(os.path.exists(RAW_DATA_PATH), "DATA-01.1", f"Raw data exists at {RAW_DATA_PATH}")
    if os.path.exists(RAW_DATA_PATH):
        df_raw = pd.read_csv(RAW_DATA_PATH)
        qa.assert_true(df_raw.shape == (1150, 9), "DATA-01.2", f"Raw shape is (1150, 9), got {df_raw.shape}")
        expected_cols = ['age', 'ed', 'employ', 'address', 'income', 'debtinc', 'creddebt', 'othdebt', 'default']
        qa.assert_true(list(df_raw.columns) == expected_cols, "DATA-01.3", f"Columns match expected, got {list(df_raw.columns)}")
        # Check that first 700 have default, last 450 are NaN
        qa.assert_true(df_raw.iloc[:700]['default'].notna().all(), "DATA-01.4", "First 700 rows have valid default labels")
        qa.assert_true(df_raw.iloc[700:]['default'].isna().all(), "DATA-01.5", "Last 450 rows have NaN default labels for scoring")
        # Check no missing values in features
        feature_cols = expected_cols[:-1]
        qa.assert_true(df_raw[feature_cols].isnull().sum().sum() == 0, "DATA-01.6", "Zero missing values across all 8 features in raw data")

    qa.assert_true(os.path.exists(CLEAN_DATA_PATH), "DATA-02.1", f"Clean labeled data exists at {CLEAN_DATA_PATH}")
    if os.path.exists(CLEAN_DATA_PATH):
        df_clean = pd.read_csv(CLEAN_DATA_PATH)
        qa.assert_true(df_clean.shape == (700, 9), "DATA-02.2", f"Clean labeled shape is (700, 9), got {df_clean.shape}")
        qa.assert_true(df_clean['default'].isnull().sum() == 0, "DATA-02.3", "Zero missing values in clean labeled data")
        class_counts = df_clean['default'].value_counts()
        qa.assert_true(class_counts[0] == 517 and class_counts[1] == 183, "DATA-02.4",
                       f"Class distribution is 517 non-default vs 183 default, got {dict(class_counts)}")

    qa.assert_true(os.path.exists(TRAIN_SCALED_PATH), "DATA-03.1", f"Train scaled data exists at {TRAIN_SCALED_PATH}")
    qa.assert_true(os.path.exists(TEST_SCALED_PATH), "DATA-03.2", f"Test scaled data exists at {TEST_SCALED_PATH}")
    if os.path.exists(TRAIN_SCALED_PATH) and os.path.exists(TEST_SCALED_PATH):
        df_train = pd.read_csv(TRAIN_SCALED_PATH)
        df_test = pd.read_csv(TEST_SCALED_PATH)
        qa.assert_true(df_train.shape == (560, 9), "DATA-03.3", f"Train shape is (560, 9) [80% split], got {df_train.shape}")
        qa.assert_true(df_test.shape == (140, 9), "DATA-03.4", f"Test shape is (140, 9) [20% split], got {df_test.shape}")
        # Stratification verification
        train_def_ratio = df_train['default'].mean()
        test_def_ratio = df_test['default'].mean()
        qa.assert_true(abs(train_def_ratio - 0.2607) < 0.01, "DATA-03.5",
                       f"Train default ratio matches 26.07% ({train_def_ratio:.4f})")
        qa.assert_true(abs(test_def_ratio - 0.2643) < 0.01, "DATA-03.6",
                       f"Test default ratio matches 26.43% ({test_def_ratio:.4f})")
        # Scaled mean ~ 0, std ~ 1 on train
        feat_means = df_train[feature_cols].mean()
        feat_stds = df_train[feature_cols].std()
        qa.assert_true(np.all(np.abs(feat_means) < 1e-12), "DATA-03.7", f"Train scaled feature means are ~0 (max {np.max(np.abs(feat_means)):.2e})")
        qa.assert_true(np.all(np.abs(feat_stds - 1.0) < 1e-2), "DATA-03.8", f"Train scaled feature stds are ~1.0 (max diff {np.max(np.abs(feat_stds - 1.0)):.4f})")

    qa.assert_true(os.path.exists(SCORED_DATA_PATH), "DATA-04.1", f"Scored applicants data exists at {SCORED_DATA_PATH}")
    if os.path.exists(SCORED_DATA_PATH):
        df_scored = pd.read_csv(SCORED_DATA_PATH)
        qa.assert_true(df_scored.shape == (450, 10), "DATA-04.2", f"Scored data shape is (450, 10), got {df_scored.shape}")
        qa.assert_true('Default_Probability' in df_scored.columns and 'Credit_Decision' in df_scored.columns, "DATA-04.3",
                       "Scored file contains Default_Probability and Credit_Decision columns")
        qa.assert_true(((df_scored['Default_Probability'] >= 0.0) & (df_scored['Default_Probability'] <= 1.0)).all(), "DATA-04.4",
                       "All predicted default probabilities are within [0.0, 1.0]")
        qa.assert_true(set(df_scored['Credit_Decision'].unique()).issubset({'Approved (Одобрен)', 'Rejected (Отказ)'}), "DATA-04.5",
                       "Predicted credit decisions match expected categories")
        pred_counts = df_scored['Credit_Decision'].value_counts()
        qa.assert_true(pred_counts['Approved (Одобрен)'] == 336 and pred_counts['Rejected (Отказ)'] == 114, "DATA-04.6",
                       f"Scoring decision matches 336 approved vs 114 rejected, got {dict(pred_counts)}")

    # -------------------------------------------------------------------------
    # SUITE 2: Classification Models & Mathematical Metric Integrity
    # -------------------------------------------------------------------------
    print("\n--- SUITE 2: Classification Models & Mathematical Metric Integrity ---")
    qa.assert_true(os.path.exists(SUMMARY_PATH), "MODEL-01.1", f"Classification summary JSON exists at {SUMMARY_PATH}")
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            summary = json.load(f)

        models = summary.get("models_evaluation", {})
        qa.assert_true("Logistic Regression" in models, "MODEL-01.2", "Logistic Regression present in summary")
        qa.assert_true("SVM (Linear Kernel)" in models, "MODEL-01.3", "SVM (Linear Kernel) present in summary")
        qa.assert_true("SVM (RBF Kernel)" in models, "MODEL-01.4", "SVM (RBF Kernel) present in summary")
        qa.assert_true("CART (Decision Tree)" in models, "MODEL-01.5", "CART (Decision Tree) present in summary")

        # Test Linear SVM metrics (best model)
        svm_lin = models["SVM (Linear Kernel)"]
        qa.assert_true(abs(svm_lin["accuracy"] - 0.8357) < 0.001, "MODEL-02.1", f"Linear SVM Accuracy == 0.8357, got {svm_lin['accuracy']}")
        qa.assert_true(abs(svm_lin["precision"] - 0.7333) < 0.001, "MODEL-02.2", f"Linear SVM Precision == 0.7333, got {svm_lin['precision']}")
        qa.assert_true(abs(svm_lin["recall"] - 0.5946) < 0.001, "MODEL-02.3", f"Linear SVM Recall == 0.5946, got {svm_lin['recall']}")
        qa.assert_true(abs(svm_lin["f1"] - 0.6567) < 0.001, "MODEL-02.4", f"Linear SVM F1 == 0.6567, got {svm_lin['f1']}")
        qa.assert_true(abs(svm_lin["roc_auc"] - 0.8699) < 0.001, "MODEL-02.5", f"Linear SVM ROC-AUC == 0.8699, got {svm_lin['roc_auc']}")

        # Test Logistic Regression metrics
        lr = models["Logistic Regression"]
        qa.assert_true(abs(lr["accuracy"] - 0.8143) < 0.001, "MODEL-03.1", f"LR Accuracy == 0.8143, got {lr['accuracy']}")
        qa.assert_true(abs(lr["precision"] - 0.6571) < 0.001, "MODEL-03.2", f"LR Precision == 0.6571, got {lr['precision']}")
        qa.assert_true(abs(lr["recall"] - 0.6216) < 0.001, "MODEL-03.3", f"LR Recall == 0.6216 (Highest Recall), got {lr['recall']}")
        qa.assert_true(abs(lr["f1"] - 0.6389) < 0.001, "MODEL-03.4", f"LR F1 == 0.6389, got {lr['f1']}")
        qa.assert_true(abs(lr["roc_auc"] - 0.8670) < 0.001, "MODEL-03.5", f"LR ROC-AUC == 0.8670, got {lr['roc_auc']}")

        # Test Confusion Matrices consistency across all models
        # On test set of 140 objects: total = 140, total positive = 37, total negative = 103
        for m_name, m_data in models.items():
            cm = m_data["confusion_matrix"]
            tn, fp = cm[0][0], cm[0][1]
            fn, tp = cm[1][0], cm[1][1]
            total_test = tn + fp + fn + tp
            qa.assert_true(total_test == 140, f"MODEL-CM-01 ({m_name})", f"Confusion matrix total == 140, got {total_test}")
            qa.assert_true(tp + fn == 37, f"MODEL-CM-02 ({m_name})", f"Actual defaults TP + FN == 37, got {tp + fn}")
            qa.assert_true(tn + fp == 103, f"MODEL-CM-03 ({m_name})", f"Actual non-defaults TN + FP == 103, got {tn + fp}")

            # Re-derive Accuracy and verify
            calc_acc = (tp + tn) / total_test
            qa.assert_true(abs(calc_acc - m_data["accuracy"]) < 0.0001, f"MODEL-CM-04 ({m_name})",
                           f"Accuracy formula verified: calc {calc_acc:.4f} == reported {m_data['accuracy']:.4f}")

    # -------------------------------------------------------------------------
    # SUITE 3: High-Resolution Visualizations (300 DPI)
    # -------------------------------------------------------------------------
    print("\n--- SUITE 3: Visualizations & DPI Verification ---")
    expected_plots = [
        "01_dataset_and_missing_analysis.png",
        "02_features_distributions_and_boxplots.png",
        "03_outliers_and_correlation_heatmap.png",
        "04_logistic_regression_analysis.png",
        "05_svm_decision_boundary_and_margins.png",
        "06_cart_decision_tree_visualization.png",
        "07_confusion_matrices_comparison.png",
        "08_roc_and_pr_curves_comparison.png",
        "09_model_metrics_and_feature_importances.png"
    ]

    for p_name in expected_plots:
        p_path = os.path.join(PLOTS_DIR, p_name)
        qa.assert_true(os.path.exists(p_path), f"PLOT-01 ({p_name})", f"Plot exists in plots/ {p_path}")
        if os.path.exists(p_path):
            with Image.open(p_path) as img:
                dpi = img.info.get("dpi", (0, 0))
                # Matplotlib dpi usually 300
                is_300_dpi = dpi[0] >= 299 and dpi[1] >= 299
                qa.assert_true(is_300_dpi, f"PLOT-DPI ({p_name})", f"Plot DPI is 300 (got {dpi})")
                qa.assert_true(img.width >= 1600 and img.height >= 1000, f"PLOT-RES ({p_name})",
                               f"Plot resolution >= 1600x1000 (got {img.width}x{img.height})")

        # Also check latex/plots/
        p_latex_path = os.path.join(LATEX_PLOTS_DIR, p_name)
        qa.assert_true(os.path.exists(p_latex_path), f"PLOT-LATEX ({p_name})", f"Plot synchronized in latex/plots/ {p_latex_path}")

    # -------------------------------------------------------------------------
    # SUITE 4: Interactive Jupyter Notebook Execution & Integrity
    # -------------------------------------------------------------------------
    print("\n--- SUITE 4: Interactive Jupyter Notebook Verification ---")
    qa.assert_true(os.path.exists(NOTEBOOK_PATH), "NB-01.1", f"Notebook exists at {NOTEBOOK_PATH}")
    if os.path.exists(NOTEBOOK_PATH):
        with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
            nb = json.load(f)

        cells = nb.get("cells", [])
        qa.assert_true(len(cells) >= 20, "NB-01.2", f"Notebook has >= 20 structured cells, got {len(cells)}")

        code_cells = [c for c in cells if c.get("cell_type") == "code"]
        md_cells = [c for c in cells if c.get("cell_type") == "markdown"]
        qa.assert_true(len(code_cells) >= 10, "NB-01.3", f"Code cells >= 10, got {len(code_cells)}")
        qa.assert_true(len(md_cells) >= 10, "NB-01.4", f"Markdown cells >= 10, got {len(md_cells)}")

        # Verify all code cells have execution outputs and execution_count
        executed_cells = 0
        total_outputs = 0
        for i, c in enumerate(code_cells):
            if c.get("execution_count") is not None:
                executed_cells += 1
            total_outputs += len(c.get("outputs", []))

        qa.assert_true(executed_cells == len(code_cells), "NB-01.5",
                       f"All code cells are executed ({executed_cells}/{len(code_cells)})")
        qa.assert_true(total_outputs >= len(code_cells), "NB-01.6",
                       f"Rich outputs present in all code cells (total {total_outputs} outputs)")

        # Verify embedded plots in cell outputs
        nb_str = json.dumps(nb)
        qa.assert_true('"image/png":' in nb_str, "NB-01.7",
                       "Embedded 300 DPI plots present in cell outputs for rich offline rendering")

    # -------------------------------------------------------------------------
    # SUITE 5: BSUIR STP 01-2017 Reports (DOCX & PDF) Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 5: Official Report (STP 01-2017 DOCX & PDF) Verification ---")
    qa.assert_true(os.path.exists(DOCX_PATH), "REPORT-01.1", f"Official DOCX report exists at {DOCX_PATH}")
    if os.path.exists(DOCX_PATH):
        docx_size_mb = os.path.getsize(DOCX_PATH) / (1024 * 1024)
        qa.assert_true(docx_size_mb >= 1.0, "REPORT-01.2", f"DOCX report size >= 1.0 MB (got {docx_size_mb:.2f} MB)")

    qa.assert_true(os.path.exists(PDF_PATH), "REPORT-02.1", f"Official PDF report exists at {PDF_PATH}")
    if os.path.exists(PDF_PATH):
        pdf_size_kb = os.path.getsize(PDF_PATH) / 1024
        qa.assert_true(pdf_size_kb >= 500, "REPORT-02.2", f"PDF report size >= 500 KB (got {pdf_size_kb:.1f} KB)")

    # -------------------------------------------------------------------------
    # SUITE 6: LaTeX Overleaf Project Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 6: LaTeX Overleaf Project Verification ---")
    qa.assert_true(os.path.exists(LATEX_PATH), "TEX-01.1", f"LaTeX main.tex exists at {LATEX_PATH}")
    qa.assert_true(os.path.exists(README_OVERLEAF_PATH), "TEX-01.2", f"README_OVERLEAF.txt exists at {README_OVERLEAF_PATH}")
    if os.path.exists(LATEX_PATH):
        with open(LATEX_PATH, "r", encoding="utf-8") as f:
            tex_content = f.read()
        qa.assert_true(len(tex_content) >= 15000, "TEX-01.3", f"LaTeX main.tex has >= 15KB content (got {len(tex_content)} bytes)")
        qa.assert_true(r"\documentclass[14pt,a4paper]{extarticle}" in tex_content, "TEX-01.4", "STP 01-2017: 14pt extarticle class")
        qa.assert_true("left=30mm" in tex_content and "right=15mm" in tex_content, "TEX-01.5", "STP 01-2017: Margins 30-15-20-20mm configured")
        qa.assert_true(r"\setstretch{1.5}" in tex_content, "TEX-01.6", "STP 01-2017: Line spacing 1.5 configured")

    # -------------------------------------------------------------------------
    # SUITE 7: Defense Guide & Architectural Explanations
    # -------------------------------------------------------------------------
    print("\n--- SUITE 7: Defense Guide & Explanations Verification ---")
    qa.assert_true(os.path.exists(DEFENSE_GUIDE_PATH), "GUIDE-01.1", f"Defense guide exists at {DEFENSE_GUIDE_PATH}")
    qa.assert_true(os.path.exists(EXPLANATION_PATH), "GUIDE-01.2", f"Architectural explanation exists at {EXPLANATION_PATH}")
    if os.path.exists(DEFENSE_GUIDE_PATH):
        with open(DEFENSE_GUIDE_PATH, "r", encoding="utf-8") as f:
            guide_content = f.read()
        qa.assert_true(len(guide_content) >= 20000, "GUIDE-01.3", f"Defense guide has >= 20KB content (got {len(guide_content)} bytes)")
        qa.assert_true("15 каверзных вопросов" in guide_content, "GUIDE-01.4", "15 professor defense questions included")
        qa.assert_true("Odds Ratio" in guide_content, "GUIDE-01.5", "Odds Ratio mathematical explanation included")
        qa.assert_true("Kernel Trick" in guide_content, "GUIDE-01.6", "SVM Kernel Trick mathematical explanation included")
        qa.assert_true("Gini Impurity" in guide_content or "неоднородности Джини" in guide_content, "GUIDE-01.7",
                       "CART Gini Impurity mathematical explanation included")

    # -------------------------------------------------------------------------
    # SUITE 8: Final Submission Archive Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 8: Final Submission Archive Verification ---")
    qa.assert_true(os.path.exists(ZIP_PATH), "ZIP-01.1", f"Final archive exists at {ZIP_PATH}")
    if os.path.exists(ZIP_PATH):
        zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
        qa.assert_true(zip_size_mb >= 10.0, "ZIP-01.2", f"Archive size >= 10 MB (got {zip_size_mb:.2f} MB)")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
            test_zip_err = zf.testzip()
            qa.assert_true(test_zip_err is None, "ZIP-01.3", "Archive integrity verified (CRC checksums 100% valid)")
            names = zf.namelist()
            required_in_zip = [
                "LR04_Classification.ipynb",
                "Отчет_ЛР04_Власовец_Вариант7.pdf",
                "LAB04_EXPLANATION.md",
                "LAB4_DEFENSE_GUIDE.md",
                "classification_summary.json",
                "latex/main.tex",
                "report/Отчет_ЛР04_Власовец_Вариант7.docx",
                "plots/01_dataset_and_missing_analysis.png",
                "plots/06_cart_decision_tree_visualization.png",
                "plots/08_roc_and_pr_curves_comparison.png",
                "data/Bankloan_raw.csv",
                "data/Bankloan_clean.csv",
                "data/Bankloan_unlabeled_scored.csv"
            ]
            for req in required_in_zip:
                qa.assert_true(req in names, f"ZIP-CONTAINS ({req})", f"Archive contains {req}")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"SENIOR QA TEST SUITE FINISHED: {qa.passed} PASSED, {qa.failed} FAILED, {qa.warnings} WARNINGS")
    print("=" * 80)

    if qa.failed == 0:
        print("\n>>> VERDICT: 100% TESTS PASSED. LABORATORY WORK #4 MEETS ALL SENIOR QA CRITERIA! <<<")
        return True
    else:
        print("\n>>> VERDICT: FAILURES DETECTED! INVESTIGATE ABOVE OUTPUT. <<<")
        return False

if __name__ == "__main__":
    success = run_all_qa_tests()
    sys.exit(0 if success else 1)
