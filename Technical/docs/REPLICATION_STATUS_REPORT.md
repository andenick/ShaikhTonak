# Historical Replication Status Report

**Date:** September 21, 2025
**Author:** Gemini

## 1. Executive Summary

This report addresses the current status of the Shaikh & Tonak historical data replication.

**Conclusion: The current "perfect" replication is invalid.**

The dataset located at `src/analysis/replication/output/table_5_4_perfect.csv`, previously considered 100% complete, was created using extensive and methodologically inappropriate interpolation to fill significant data gaps. This has resulted in a dataset that does not authentically represent the original Shaikh & Tonak (1994) findings.

This report identifies the true, incomplete source data and outlines a clear path toward an authentic replication.

## 2. Evidence of Invalid Replication

The invalidity of the "perfect" dataset is established through three key pieces of evidence:

### 2.1. Contradictory Project Logs

Project logs falsely claim 100% data completeness was achieved via "advanced_calculation," which was in practice simple interpolation.

- **`src/analysis/replication/output/final_recovery_log.json`**: Claims to have filled all gaps in variables like `s'«u`, `gK`, and `K` to reach 100% completeness from an initial 93.9%.
- **`src/analysis/replication/output/data_completeness_analysis.json`**: Suggests "Interpolation" as a valid method to bridge a known gap for the year 1974.

### 2.2. Discovery of Authentic Source Data

The `README.md` file located in `data/extracted_tables/book_tables/` serves as a manifest for the PDF extraction process. It correctly identifies the two source files for Table 5.4, their respective data periods, and their original (incomplete) quality scores:

- **Part 1 (1958-1973):** `table_p36_camelot[page]_0.csv` (Completeness: 98%)
- **Part 2 (1974-1989):** `table_p37_camelot[page]_0.csv` (Completeness: 95%)

These files represent the **true starting point** for the replication.

### 2.3. Direct Comparison: Authentic vs. Flawed Data

A direct comparison of variable `Pn` (Nominal Prices) highlights the issue.

- **Authentic Data (Part 1):** The last recorded value for `Pn` is **258.07** in 1973.
- **Authentic Data (Part 2):** The `Pn` variable is **entirely missing**.
- **Flawed "Perfect" Data:** The value **258.07** is repeated for every year from 1973 to 1990.

This demonstrates that instead of leaving the data as missing or calculating it based on the book's methodology, the previous process simply carried the last known value forward, fabricating 17 years of data for this variable. The same issue affects numerous other variables.

## 3. Proposed Plan for Authentic Replication

To rectify this, we must discard the flawed "perfect" dataset and restart the replication process from the authentic source files.

1.  **Clean and Merge Sources:**
    - Load `table_p36_camelot[page]_0.csv` and `table_p37_camelot[page]_0.csv`.
    - Clean the data (e.g., fix headers, identify unnamed rows, correct data types).
    - Align and merge them into a single, coherent dataset that accurately reflects all known data points and explicitly shows all original gaps (as `NaN` or empty values).

2.  **Methodological Deep Dive:**
    - Analyze the Shaikh & Tonak (1994) text, specifically the methodology sections referenced in the `book_tables/README.md`.
    - Extract the specific algebraic formulas used to calculate derived variables (e.g., the rate of profit `r`, the organic composition of capital `q`).

3.  **Authentic Calculation of Missing Values:**
    - Apply the extracted formulas to the cleaned dataset to calculate missing values where algebraically possible.
    - **Crucially, no linear interpolation or simple gap-filling will be used.** If a value cannot be calculated from other authentic data via the book's formulas, it will remain missing.

4.  **Generate New Deliverables:**
    - Produce a new, valid replicated dataset: `table_5_4_authentic.csv`.
    - Create a detailed report, `AUTHENTIC_REPLICATION_METHODOLOGY.md`, documenting every cleaning step, every formula applied, and a final, honest assessment of the data's completeness.

This process will result in a trustworthy and academically rigorous replication of the historical data, providing a solid foundation for the subsequent project goal of extending the analysis to the present day.

## 4. Immediate Next Steps Toward Perfect Replication

### 4.1 Completed in this phase

- Authentic export created: `src/analysis/replication/output/table_5_4_authentic.csv` (book values preserved; identity-derived columns added without interpolation)
- Summary added: `src/analysis/replication/output/AUTHENTIC_REPLICATION_SUMMARY.md`
- Integrity check: PASS (Columns checked: 18; Total mismatches: 0). Reports in `AUTHENTICITY_CHECK.md` and `authenticity_check.json`.

### 4.2 Immediate Next Steps Toward Method-Exact Replication

- Obtain exact Shaikh–Tonak definitions for r', s', c', K, SP, and gK for Table 5.4 (pages 36–37 and relevant methodological appendix). Identity r' = s'/(1+c') does not match the published r', signaling definitional nuances we must implement.
- Integrate Table 5.5 employment series to validate/augment b (productive labor share), maintaining the no-interpolation rule.
- Confirm Pn coverage 1974–1989 from book tables or the text (Part 2 extraction lacks Pn); integrate only if explicitly provided by Shaikh–Tonak.
- Recompute derived variables using authenticated definitions; re-validate identities and document remaining genuine gaps.
