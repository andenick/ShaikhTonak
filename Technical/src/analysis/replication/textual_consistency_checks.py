#!/usr/bin/env python3
"""
Textual Consistency Checks for Shaikh & Tonak (1994)
---------------------------------------------------

Validates a set of algebraic relationships referenced in the book's text
against the authentic merged data and identity-based derivations. No
interpolation is used; all checks are performed only where inputs exist.

Checks included:
1) s'u identity: s'u = s' × u (both parts)
2) Profit rate candidate: r' ≈ SP / (K_unified × u)
3) Investment-capital ratio: gK ≈ I / K_unified (heuristic; definitional caveats)
4) Internal consistency of c' and s' via V_from_SP and C_from_SP
   - s' ≈ SP / V_from_SP; c' ≈ C_from_SP / V_from_SP

Outputs:
- src/analysis/replication/output/TEXTUAL_CHECKS_SUMMARY.json
- src/analysis/replication/output/TEXTUAL_CHECKS_SUMMARY.md
"""

from pathlib import Path
import json
import pandas as pd
import numpy as np

OUT_DIR = Path("src/analysis/replication/output")
RAW_PATH = OUT_DIR / "table_5_4_authentic_raw_merged.csv"
CALC_PATH = OUT_DIR / "table_5_4_authentic_calculated.csv"
MD_OUT = OUT_DIR / "TEXTUAL_CHECKS_SUMMARY.md"
JSON_OUT = OUT_DIR / "TEXTUAL_CHECKS_SUMMARY.json"
ALIGN_MD = OUT_DIR / "BOOK_TEXT_ALIGNMENT.md"


def _mae_max(a: pd.Series, b: pd.Series) -> dict:
    diff = a - b
    common = diff.dropna()
    if len(common) == 0:
        return {"observations": 0}
    return {
        "observations": int(len(common)),
        "mae": float(common.abs().mean()),
        "max_abs_err": float(common.abs().max())
    }


