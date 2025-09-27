#!/usr/bin/env python3
"""
Stub: Build modern SP (S&T-consistent) from BEA NIPA
====================================================

This is a placeholder to document where the modern SP series, consistent with
Shaikh & Tonak's definition of surplus product, should be constructed and saved.

Expected output file (for integration to auto-pick up):
- data/modern/bea_nipa/modern_sp_st_consistent_1990_2025.csv
  columns: year, modern_SP_st_consistent

Notes:
- Do NOT use corporate profits as a proxy. Assemble SP from NIPA components per
  S&T: align to private domestic economy, use income-side aggregates that match
  their concept of surplus product. Document exact table/line mappings.
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / "data" / "modern" / "bea_nipa" / "modern_sp_st_consistent_1990_2025.csv"


def main() -> None:
    # This is just a documentation stub; write a tiny placeholder with header only
    if not OUT.exists():
        df = pd.DataFrame({"year": [], "modern_SP_st_consistent": []})
        df.to_csv(OUT, index=False)
        print(f"Created placeholder for modern SP here: {OUT}")
    else:
        print(f"SP placeholder already exists: {OUT}")


if __name__ == "__main__":
    main()
