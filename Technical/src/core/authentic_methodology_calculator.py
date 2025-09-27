#!/usr/bin/env python3
"""
Authentic Methodology Calculator for Table 5.4
================================================

This script takes the authentic merged dataset (no interpolation) and computes
only those variables that are algebraically derivable from Shaikh & Tonak's
identities. It DOES NOT fabricate or interpolate any values.

Derived variables implemented (when inputs exist for a given year):
- s_u_calc (productive surplus adjusted by utilization)
- r_calc (textbook identity version of the rate of profit)
- K_unified (naming harmonization of KK and K; no inference)
- gK_from_K_unified (discrete growth; diagnostic only)
- r_sp_over_Ku (profit rate candidate consistent with published r')
- V_from_SP, C_from_SP (derived from SP and s', c')
- V_from_S,  C_from_S  (alternative path using S and s', c')

Outputs:
- src/analysis/replication/output/table_5_4_authentic_calculated.csv
- src/analysis/replication/output/authentic_validation_summary.json
- src/analysis/replication/output/AUTHENTIC_FORMULAS_REFERENCE.md

Formulas and Conditions (no interpolation)
-----------------------------------------
Symbols below refer to columns in the authentic dataset:
- s' (rate of surplus value), c' (organic composition of capital), u (capacity utilization)
- SP (surplus product measure), S (surplus), K (capital), KK (capital Part 1)

1) Utilization-adjusted surplus
    s_u_calc_t = s'_t × u_t
    Domain: s' and u both present; else NaN.

2) Identity profit rate (textbook Marxian identity)
    r_calc_t = s'_t / (1 + c'_t)
    Domain: c' present and (1+c') ≠ 0; else NaN.
    Note: This does NOT match the published r' in Table 5.4 using the extracted s' and c'.

3) Unified capital naming (no inference)
    K_unified_t = KK_t if KK_t is present; else K_t if present; else NaN.
    Domain: Uses whichever series is present in that year; does not fill gaps.

4) Diagnostic growth from unified capital
    gK_from_K_unified_t = (K_unified_t − K_unified_{t−1}) / K_unified_{t−1}
    Domain: Requires consecutive years with K_unified; else NaN.
    Note: Provided for comparison; may differ from book gK per definitional choices.

5) Profit rate candidate consistent with published r'
    r_sp_over_Ku_t = SP_t / (K_unified_t × u_t)
    Domain: SP, K_unified, u present and K_unified×u ≠ 0; else NaN.
    Validation indicates close alignment with published r'.

6) Derivations of V and C via SP
    V_from_SP_t = SP_t / s'_t,  C_from_SP_t = c'_t × V_from_SP_t
    Domain: s' present and s' ≠ 0; c' present for C_from_SP; else NaN.

7) Alternative derivations via S
    V_from_S_t  = S_t  / s'_t,  C_from_S_t  = c'_t × V_from_S_t
    Domain: s' present and s' ≠ 0; c' present for C_from_S; else NaN.

8) Diagnostic checks using V and C
    r_from_cv(SP)_t = SP_t / (C_from_SP_t + V_from_SP_t)
    r_from_cv(S)_t  =  S_t / (C_from_S_t  + V_from_S_t)
    Used only for validation; not exported to the final table.

General policy: If inputs are missing or denominators are zero, results are NaN. No interpolation or smoothing is performed.
"""

from pathlib import Path
from textwrap import dedent
from typing import Dict, Any
import pandas as pd
import numpy as np
import json

