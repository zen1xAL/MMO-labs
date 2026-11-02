"""
Automated Senior QA Test Suite for MMO Laboratory Work #2.
Conducts full-cycle verification of data integrity, pipeline logic,
feature engineering, encodings, scalings, visualizations, notebook, reports, and archive.
"""

import os
import sys
import json
import zipfile
import numpy as np
import pandas as pd
from PIL import Image

BASE_DIR = r"d:\MMO\lab2"
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
RAW_DATA_PATH = os.path.join(BASE_DIR, "StudentPerformanceFactors", "StudentPerformanceFactors.csv")
PREP_DATA_PATH = os.path.join(BASE_DIR, "StudentPerformance_Preprocessed.csv")
NOTEBOOK_PATH = os.path.join(BASE_DIR, "LR02_EDA_StudentPerformance.ipynb")
DOCX_PATH = os.path.join(BASE_DIR, "report", "Отчет_ЛР02_Власовец.docx")
PDF_PATH = os.path.join(BASE_DIR, "Отчет_ЛР02_Власовец.pdf")
ZIP_PATH = os.path.join(BASE_DIR, "LR02_Vlasovets.zip")

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
    print("=" * 70)
    print("STARTING SENIOR QA TEST SUITE: MMO LAB 2 (EDA & DATA PREPARATION)")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # SUITE 1: Raw Dataset Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 1: Raw Dataset Integrity ---")
    qa.assert_true(os.path.exists(RAW_DATA_PATH), "DATA-01.1", f"Raw data file exists at {RAW_DATA_PATH}")
    if os.path.exists(RAW_DATA_PATH):
        df_raw = pd.read_csv(RAW_DATA_PATH)
        qa.assert_true(df_raw.shape == (6607, 20), "DATA-01.2", f"Raw shape is (6607, 20), got {df_raw.shape}")
        
        missing = df_raw.isnull().sum()
        missing_dict = missing[missing > 0].to_dict()
        expected_missing = {"Teacher_Quality": 78, "Parental_Education_Level": 90, "Distance_from_Home": 67}
        qa.assert_true(missing_dict == expected_missing, "DATA-01.3", 
                       f"Missing values match {expected_missing}, got {missing_dict}")
        
        # Outlier count in raw
        q1_hours, q3_hours = df_raw["Hours_Studied"].quantile(0.25), df_raw["Hours_Studied"].quantile(0.75)
        iqr_hours = q3_hours - q1_hours
        hours_outliers = int(((df_raw["Hours_Studied"] < q1_hours - 1.5 * iqr_hours) | 
                              (df_raw["Hours_Studied"] > q3_hours + 1.5 * iqr_hours)).sum())
        qa.assert_true(hours_outliers == 43, "DATA-01.4", f"Hours_Studied has 43 outliers, got {hours_outliers}")
        
        exam_max = df_raw["Exam_Score"].max()
        qa.assert_true(exam_max == 101, "DATA-01.5", f"Raw Exam_Score max is 101 (anomaly identified), got {exam_max}")

    # -------------------------------------------------------------------------
    # SUITE 2: Preprocessed Dataset Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 2: Preprocessed Dataset & Pipeline Transformations ---")
    qa.assert_true(os.path.exists(PREP_DATA_PATH), "DATA-02.1", f"Preprocessed CSV exists at {PREP_DATA_PATH}")
    if os.path.exists(PREP_DATA_PATH):
        df_prep = pd.read_csv(PREP_DATA_PATH)
        qa.assert_true(df_prep.shape == (6607, 31), "DATA-02.2", f"Preprocessed shape is (6607, 31), got {df_prep.shape}")
        qa.assert_true(df_prep.isnull().sum().sum() == 0, "DATA-02.3", "Zero missing values in preprocessed dataset")
        
        # Check winsorization bounds
        qa.assert_true(df_prep["Hours_Studied"].min() >= 4.0 and df_prep["Hours_Studied"].max() <= 36.0,
                       "DATA-02.4", f"Hours_Studied within [4, 36]: [{df_prep['Hours_Studied'].min()}, {df_prep['Hours_Studied'].max()}]")
        qa.assert_true(df_prep["Tutoring_Sessions"].min() >= 0.0 and df_prep["Tutoring_Sessions"].max() <= 3.0,
                       "DATA-02.5", f"Tutoring_Sessions within [0, 3]: [{df_prep['Tutoring_Sessions'].min()}, {df_prep['Tutoring_Sessions'].max()}]")
        qa.assert_true(df_prep["Exam_Score"].min() >= 59.0 and df_prep["Exam_Score"].max() <= 75.0,
                       "DATA-02.6", f"Exam_Score within [59, 75]: [{df_prep['Exam_Score'].min()}, {df_prep['Exam_Score'].max()}]")
        
        # Check Feature Engineering
        qa.assert_true("Study_to_Sleep_Ratio" in df_prep.columns, "FE-01.1", "Study_to_Sleep_Ratio column present")
        qa.assert_true("Academic_Effort_Index" in df_prep.columns, "FE-01.2", "Academic_Effort_Index column present")
        qa.assert_true("Score_Growth" in df_prep.columns, "FE-01.3", "Score_Growth column present")
        
        # Check formula accuracy on sample
        recalc_ratio = np.round(df_prep["Hours_Studied"] / df_prep["Sleep_Hours"], 2)
        diff_ratio = np.abs(df_prep["Study_to_Sleep_Ratio"] - recalc_ratio).max()
        qa.assert_true(diff_ratio < 0.02, "FE-01.4", f"Study_to_Sleep_Ratio calculation matches formula (max diff {diff_ratio})")

        # Check binary encodings
        for col in ["Gender", "Extracurricular_Activities", "Internet_Access", "Learning_Disabilities", "School_Type"]:
            vals = set(df_prep[col].unique())
            qa.assert_true(vals.issubset({0, 1}), "ENC-01", f"Binary column {col} has values in {{0, 1}}, got {vals}")

        # Check OHE dummy columns (16 dummy cols for 8 categories)
        ohe_prefixes = ['Parental_Involvement', 'Access_to_Resources', 'Motivation_Level',
                        'Family_Income', 'Teacher_Quality', 'Peer_Influence',
                        'Parental_Education_Level', 'Distance_from_Home']
        for pref in ohe_prefixes:
            matching = [c for c in df_prep.columns if c.startswith(pref + "_")]
            qa.assert_true(len(matching) == 2, f"ENC-02 ({pref})", f"Category {pref} produced 2 dummy columns, got {len(matching)}: {matching}")

    # -------------------------------------------------------------------------
    # SUITE 3: Plot Assets & Visual Quality
    # -------------------------------------------------------------------------
    print("\n--- SUITE 3: Plot Quality & Visual Verification ---")
    plot_files = [
        ("01_missing_values_heatmap_before.png", "Missing Values Before"),
        ("02_numeric_distributions_before.png", "Distributions Before"),
        ("03_numeric_boxplots_before.png", "BoxPlots Before"),
        ("04_missing_values_heatmap_after.png", "Missing Values After (Validation)"),
        ("05_numeric_boxplots_after.png", "BoxPlots After"),
        ("06_numeric_distributions_after.png", "Distributions After"),
        ("07_new_features_distributions.png", "New Features Distributions"),
        ("08_scaling_comparison.png", "Scaling Comparison"),
        ("09_correlation_matrix_heatmap.png", "Correlation Matrix")
    ]
    for p_file, desc in plot_files:
        p_path = os.path.join(PLOTS_DIR, p_file)
        exists = os.path.exists(p_path)
        qa.assert_true(exists, f"VIS-01 ({p_file})", f"{desc} exists in plots/")
        if exists:
            im = Image.open(p_path)
            width, height = im.size
            qa.assert_true(width >= 2500 and height >= 1400, f"VIS-02 ({p_file})", 
                           f"High resolution 300 DPI verified: {width}x{height}")
            im.close()

    # -------------------------------------------------------------------------
    # SUITE 4: Jupyter Notebook Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 4: Jupyter Notebook Execution & Completeness ---")
    qa.assert_true(os.path.exists(NOTEBOOK_PATH), "NOTE-01.1", f"Notebook file exists at {NOTEBOOK_PATH}")
    if os.path.exists(NOTEBOOK_PATH):
        with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
            nb = json.load(f)
        qa.assert_true("cells" in nb and len(nb["cells"]) >= 15, "NOTE-01.2", f"Notebook has {len(nb.get('cells', []))} cells")
        
        # Check monotonic execution counts
        code_cells = [c for c in nb["cells"] if c.get("cell_type") == "code"]
        exec_counts = [c.get("execution_count") for c in code_cells]
        is_monotonic = all(exec_counts[i] == i + 1 for i in range(len(exec_counts)))
        qa.assert_true(is_monotonic, "NOTE-01.3", f"Code cells execution counts are clean 1..N: {exec_counts}")

        # Check outputs presence
        has_empty_outputs = any(len(c.get("outputs", [])) == 0 for c in code_cells)
        qa.assert_true(not has_empty_outputs, "NOTE-01.4", "All code cells contain outputs (no unexecuted cells)")

        # Check embedded images count
        imgs_found = 0
        for c in code_cells:
            for out in c.get("outputs", []):
                if "data" in out and "image/png" in out["data"]:
                    imgs_found += 1
        qa.assert_true(imgs_found == 9, "NOTE-01.5", f"Notebook embeds all 9 pipeline plots: {imgs_found}/9")

        # Check scaled dataset
        scaled_path = os.path.join(BASE_DIR, "StudentPerformance_Scaled.csv")
        qa.assert_true(os.path.exists(scaled_path), "DATA-02.7", "Scaled dataset StudentPerformance_Scaled.csv exists")

    # -------------------------------------------------------------------------
    # SUITE 5: Report (DOCX & PDF) Verification
    # -------------------------------------------------------------------------
    print("\n--- SUITE 5: Academic Report Compliance (BSUIR STP 01-2017) ---")
    qa.assert_true(os.path.exists(DOCX_PATH), "DOC-01.1", f"DOCX report exists: {DOCX_PATH}")
    qa.assert_true(os.path.exists(PDF_PATH), "DOC-01.2", f"PDF report exists: {PDF_PATH}")
    if os.path.exists(PDF_PATH):
        pdf_size = os.path.getsize(PDF_PATH)
        qa.assert_true(pdf_size > 500000, "DOC-01.3", f"PDF report size is valid: {pdf_size / 1024 / 1024:.2f} MB")

    # -------------------------------------------------------------------------
    # SUITE 6: Final Archive Integrity
    # -------------------------------------------------------------------------
    print("\n--- SUITE 6: Final Submission Archive (ZIP) ---")
    qa.assert_true(os.path.exists(ZIP_PATH), "ARCH-01.1", f"Submission ZIP archive exists: {ZIP_PATH}")
    if os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, "r") as z:
            names = z.namelist()
            qa.assert_true("LR02_EDA_StudentPerformance.ipynb" in names, "ARCH-01.2", "Notebook present in ZIP")
            pdf_names = [n for n in names if n.endswith(".pdf")]
            qa.assert_true(len(pdf_names) >= 1, "ARCH-01.3", f"PDF report present in ZIP: {pdf_names}")
            qa.assert_true("StudentPerformance_Preprocessed.csv" in names, "ARCH-01.5", "Preprocessed CSV in ZIP")
            qa.assert_true("StudentPerformance_Scaled.csv" in names, "ARCH-01.6", "Scaled CSV in ZIP")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"QA TEST RUN COMPLETED: {qa.passed} PASSED, {qa.failed} FAILED, {qa.warnings} WARNINGS")
    print("=" * 70)
    return qa

if __name__ == "__main__":
    res = run_all_qa_tests()
    if res.failed > 0:
        sys.exit(1)
    sys.exit(0)
