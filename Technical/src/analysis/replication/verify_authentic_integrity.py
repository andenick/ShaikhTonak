#!/usr/bin/env python3
"""
Verify Authentic Integrity
--------------------------

Compares `table_5_4_authentic.csv` (final export) with the original
`table_5_4_authentic_raw_merged.csv` (book values) to ensure original
book-provided entries were not altered. Derived columns are ignored.

Outputs:
- src/analysis/replication/output/authenticity_check.json
- src/analysis/replication/output/AUTHENTICITY_CHECK.md
"""

from pathlib import Path
import pandas as pd
import numpy as np
import json

OUT_DIR = Path("src/analysis/replication/output")
RAW_PATH = OUT_DIR / "table_5_4_authentic_raw_merged.csv"
FINAL_PATH = OUT_DIR / "table_5_4_authentic.csv"
JSON_OUT = OUT_DIR / "authenticity_check.json"
MD_OUT = OUT_DIR / "AUTHENTICITY_CHECK.md"

# Columns created by our derivations that should be ignored for authenticity checks
DERIVED_COLS = {
    "r_prime_calc",
    "s_u_calc",
    "V_from_SP",
    "C_from_SP",
}


def _normalize_numeric(s: pd.Series) -> pd.Series:
    """Attempt numeric conversion while preserving NaNs."""
    return pd.to_numeric(s, errors="coerce")


def main() -> None:
    # Load raw (variables-as-rows) then transpose to years × variables
    raw = pd.read_csv(RAW_PATH, index_col=0).T
    raw.index.name = "year"
    raw.index = raw.index.astype(int)

    final_df = pd.read_csv(FINAL_PATH)
    if "year" in final_df.columns:
        final_df = final_df.set_index("year")

    # Determine columns to check: intersection excluding derived
    book_cols = [c for c in raw.columns if c in final_df.columns and c not in DERIVED_COLS]

    report = {"status": "pass", "mismatch_columns": [], "mismatch_count": 0, "checked_columns": book_cols}
    details = {}

    total_mismatches = 0
    for col in book_cols:
        a = raw[col]
        b = final_df[col]

        # Align indices
        idx = a.index.intersection(b.index)
        a = a.loc[idx]
        b = b.loc[idx]

        # Try numeric compare first
        a_num = _normalize_numeric(a)
        b_num = _normalize_numeric(b)
        both_num = a_num.notna() | b_num.notna()

        mismatches = []

        if both_num.any():
            # Consider NaN == NaN
            num_equal = (a_num.fillna(np.nan) - b_num.fillna(np.nan)).abs() <= 1e-12
            # Treat both NaN as equal
            both_nan = a_num.isna() & b_num.isna()
            equal_mask = num_equal | both_nan
            for y, ok in equal_mask.items():
                if not ok:
                    mismatches.append({
                        "year": int(y),
                        "raw": None if pd.isna(a_num.loc[y]) else float(a_num.loc[y]),
                        "final": None if pd.isna(b_num.loc[y]) else float(b_num.loc[y])
                    })
        else:
            # Fallback to string comparison (including empty values)
            a_str = a.astype(str).replace({"nan": None})
            b_str = b.astype(str).replace({"nan": None})
            for y in idx:
                if a_str.loc[y] != b_str.loc[y]:
                    mismatches.append({"year": int(y), "raw": a_str.loc[y], "final": b_str.loc[y]})

        if mismatches:
            details[col] = {"mismatches": mismatches, "count": len(mismatches)}
            report["mismatch_columns"].append(col)
            total_mismatches += len(mismatches)

    report["mismatch_count"] = total_mismatches
    if total_mismatches > 0:
        report["status"] = "fail"

    # Write outputs
    JSON_OUT.write_text(json.dumps({"summary": report, "details": details}, indent=2), encoding="utf-8")

    lines = []
    lines.append("# AUTHENTICITY CHECK")
    lines.append("")
    lines.append(f"Status: {report['status'].upper()}")
    lines.append(f"Columns checked: {len(book_cols)}")
    lines.append(f"Total mismatches: {total_mismatches}")
    if report["mismatch_columns"]:
        lines.append("")
        lines.append("## Columns with mismatches")
        for c in report["mismatch_columns"]:
            lines.append(f"- {c}: {details[c]['count']} mismatches (showing up to first 5)")
            for m in details[c]["mismatches"][:5]:
                lines.append(f"  - {m['year']}: raw={m['raw']}, final={m['final']}")

    MD_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote authenticity check report to: {JSON_OUT}")
    print(f"Wrote authenticity check summary to: {MD_OUT}")


if __name__ == "__main__":
    main()