AUTHENTIC_RAW_PATH = Path("src/analysis/replication/output/table_5_4_authentic_raw_merged.csv")
OUTPUT_DIR = Path("src/analysis/replication/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FORMULAS_MD_PATH = OUTPUT_DIR / "AUTHENTIC_FORMULAS_REFERENCE.md"


def load_authentic_raw() -> pd.DataFrame:
    """Load the authentic raw merged dataset and return with years as index."""
    df = pd.read_csv(AUTHENTIC_RAW_PATH, index_col=0)
    # Raw file has variables as rows and years as columns; transpose to years rows
    df = df.T
    # Columns become variable names; ensure consistent dtype
    df.index.name = "year"
    # Coerce year index to int where possible
    try:
        df.index = df.index.astype(int)
    except Exception:
        pass
    # Convert all numeric-like values to floats
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def compute_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Compute algebraically derivable variables without interpolation."""
    out = df.copy()

    # 1) s_u = s' * u (part2 shows row "s'«u" which equals s' * u)
    if "s'" in out.columns and "u" in out.columns:
        out["s_u_calc"] = out["s'"] * out["u"]

    # 2) r by identity: r = s' / (1 + c')
    if "s'" in out.columns and "c'" in out.columns:
        denom = 1.0 + out["c'"]
        out["r_calc"] = np.where(denom != 0, out["s'"] / denom, np.nan)

    # 3) Unify K: use KK for early years, K for later years (naming harmonization)
    # Note: We do NOT infer missing values; we only pick what's present per period.
    k_unified = pd.Series(index=out.index, dtype=float)
    if "KK" in out.columns:
        k_unified.loc[out.index] = np.where(~out["KK"].isna(), out["KK"], np.nan)
    if "K" in out.columns:
        # Prefer K where available (later years)
        k_unified.loc[out.index] = np.where(~out["K"].isna(), out["K"], k_unified)
    if not k_unified.isna().all():
        out["K_unified"] = k_unified

    # 4) gK_from_K_unified: simple discrete growth from K_unified (comparison only)
    if "K_unified" in out.columns:
        out["gK_from_K_unified"] = out["K_unified"].pct_change()

    # 5) Profit rate candidate consistent with published r': r ≈ SP / (K * u)
    # Compute only when SP, K_unified, and u are present. Do not fill gaps.
    if all(col in out.columns for col in ["SP", "K_unified", "u"]):
        denom = out["K_unified"] * out["u"]
        out["r_sp_over_Ku"] = np.where(denom != 0, out["SP"] / denom, np.nan)

    # 6) Derive V and C from s' and c' using SP (and alternatively S) when available
    # Using s' = SP / V  =>  V = SP / s'; then C = c' * V. Do not fill gaps.
    if all(col in out.columns for col in ["SP", "s'"]):
        sprime = out["s'"]
        out["V_from_SP"] = np.where(sprime != 0, out["SP"] / sprime, np.nan)
        if "c'" in out.columns:
            out["C_from_SP"] = out["c'"] * out["V_from_SP"]

    # Alternative path using S: V = S / s'; C = c' * V
    if all(col in out.columns for col in ["S", "s'"]):
        sprime = out["s'"]
        out["V_from_S"] = np.where(sprime != 0, out["S"] / sprime, np.nan)
        if "c'" in out.columns:
            out["C_from_S"] = out["c'"] * out["V_from_S"]

    return out


def write_formulas_reference_md() -> None:
     """Write a Markdown reference of all formulas and their domains to the output folder."""
     md = dedent(
          """
          # Authentic Formulas Reference for Table 5.4

          This reference lists the algebraic identities used in the authentic phase. No interpolation is applied; missing inputs yield missing outputs.

          Notation: s' (rate of surplus value), c' (organic composition), u (capacity utilization), SP (surplus product), S (surplus), K/KK (capital stock).

          1) Utilization-adjusted surplus
              s_u_calc_t = s'_t × u_t
              Domain: s' and u present.

          2) Identity profit rate (textbook)
              r_calc_t = s'_t / (1 + c'_t)
              Domain: c' present and (1+c') ≠ 0.

          3) Unified capital naming (no inference)
              K_unified_t = KK_t if present, else K_t if present, else NaN.

          4) Diagnostic capital growth
              gK_from_K_unified_t = (K_unified_t − K_unified_{t−1}) / K_unified_{t−1}

          5) Profit rate candidate consistent with published r'
              r_sp_over_Ku_t = SP_t / (K_unified_t × u_t)

          6) Derivations via SP
              V_from_SP_t = SP_t / s'_t
              C_from_SP_t = c'_t × V_from_SP_t

          7) Alternative derivations via S
              V_from_S_t = S_t / s'_t
              C_from_S_t = c'_t × V_from_S_t

          8) Diagnostic checks
              r_from_cv(SP)_t = SP_t / (C_from_SP_t + V_from_SP_t)
              r_from_cv(S)_t  =  S_t / (C_from_S_t  + V_from_S_t)

          Policy: If inputs are missing or denominators are zero, results are NaN. No interpolation or smoothing is performed.
          """
     ).strip()
     FORMULAS_MD_PATH.write_text(md + "\n", encoding="utf-8")


def validate_identities(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate S&T identities where both sides exist; report errors without altering inputs."""
    results: Dict[str, Any] = {}

    # Validate s_u (if original provided under various names)
    # Part 1 uses "s'u"; Part 2 uses "s'«u". We compare both to s_u_calc when present.
    if "s_u_calc" in df.columns:
        comparisons = {}
        for candidate in ["s'u", "s'«u"]:
            if candidate in df.columns:
                diff = df[candidate] - df["s_u_calc"]
                common = diff.dropna()
                if len(common) > 0:
                    comparisons[candidate] = {
                        "observations": int(len(common)),
                        "mae": float(common.abs().mean()),
                        "max_abs_err": float(common.abs().max())
                    }
        if comparisons:
            results["s_u_identity"] = comparisons

    # Validate r identity vs reported r' (if present)
    if "r_calc" in df.columns and "r'" in df.columns:
        diff = df["r'"] - df["r_calc"]
        common = diff.dropna()
        if len(common) > 0:
            results["r_identity"] = {
                "observations": int(len(common)),
                "mae": float(common.abs().mean()),
                "max_abs_err": float(common.abs().max()),
            }

    # Compare published gK with growth from K_unified (informational only)
    if "gK" in df.columns and "gK_from_K_unified" in df.columns:
        diff = df["gK"] - df["gK_from_K_unified"]
        common = diff.dropna()
        if len(common) > 0:
            results["gK_vs_growth_from_K_unified"] = {
                "observations": int(len(common)),
                "mae": float(common.abs().mean()),
                "max_abs_err": float(common.abs().max())
            }

    # Validate r' vs SP/(K*u) candidate
    if "r'" in df.columns and "r_sp_over_Ku" in df.columns:
        diff = df["r'"] - df["r_sp_over_Ku"]
        common = diff.dropna()
        if len(common) > 0:
            results["r_vs_sp_over_Ku"] = {
                "observations": int(len(common)),
                "mae": float(common.abs().mean()),
                "max_abs_err": float(common.abs().max())
            }

    # Validate r' vs SP/(C_from_SP + V_from_SP)
    if "r'" in df.columns and all(col in df.columns for col in ["SP", "C_from_SP", "V_from_SP"]):
        denom = df["C_from_SP"] + df["V_from_SP"]
        with np.errstate(divide='ignore', invalid='ignore'):
            r_from_cv = np.where(denom != 0, df["SP"] / denom, np.nan)
        diff = df["r'"] - r_from_cv
        common = pd.Series(r_from_cv, index=df.index).dropna().index.intersection(df["r'"] .dropna().index)
        if len(common) > 0:
            errs = (df.loc[common, "r'"] - pd.Series(r_from_cv, index=df.index).loc[common]).abs()
            results["r_vs_sp_over_CplusV_from_SP"] = {
                "observations": int(len(common)),
                "mae": float(errs.mean()),
                "max_abs_err": float(errs.max())
            }

    # Validate r' vs S/(C_from_S + V_from_S)
    if "r'" in df.columns and all(col in df.columns for col in ["S", "C_from_S", "V_from_S"]):
        denom = df["C_from_S"] + df["V_from_S"]
        with np.errstate(divide='ignore', invalid='ignore'):
            r_from_cv_s = np.where(denom != 0, df["S"] / denom, np.nan)
        diff = df["r'"] - r_from_cv_s
        common = pd.Series(r_from_cv_s, index=df.index).dropna().index.intersection(df["r'"] .dropna().index)
        if len(common) > 0:
            errs = (df.loc[common, "r'"] - pd.Series(r_from_cv_s, index=df.index).loc[common]).abs()
            results["r_vs_s_over_CplusV_from_S"] = {
                "observations": int(len(common)),
                "mae": float(errs.mean()),
                "max_abs_err": float(errs.max())
            }

    return results


def main() -> None:
    df = load_authentic_raw()
    calculated = compute_derived(df)

    # Export calculated dataset
    out_path = OUTPUT_DIR / "table_5_4_authentic_calculated.csv"
    calculated.reset_index().to_csv(out_path, index=False)

    # Validate identities and export summary
    validation = validate_identities(calculated)
    summary = {
        "notes": [
            "No interpolation performed. Only algebraic identities applied.",
            "K_unified is a naming harmonization (KK up to 1973, K from 1974).",
            "gK_from_K_unified is provided for comparison and may differ from published gK, \n"
            "reflecting definitional differences in S&T (e.g., real vs nominal, net vs gross)."
        ],
        "variables_available": sorted(list(df.columns)),
        "variables_added": [col for col in calculated.columns if col not in df.columns],
        "validation": validation,
    }

    val_path = OUTPUT_DIR / "authentic_validation_summary.json"
    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Export formulas reference for easy review
    write_formulas_reference_md()

    print(f"Wrote calculated dataset to: {out_path}")
    print(f"Wrote validation summary to: {val_path}")
    print(f"Wrote formulas reference to: {FORMULAS_MD_PATH}")


if __name__ == "__main__":
    main()
