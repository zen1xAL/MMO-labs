"""
Automated Senior QA Test Suite for MMO Laboratory Work #3.
Conducts full-cycle verification of data integrity, mathematical optimizers (BGD, SGD),
Variant 7 (L2 Regularization / Ridge Regression), visualizations, notebook, reports, and archive
strictly according to BSUIR STP 01-2017 and mmo-lab-qa methodology.
"""

import os
import sys
import json
import zipfile
import numpy as np
import pandas as pd
from PIL import Image

# Reconfigure stdout for utf-8 display
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\MMO\lab3"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
LATEX_PLOTS_DIR = os.path.join(BASE_DIR, "latex", "plots")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_regression_raw.csv")
SCALED_DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_regression_scaled.csv")
NOTEBOOK_PATH = os.path.join(BASE_DIR, "LR03_Gradient_Descent.ipynb")
DOCX_PATH = os.path.join(BASE_DIR, "report", "Отчет_ЛР03_Власовец_Вариант7.docx")
PDF_PATH = os.path.join(BASE_DIR, "Отчет_ЛР03_Власовец_Вариант7.pdf")
LATEX_PATH = os.path.join(BASE_DIR, "latex", "main.tex")
SUMMARY_PATH = os.path.join(BASE_DIR, "gd_summary.json")
ZIP_PATH = os.path.join(BASE_DIR, "LR03_Vlasovets_Variant7.zip")

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
    print("=" * 75)
    print("STARTING SENIOR QA TEST SUITE: MMO LAB 3 (GRADIENT DESCENT & REGULARIZATION)")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # SUITE 1: Synthetic Dataset & Preprocessing Integrity
    # -------------------------------------------------------------------------
    print("\n--- SUITE 1: Synthetic Dataset & Preprocessing Integrity ---")
    qa.assert_true(os.path.exists(RAW_DATA_PATH), "DATA-01.1", f"Raw synthetic data exists at {RAW_DATA_PATH}")
    if os.path.exists(RAW_DATA_PATH):
        df_raw = pd.read_csv(RAW_DATA_PATH)
        qa.assert_true(df_raw.shape == (1000, 3), "DATA-01.2", f"Raw shape is (1000, 3) [Feature_1, Feature_2, Target_y], got {df_raw.shape}")
        qa.assert_true(set(df_raw.columns) == {"Feature_1", "Feature_2", "Target_y"}, "DATA-01.3", f"Columns match [Feature_1, Feature_2, Target_y], got {list(df_raw.columns)}")
        qa.assert_true(df_raw.isnull().sum().sum() == 0, "DATA-01.4", "Zero missing values in synthetic raw dataset")

    qa.assert_true(os.path.exists(SCALED_DATA_PATH), "DATA-02.1", f"Scaled data exists at {SCALED_DATA_PATH}")
    if os.path.exists(SCALED_DATA_PATH):
        df_scaled = pd.read_csv(SCALED_DATA_PATH)
        qa.assert_true(df_scaled.shape == (1000, 3), "DATA-02.2", f"Scaled shape is (1000, 3), got {df_scaled.shape}")
        qa.assert_true(set(df_scaled.columns) == {"Feature_1_scaled", "Feature_2_scaled", "Target_y"},
                       "DATA-02.3", f"Scaled columns match [Feature_1_scaled, Feature_2_scaled, Target_y], got {list(df_scaled.columns)}")
        qa.assert_true(abs(df_scaled["Feature_1_scaled"].mean()) < 1e-12, "DATA-02.4", f"Feature_1 scaled mean is ~0 ({df_scaled['Feature_1_scaled'].mean():.2e})")
        qa.assert_true(abs(df_scaled["Feature_2_scaled"].mean()) < 1e-12, "DATA-02.5", f"Feature_2 scaled mean is ~0 ({df_scaled['Feature_2_scaled'].mean():.2e})")
        qa.assert_true(abs(df_scaled["Feature_1_scaled"].std() - 1.0) < 1e-3, "DATA-02.6", f"Feature_1 scaled std is 1.0 ({df_scaled['Feature_1_scaled'].std():.4f})")
        qa.assert_true(abs(df_scaled["Feature_2_scaled"].std() - 1.0) < 1e-3, "DATA-02.7", f"Feature_2 scaled std is 1.0 ({df_scaled['Feature_2_scaled'].std():.4f})")

    # -------------------------------------------------------------------------
    # SUITE 2: Mathematical Optimizers & Photo Formulas
    # -------------------------------------------------------------------------
    print("\n--- SUITE 2: Mathematical Optimizers & Exact Convergence ---")
    qa.assert_true(os.path.exists(SUMMARY_PATH), "MATH-01.1", f"Summary JSON exists at {SUMMARY_PATH}")
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            summary = json.load(f)

        # Check analytical OLS
        ols_w = summary["analytical_weights"]
        qa.assert_true(len(ols_w) == 3, "MATH-01.2", f"OLS weights has length 3 [bias, w1, w2], got {len(ols_w)}")
        qa.assert_true(abs(ols_w[0] - 1.7660) < 0.01, "MATH-01.3", f"OLS bias w0 ~ 1.766, got {ols_w[0]:.4f}")
        qa.assert_true(abs(ols_w[1] - 39.4725) < 0.01, "MATH-01.4", f"OLS w1 ~ 39.472, got {ols_w[1]:.4f}")
        qa.assert_true(abs(ols_w[2] - 6.8970) < 0.01, "MATH-01.5", f"OLS w2 ~ 6.897, got {ols_w[2]:.4f}")

        # Check BGD convergence
        bgd = summary["bgd_results"]
        qa.assert_true(bgd["iterations"] == 124, "MATH-02.1", f"BGD converged in exactly 124 iterations, got {bgd['iterations']}")
        qa.assert_true(abs(bgd["final_mse"] - 96.85) < 0.2, "MATH-02.2", f"BGD final MSE ~ 96.85, got {bgd['final_mse']:.4f}")
        qa.assert_true(bgd["converged"] is True, "MATH-02.3", "BGD reached stopping criterion ||w^k - w^{k-1}|| < eps")
        qa.assert_true(bgd["diff_from_analytical"] < 1e-4, "MATH-02.4", f"BGD weight diff to OLS < 1e-4, got {bgd['diff_from_analytical']:.2e}")

        # Check SGD
        sgd = summary["sgd_results"]
        qa.assert_true(sgd["iterations"] == 1500, "MATH-03.1", f"SGD executed 1500 iterations, got {sgd['iterations']}")
        qa.assert_true(abs(sgd["final_mse"] - 100.52) < 2.0, "MATH-03.2", f"SGD train MSE ~ 100.52, got {sgd['final_mse']:.4f}")

        # Check Learning rates
        qa.assert_true(summary["learning_rates_tested"] == [0.001, 0.01, 0.05, 0.1, 0.5],
                       "MATH-04.1", "Learning rates tested include 0.001, 0.01, 0.05, 0.1, 0.5")

    # -------------------------------------------------------------------------
    # SUITE 3: Variant 7 (L2 Regularization / Ridge) Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 3: Variant 7 (L2 Regularization / Ridge) Verification ---")
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            summary = json.load(f)
        
        l2_meta = summary["l2_regularization"]
        qa.assert_true(l2_meta["variant"] == 7, "VAR7-01.1", f"Variant is 7, got {l2_meta['variant']}")
        qa.assert_true(l2_meta["type"] == "L2 Ridge", "VAR7-01.2", f"Type is L2 Ridge, got {l2_meta['type']}")
        qa.assert_true(l2_meta["lambdas_count"] == 20, "VAR7-01.3", f"Lambdas count is 20, got {l2_meta['lambdas_count']}")
        qa.assert_true(l2_meta["lambda_min"] == 0.001, "VAR7-01.4", f"Min lambda is 0.001, got {l2_meta['lambda_min']}")
        qa.assert_true(l2_meta["lambda_max"] == 1000.0, "VAR7-01.5", f"Max lambda is 1000.0, got {l2_meta['lambda_max']}")

        # Verify initial and final norms
        w_min = np.array(l2_meta["w_at_lambda_min"][1:])
        w_max = np.array(l2_meta["w_at_lambda_max"][1:])
        norm_min = float(np.linalg.norm(w_min))
        norm_max = float(np.linalg.norm(w_max))
        qa.assert_true(norm_min > 40.0, "VAR7-01.6", f"Norm at lambda=0.001 is ~40.03, got {norm_min:.4f}")
        qa.assert_true(norm_max < 0.05, "VAR7-01.7", f"Norm at lambda=1000 is ~0.04, got {norm_max:.4f}")
        qa.assert_true(norm_min > norm_max, "VAR7-01.8", "L2 penalty successfully shrunk weights towards zero")

        # Verify bias is unpenalized
        bias_min = l2_meta["w_at_lambda_min"][0]
        bias_max = l2_meta["w_at_lambda_max"][0]
        qa.assert_true(abs(bias_min - bias_max) < 1e-10, "VAR7-01.9", f"Bias w0 unpenalized ({bias_min:.4f} vs {bias_max:.4f})")

    # -------------------------------------------------------------------------
    # SUITE 4: Visualizations Quality Assurance (300 DPI)
    # -------------------------------------------------------------------------
    print("\n--- SUITE 4: Visualizations Quality Assurance (300 DPI) ---")
    plot_files = [
        "01_dataset_regression_structure.png",
        "02_bgd_convergence_trajectory.png",
        "03_learning_rate_experiments.png",
        "04_bgd_vs_sgd_comparison.png",
        "05_l2_regularization_paths.png",
        "06_l1_vs_l2_comparison.png",
        "07_model_evaluation_residuals.png"
    ]

    for p_name in plot_files:
        p_path = os.path.join(PLOTS_DIR, p_name)
        qa.assert_true(os.path.exists(p_path), f"VIS-{p_name[:2]}.1", f"Plot {p_name} exists in plots/")
        if os.path.exists(p_path):
            file_size_kb = os.path.getsize(p_path) / 1024
            qa.assert_true(file_size_kb > 200, f"VIS-{p_name[:2]}.2", f"File size > 200 KB ({file_size_kb:.1f} KB)")
            with Image.open(p_path) as img:
                w, h = img.size
                qa.assert_true(w >= 4000 or h >= 2000, f"VIS-{p_name[:2]}.3", f"Resolution adequate for 300 DPI ({w}x{h})")

        # Check copy in latex/plots
        p_latex = os.path.join(LATEX_PLOTS_DIR, p_name)
        qa.assert_true(os.path.exists(p_latex), f"VIS-{p_name[:2]}.4", f"Plot {p_name} copied to latex/plots/")

    # -------------------------------------------------------------------------
    # SUITE 5: Jupyter Notebook Quality Assurance
    # -------------------------------------------------------------------------
    print("\n--- SUITE 5: Jupyter Notebook Quality Assurance ---")
    qa.assert_true(os.path.exists(NOTEBOOK_PATH), "NOTE-01.1", f"Notebook exists at {NOTEBOOK_PATH}")
    if os.path.exists(NOTEBOOK_PATH):
        with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
            nb = json.load(f)
        
        qa.assert_true(nb.get("nbformat") == 4, "NOTE-01.2", f"nbformat is 4, got {nb.get('nbformat')}")
        cells = nb.get("cells", [])
        qa.assert_true(len(cells) >= 15, "NOTE-01.3", f"Notebook contains >= 15 cells, got {len(cells)}")

        # Check execution count monotonicity
        exec_counts = [c.get("execution_count") for c in cells if c.get("cell_type") == "code"]
        valid_exec = [ec for ec in exec_counts if ec is not None]
        is_monotonic = all(valid_exec[i] <= valid_exec[i+1] for i in range(len(valid_exec)-1))
        qa.assert_true(is_monotonic, "NOTE-01.4", f"Execution counts are strictly sequential: {valid_exec}")

        # Check embedded images count
        embedded_img_count = 0
        error_count = 0
        for c in cells:
            if c.get("cell_type") == "code":
                for out in c.get("outputs", []):
                    if out.get("output_type") == "error":
                        error_count += 1
                    if "data" in out and "image/png" in out["data"]:
                        embedded_img_count += 1

        qa.assert_true(embedded_img_count == 7, "NOTE-01.5", f"All 7 plots embedded in outputs, got {embedded_img_count}")
        qa.assert_true(error_count == 0, "NOTE-01.6", f"Zero error outputs in notebook cells, got {error_count}")

    # -------------------------------------------------------------------------
    # SUITE 6: Academic Compliance & Document Sync (STP 01-2017)
    # -------------------------------------------------------------------------
    print("\n--- SUITE 6: Academic Compliance & Document Sync (STP 01-2017) ---")
    qa.assert_true(os.path.exists(DOCX_PATH), "DOC-01.1", f"DOCX report exists at {DOCX_PATH}")
    if os.path.exists(DOCX_PATH):
        docx_size_mb = os.path.getsize(DOCX_PATH) / (1024 * 1024)
        qa.assert_true(docx_size_mb > 2.0, "DOC-01.2", f"DOCX size > 2.0 MB ({docx_size_mb:.2f} MB)")

    qa.assert_true(os.path.exists(PDF_PATH), "DOC-02.1", f"PDF report exists at {PDF_PATH}")
    if os.path.exists(PDF_PATH):
        pdf_size_kb = os.path.getsize(PDF_PATH) / 1024
        qa.assert_true(pdf_size_kb > 500, "DOC-02.2", f"PDF size > 500 KB ({pdf_size_kb:.1f} KB)")

    qa.assert_true(os.path.exists(LATEX_PATH), "DOC-03.1", f"LaTeX main.tex exists at {LATEX_PATH}")
    if os.path.exists(LATEX_PATH):
        with open(LATEX_PATH, "r", encoding="utf-8") as f:
            tex_content = f.read()
        qa.assert_true("Вариант 7" in tex_content or "Вариант 7 (нечетный)" in tex_content or "Вариант 7" in tex_content,
                       "DOC-03.2", "LaTeX contains Variant 7")
        qa.assert_true("Власовец" in tex_content, "DOC-03.3", "LaTeX contains student name Vlasovets")
        qa.assert_true("Лебедевич" in tex_content, "DOC-03.4", "LaTeX contains teacher name Lebedevich")
        qa.assert_true("nabla Q" in tex_content, "DOC-03.5", "LaTeX contains Gradient Descent Photo 1 formula")
        qa.assert_true("varepsilon" in tex_content, "DOC-03.6", "LaTeX contains Photo 2 stopping condition")

    # -------------------------------------------------------------------------
    # SUITE 7: Final Release Archive & Packaging
    # -------------------------------------------------------------------------
    print("\n--- SUITE 7: Final Release Archive & Packaging ---")
    qa.assert_true(os.path.exists(ZIP_PATH), "ARCH-01.1", f"Final ZIP archive exists at {ZIP_PATH}")
    if os.path.exists(ZIP_PATH):
        zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
        qa.assert_true(zip_size_mb > 10.0, "ARCH-01.2", f"ZIP archive size > 10 MB ({zip_size_mb:.2f} MB)")
        
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zip_names = zf.namelist()
            required_in_zip = [
                "LR03_Gradient_Descent.ipynb",
                "Отчет_ЛР03_Власовец_Вариант7.pdf",
                "LAB03_EXPLANATION.md",
                "gd_summary.json",
                "latex/main.tex",
                "report/Отчет_ЛР03_Власовец_Вариант7.docx"
            ]
            for req in required_in_zip:
                # Handle path separators
                found = any(req.replace("\\", "/") == z.replace("\\", "/") for z in zip_names)
                qa.assert_true(found, f"ARCH-01.3-{os.path.basename(req)}", f"File {req} present in archive")

            # Check no junk
            has_pyc = any(z.endswith(".pyc") or "__pycache__" in z for z in zip_names)
            qa.assert_true(not has_pyc, "ARCH-01.4", "No .pyc or __pycache__ files in archive")

    # -------------------------------------------------------------------------
    # QA SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(f"SENIOR QA VERIFICATION RESULTS: {qa.passed} PASSED | {qa.failed} FAILED | {qa.warnings} WARNINGS")
    print("=" * 75)

    if qa.failed == 0:
        print("\n>>> ACCEPTANCE STATUS: [APPROVED FOR SUBMISSION / ВЫПОЛНЕНО УСПЕШНО] <<<")
    else:
        print("\n>>> ACCEPTANCE STATUS: [REJECTED - ISSUES MUST BE FIXED] <<<")
        sys.exit(1)

if __name__ == "__main__":
    run_all_qa_tests()
