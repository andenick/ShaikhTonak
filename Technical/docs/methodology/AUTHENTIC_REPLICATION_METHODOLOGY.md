# Authentic Replication Methodology for Table 5.4

**Date:** September 21, 2025
**Author:** Gemini

## 1. Objective

This document details the process of creating an authentic, methodologically sound replication of Shaikh & Tonak's (1994) Table 5.4. This process was necessitated by the discovery that the previous "perfect" replication was corrupted by improper data fabrication.

This document outlines the initial, successful step: creating a clean, merged dataset from the original source files.

## 2. Source Files

The authentic replication is based exclusively on the two raw data files identified in the `data/extracted_tables/book_tables/README.md`:

- **Part 1 (1958-1973):** `table_p36_camelot[page]_0.csv`
- **Part 2 (1974-1989):** `table_p37_camelot[page]_0.csv`

## 3. Cleaning and Merging Process

The process was executed by the script `src/analysis/replication/create_authentic_replication.py`. The key steps are as follows:

### 3.1. Loading and Cleaning Part 1 (1958-1973)

1.  **Load Data:** The file `table_p36_camelot[page]_0.csv` was loaded into a pandas DataFrame.
2.  **Identify Unnamed Row:** The row containing data `(0.049, 0.067, ...)` was identified as belonging to the variable `gK` (Growth Rate of Capital) based on its position and context. The row was explicitly renamed.
3.  **Correct Missing Value:** The value for the variable `u` (Capacity Utilization) in the year 1973 was `0.0` in the source file. This is an invalid value for this metric and was identified as a missing data point. It was converted to `NaN` to ensure mathematical correctness in future calculations.

### 3.2. Loading and Cleaning Part 2 (1974-1989)

1.  **Load Data:** The file `table_p37_camelot[page]_0.csv` was loaded.
2.  **Assign Column Headers:** The raw file was missing year headers. Based on the `README.md`, the 16 columns of data were programmatically assigned to the years 1974 through 1989.

### 3.3. Merging

1.  **Concatenation:** The two cleaned DataFrames (Part 1 and Part 2) were concatenated along the column axis.
2.  **Index Alignment:** The `concat` operation automatically aligned the data by the variable names in the index. This ensures that data for the same variable from both periods were correctly placed in the same row.
3.  **Chronological Sort:** The columns (years) were reordered to ensure a continuous timeline from 1958 to 1989.

## 4. Output: The Authentic Raw Merged Dataset

The result of this process is the file:

- **`src/analysis/replication/output/table_5_4_authentic_raw_merged.csv`**

This file represents a **truthful baseline** for the replication. It contains all the data present in the original extracted tables and correctly represents all missing data as empty cells (`NaN`).

## 5. Next Steps: Authentic Calculation

This clean dataset is now ready for the next phase of the authentic replication.

1.  **Formula Extraction:** The next step is to systematically extract the algebraic formulas from the Shaikh & Tonak (1994) text that define the relationships between the variables in Table 5.4.
2.  **Programmatic Calculation:** These formulas will be implemented in a new script to calculate the missing values based on the known, authentic data points.
3.  **Final Authentic Dataset:** The output will be a final, authentically replicated dataset that is as complete as the original methodology allows, with any remaining gaps being truly un-calculable.

## 6. Implemented Methodology-Only Calculations (No Interpolation)

As an initial step toward full methodological replication, we added a calculator that applies only algebraic identities which can be computed directly from the authentic merged data. This preserves all genuine gaps and avoids any form of interpolation.

- Script: `src/analysis/replication/authentic_methodology_calculator.py`
- Input: `src/analysis/replication/output/table_5_4_authentic_raw_merged.csv`
- Outputs:
	- `src/analysis/replication/output/table_5_4_authentic_calculated.csv`
	- `src/analysis/replication/output/authentic_validation_summary.json`

### 6.1 Identities Implemented

- Productive surplus adjusted by utilization: s_u_calc = s' × u
  - Formula: $s^{u}_{t} = s'_{t} \times u_{t}$
- Profit rate identity (textbook Marxian identity): r_calc = s' / (1 + c')
  - Formula: $r_{t} = \dfrac{s'_{t}}{1 + c'_{t}}$
- Unified capital series name: K_unified = KK (1958–1973) ∪ K (1974–1989)
  - Definition: $K^{\text{unified}}_{t} = \begin{cases} KK_{t} & \text{if } KK_{t}\ \text{present} \\ K_{t} & \text{else if } K_{t}\ \text{present} \\ \text{NaN} & \text{otherwise}\end{cases}$
- Informational growth from unified capital: gK_from_K_unified = ΔK_unified / K_unified(-1)
  - Formula: $gK^{\text{unified}}_{t} = \dfrac{K^{\text{unified}}_{t} - K^{\text{unified}}_{t-1}}{K^{\text{unified}}_{t-1}}$

No missing values were filled; identities are only computed where inputs exist for that year.

### 6.2 Validation Summary (from authentic_validation_summary.json)