def main() -> None:
    raw = pd.read_csv(RAW_PATH, index_col=0).T
    raw.index.name = "year"
    raw.index = raw.index.astype(int)

    calc = pd.read_csv(CALC_PATH)
    if 'year' in calc.columns:
        calc = calc.set_index('year')

    # Prepare containers
    summary = {"checks": {}, "notes": []}

    # 1) s'u identity across parts vs s'×u
    if all(col in calc.columns for col in ["s_u_calc"]):
        # Part 1 label: s'u; Part 2 label: s'«u
        results = {}
        if "s'u" in raw.columns:
            m = _mae_max(raw["s'u"], calc["s_u_calc"])  # type: ignore
            results["s'u_vs_s'x_u"] = m
        if "s'«u" in raw.columns:
            m = _mae_max(raw["s'«u"], calc["s_u_calc"])  # type: ignore
            results["s'«u_vs_s'x_u"] = m
        if results:
            summary["checks"]["s_u_identity"] = results

    # 2) Profit rate candidate: r' vs SP/(K_unified × u)
    if all(col in calc.columns for col in ["r_sp_over_Ku"]) and "r'" in raw.columns:
        m = _mae_max(raw["r'"], calc["r_sp_over_Ku"])  # type: ignore
        summary["checks"]["r_prime_vs_SP_over_Ku"] = m

    # 3) Investment-capital ratio: gK ≈ I / K_unified (or I! if present)
    # Heuristic: text references In/K*, while we have I or I!; definitions may differ.
    if "gK" in raw.columns and "K_unified" in calc.columns:
        inv_col = None
        if "I" in raw.columns:
            inv_col = "I"
        elif "I!" in raw.columns:
            inv_col = "I!"
        if inv_col is not None:
            with np.errstate(divide='ignore', invalid='ignore'):
                ratio = raw[inv_col] / calc["K_unified"]
            # Compare only where both are present
            common_idx = ratio.dropna().index.intersection(raw["gK"].dropna().index)  # type: ignore
            if len(common_idx) > 0:
                diff = raw.loc[common_idx, "gK"] - ratio.loc[common_idx]
                summary["checks"]["gK_vs_I_over_K"] = {
                    "observations": int(len(common_idx)),
                    "mae": float(diff.abs().mean()),
                    "max_abs_err": float(diff.abs().max()),
                    "investment_column": inv_col
                }
            summary["notes"].append(
                "gK vs I/K_unified is heuristic; the text refers to In/K* (net investment, specific capital measure)."
            )

    # 4) Internal consistency of s' and c' via V_from_SP and C_from_SP
    if all(col in calc.columns for col in ["V_from_SP"]) and "s'" in raw.columns:
        with np.errstate(divide='ignore', invalid='ignore'):
            s_from_sp = calc["SP"] / calc["V_from_SP"] if "SP" in calc.columns else np.nan
        if isinstance(s_from_sp, pd.Series):
            m = _mae_max(raw["s'"], s_from_sp)
            summary["checks"]["s_prime_vs_SP_over_V_from_SP"] = m

    if all(col in calc.columns for col in ["V_from_SP", "C_from_SP"]) and "c'" in raw.columns:
        with np.errstate(divide='ignore', invalid='ignore'):
            c_from_sp = calc["C_from_SP"] / calc["V_from_SP"]
        m = _mae_max(raw["c'"], c_from_sp)
        summary["checks"]["c_prime_vs_C_over_V_from_SP"] = m

    # 5) s' vs (1 - c') relationship noted in book text (warning: may depend on conventions)
    if all(col in raw.columns for col in ["s'", "c'"]):
        one_minus_c = 1.0 - raw["c'"]
        m = _mae_max(raw["s'"], one_minus_c)
        summary["checks"]["s_prime_vs_1_minus_c_prime"] = m

    # Write outputs
    JSON_OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Markdown summary
    lines = ["# TEXTUAL CONSISTENCY CHECKS", ""]
    for k, v in summary["checks"].items():
        if isinstance(v, dict) and "observations" in v:
            lines.append(f"- {k}: MAE={v.get('mae', 'n/a')}, max|err|={v.get('max_abs_err', 'n/a')}, n={v.get('observations', 0)}")
        else:
            lines.append(f"- {k}:")
            for subk, subv in v.items():
                lines.append(f"  - {subk}: MAE={subv.get('mae', 'n/a')}, max|err|={subv.get('max_abs_err', 'n/a')}, n={subv.get('observations', 0)}")
    if summary["notes"]:
        lines.append("")
        lines.append("## Notes")
        for n in summary["notes"]:
            lines.append(f"- {n}")
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Book text alignment report (simple thresholds)
    # Thresholds are indicative; identities should be near-equalities modulo rounding.
    THRESHOLD_MAE = 0.01
    THRESHOLD_MAX = 0.03

    def _flag(metric: dict) -> str:
        if not metric or metric.get("observations", 0) == 0:
            return "N/A"
        mae_ok = metric.get("mae", float("inf")) <= THRESHOLD_MAE
        max_ok = metric.get("max_abs_err", float("inf")) <= THRESHOLD_MAX
        return "PASS" if (mae_ok and max_ok) else "FLAG"

    lines2 = ["# BOOK TEXT ALIGNMENT", "", "Thresholds:", f"- MAE <= {THRESHOLD_MAE}", f"- max|err| <= {THRESHOLD_MAX}", ""]

    def _emit(name: str, metric_or_dict):
        if isinstance(metric_or_dict, dict) and "observations" in metric_or_dict:
            lines2.append(f"- {name}: {_flag(metric_or_dict)}  (MAE={metric_or_dict.get('mae','n/a')}, max|err|={metric_or_dict.get('max_abs_err','n/a')}, n={metric_or_dict.get('observations',0)})")
        else:
            lines2.append(f"- {name}:")
            for subk, subv in metric_or_dict.items():
                lines2.append(f"  - {subk}: {_flag(subv)}  (MAE={subv.get('mae','n/a')}, max|err|={subv.get('max_abs_err','n/a')}, n={subv.get('observations',0)})")

    # Emit key alignments
    for key in [
        "s_u_identity",
        "r_prime_vs_SP_over_Ku",
        "gK_vs_I_over_K",
        "s_prime_vs_SP_over_V_from_SP",
        "c_prime_vs_C_over_V_from_SP",
        "s_prime_vs_1_minus_c_prime",
    ]:
        if key in summary["checks"]:
            _emit(key, summary["checks"][key])

    if summary["notes"]:
        lines2.append("")
        lines2.append("## Notes")
        for n in summary["notes"]:
            lines2.append(f"- {n}")

    ALIGN_MD.write_text("\n".join(lines2) + "\n", encoding="utf-8")

    print(f"Wrote textual checks JSON: {JSON_OUT}")
    print(f"Wrote textual checks MD: {MD_OUT}")
    print(f"Wrote text alignment MD: {ALIGN_MD}")


if __name__ == "__main__":
    main()
