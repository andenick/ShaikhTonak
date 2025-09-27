#!/usr/bin/env python3
"""
Consolidate Authentic Replication Outputs
----------------------------------------

Merges the authentic raw merged dataset with the methodology-calculated identities
into a single, wide CSV to aid inspection and manual validation. No interpolation
or gap-filling is performed.
"""

from pathlib import Path
import pandas as pd

RAW_PATH = Path("src/analysis/replication/output/table_5_4_authentic_raw_merged.csv")
CALC_PATH = Path("src/analysis/replication/output/table_5_4_authentic_calculated.csv")
OUT_PATH = Path("src/analysis/replication/output/table_5_4_authentic_consolidated.csv")


def main() -> None:
    raw = pd.read_csv(RAW_PATH, index_col=0).T
    raw.index.name = "year"
    raw.index = raw.index.astype(int)

    calc = pd.read_csv(CALC_PATH)
    if 'year' in calc.columns:
        calc = calc.set_index('year')

    # Ensure numeric types where possible
    for df in (raw, calc):
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    consolidated = raw.join(calc, how='outer', lsuffix='_raw', rsuffix='_calc')
    consolidated.to_csv(OUT_PATH)

    print(f"Wrote consolidated authentic dataset to: {OUT_PATH}")


if __name__ == '__main__':
    main()