- s'u vs s'×u (Part 1) — MAE ≈ 0.00345, max |err| ≈ 0.0078
- s'«u vs s'×u (Part 2) — MAE ≈ 0.00369, max |err| ≈ 0.0087
- Published gK vs growth from K_unified — MAE ≈ 0.0347 (informational only)
- Profit rate identity r' vs s'/(1+c') — MAE ≈ 0.307 (does not match)

Interpretation: The utilization-adjusted surplus identity aligns closely (differences are consistent with rounding/measurement conventions). However, the published profit rate r' does not equal $\;r_{t}=\dfrac{s'_{t}}{1+c'_{t}}\;$ using the table’s $s'$ and $c'$ series. This implies that Shaikh & Tonak’s table definitions for $s'$, $c'$, and/or $r'$ use specific measurement conventions (e.g., net vs gross, deflation choices, or category definitions) that must be read directly from the book to implement exactly. We therefore require the book’s explicit variable definitions and formula statements for Table 5.4 before proceeding to compute additional variables.

### 6.3 What We Need Next

To complete a faithful, method-based replication, please provide scans or verbatim text of the relevant sections defining Table 5.4 variables and formulas (ideally the pages around 36–37 and the methodological appendix where r', c', s', K, and SP are defined). With those precise definitions, we will:

1. Map each variable to its exact accounting definition (levels, deflation, net/gross treatment).
2. Implement the profit rate and related ratios precisely as per Shaikh & Tonak.
3. Recompute derived variables and re-validate identities without interpolation.

## 7. Final Authentic Export (No Interpolation)

- Script: `src/analysis/replication/export_final_authentic_table.py`
- Inputs:
  - `src/analysis/replication/output/table_5_4_authentic_raw_merged.csv`
  - `src/analysis/replication/output/table_5_4_authentic_calculated.csv`
  - `src/analysis/replication/output/authentic_validation_summary.json`
- Outputs:
  - `src/analysis/replication/output/table_5_4_authentic.csv`
  - `src/analysis/replication/output/AUTHENTIC_REPLICATION_SUMMARY.md`

This export preserves all original book values exactly (verifiable below) and adds only identity-based, algebraically computable series. No interpolation or smoothing is applied; genuine gaps remain NaN.

### 7.1 Identities Included in Final Export

- Utilization-adjusted surplus: $s^{u}_{t} = s'_{t} \times u_{t}$
- Variable labor (from SP): $V^{(SP)}_{t} = \dfrac{SP_{t}}{s'_{t}}$
- Constant capital (from SP): $C^{(SP)}_{t} = c'_{t} \times V^{(SP)}_{t}$
- Profit rate candidate (validated): $r^{(SP/K\cdot u)}_{t} = \dfrac{SP_{t}}{K^{\text{unified}}_{t}\, u_{t}}$, with $K^{\text{unified}} = KK \cup K$

Notes:
- The book’s `r'` column is preserved unmodified. The identity-based profit rate is exported separately as `r_prime_calc` to avoid overwriting book data.
- `gK_from_K_unified = ΔK_unified / K_unified(-1)` is kept for diagnostics (see calculated CSV), not exported in the final table.

### 7.2 Validation (Excerpt)

From `AUTHENTIC_REPLICATION_SUMMARY.md`:

- r' vs SP/(K×u): MAE = 0.002219, max |err| = 0.007456, n = 31
- s'u vs s'×u (Part 1): MAE = 0.003447, max |err| = 0.007800, n = 15
- s'«u vs s'×u (Part 2): MAE = 0.003694, max |err| = 0.008700, n = 16

### 7.3 Authenticity Integrity Check

- Script: `src/analysis/replication/verify_authentic_integrity.py`
- Compares `table_5_4_authentic.csv` against `table_5_4_authentic_raw_merged.csv` for all original book columns and years; ignores derived columns.
- Outputs:
  - `src/analysis/replication/output/authenticity_check.json`
  - `src/analysis/replication/output/AUTHENTICITY_CHECK.md`
- Result: PASS; Columns checked: 18; Total mismatches: 0 (all original book data preserved exactly).

### 7.4 Where-To-Find Summary

- Final table: `src/analysis/replication/output/table_5_4_authentic.csv`
- Summary: `src/analysis/replication/output/AUTHENTIC_REPLICATION_SUMMARY.md`
- Raw baseline (book tables merged): `src/analysis/replication/output/table_5_4_authentic_raw_merged.csv`
- Calculations (identities): `src/analysis/replication/output/table_5_4_authentic_calculated.csv`
- Integrity reports: `src/analysis/replication/output/AUTHENTICITY_CHECK.md` and `authenticity_check.json`

## 8. No-Interpolation Guarantee
---

End-of-day note (Sep 21, 2025): Completed authentic export, formula injections, validation excerpts, and integrity PASS (0 mismatches). Added formulas reference and data dictionary pointers. Next: incorporate exact book definitions for $r'$, $s'$, $c'$, $K$, $SP$, and $gK$ to move from algebraic alignment to methodology-exact replication.

All computations in this authentic phase are strictly algebraic identities applied to available book inputs. No interpolation, extrapolation, smoothing, or data fabrication has been performed. Missing values remain explicitly missing.
