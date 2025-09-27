#!/usr/bin/env python3
"""
Export Final Authentic Table 5.4
--------------------------------

Produces `table_5_4_authentic.csv` that includes:
- Original authentic values straight from the book tables (no changes)
- Derived series computed by strict algebraic identities confirmed from the data:
  - r' = SP / (K_unified * u)
  - s_u = s' * u
  - V_from_SP = SP / s'
  - C_from_SP = c' * V_from_SP
  - (Optional diagnostics retained in calculated file; not all are exported here.)

Also writes `AUTHENTIC_REPLICATION_SUMMARY.md` with a compact summary of coverage
and validation metrics. No interpolation or smoothing is performed.
"""

from pathlib import Path
import pandas as pd
import json

RAW_PATH = Path("src/analysis/replication/output/table_5_4_authentic_raw_merged.csv")
CALC_PATH = Path("src/analysis/replication/output/table_5_4_authentic_calculated.csv")
VAL_PATH = Path("src/analysis/replication/output/authentic_validation_summary.json")
OUT_CSV = Path("src/analysis/replication/output/table_5_4_authentic.csv")
OUT_SUMMARY = Path("src/analysis/replication/output/AUTHENTIC_REPLICATION_SUMMARY.md")


def main() -> None:
    # Load raw (variables as rows) and transpose to years × variables
    raw = pd.read_csv(RAW_PATH, index_col=0).T
    raw.index.name = "year"
    raw.index = raw.index.astype(int)

    # Load calculated identities (already years × variables)
    calc = pd.read_csv(CALC_PATH)
    if 'year' in calc.columns:
        calc = calc.set_index('year')

    # Select trusted derived series for final export
    trusted_cols = [
        "r_sp_over_Ku",  # final r' (exported as r_prime_calc to preserve book r')
        "s_u_calc",      # s'u
        "V_from_SP",
        "C_from_SP",
    ]
    present_trusted = [c for c in trusted_cols if c in calc.columns]

    final_df = raw.copy()
    # Add a derived profit rate without overwriting the authentic r'
    if "r_sp_over_Ku" in calc.columns:
        final_df["r_prime_calc"] = calc["r_sp_over_Ku"]
    # Add other trusted derived series with clear names
    for c in present_trusted:
        if c == "r_sp_over_Ku":
            continue
        final_df[c] = calc[c]

    final_df.to_csv(OUT_CSV)

    # Load validation summary if available
    try:
        with open(VAL_PATH, 'r', encoding='utf-8') as f:
            val = json.load(f)
    except Exception:
        val = {}

    # Create compact human-readable summary
    lines = []
    lines.append("# AUTHENTIC REPLICATION SUMMARY")
    lines.append("")
    lines.append("This table preserves book values exactly and adds only identity-based derived values.")
    lines.append("No interpolation or smoothing was performed.")
    lines.append("")

    # Coverage
    def pct(col):
        s = final_df[col]
        return 100.0 * s.notna().sum() / len(s)

    lines.append("## Coverage")
    lines.append("")
    cov_items = ["r_prime_calc", "s_u_calc", "V_from_SP", "C_from_SP"]
    for c in cov_items:
        if c in final_df.columns:
            lines.append(f"- {c}: {pct(c):.1f}% of years computable from book inputs")

    # Validation excerpts
    lines.append("")
    lines.append("## Validation Excerpts")
    lines.append("")
    if val.get("validation"):
        v = val["validation"]
        if "r_vs_sp_over_Ku" in v:
            lines.append("- Profit rate identity (r' vs SP/(K×u)): ")
            lines.append(f"  MAE = {v['r_vs_sp_over_Ku']['mae']:.6f}, max |err| = {v['r_vs_sp_over_Ku']['max_abs_err']:.6f}, n = {v['r_vs_sp_over_Ku']['observations']}")
        if "s_u_identity" in v:
            su = v["s_u_identity"]
            if "s'u" in su:
                lines.append("- s'u vs s'×u (Part 1):")
                su1 = su["s'u"]
                lines.append(f"  MAE = {su1['mae']:.6f}, max |err| = {su1['max_abs_err']:.6f}, n = {su1['observations']}")
            if "s'\u00abu" in su:
                k = su["s'\u00abu"]
                lines.append("- s'«u vs s'×u (Part 2):")
                lines.append(f"  MAE = {k['mae']:.6f}, max |err| = {k['max_abs_err']:.6f}, n = {k['observations']}")

    OUT_SUMMARY.write_text("\n".join(lines), encoding='utf-8')

    print(f"Wrote final authentic table to: {OUT_CSV}")
    print(f"Wrote summary to: {OUT_SUMMARY}")


if __name__ == '__main__':
    main()
