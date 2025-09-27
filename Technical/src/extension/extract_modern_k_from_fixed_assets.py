#!/usr/bin/env python3
"""
Extract modern K (S&T-consistent) from BEA Fixed Assets FlatFiles
================================================================

We construct modern_K_st_consistent as the BEA Fixed Assets "Private fixed assets"
current-cost net stock series (level, current dollars). This aligns with
Shaikh & Tonak's K concept at the aggregate private economy level.

Data source in repo (archived raw):
- archive/deprecated_databases/Database_Leontief_original/data/raw/bea-fixedAssets/FlatFiles/
  - FixedAssets.txt (SeriesCode, Period, Value)
  - SeriesRegister.txt (Series metadata)

Target series:
- SeriesCode: k1ptotl1es00
  Label: "Private fixed assets" | Metric: "Current Dollars" | Level | FAAt201 lines

Output:
- data/modern/processed/bea_fixed_assets/private_net_stock_current_cost.csv
  columns: year, modern_K_st_consistent

No interpolation or transformation beyond type cleaning.
"""

from __future__ import annotations

import csv
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
RAW_FIXED_ASSETS = BASE / "archive" / "deprecated_databases" / "Database_Leontief_original" / "data" / "raw" / "bea-fixedAssets" / "FlatFiles"
FIXED_ASSETS_FILE = RAW_FIXED_ASSETS / "FixedAssets.txt"
OUTPUT_DIR = BASE / "data" / "modern" / "processed" / "bea_fixed_assets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUTPUT_DIR / "private_net_stock_current_cost.csv"

TARGET_SERIES = "k1ptotl1es00"  # Private fixed assets, current-cost, net stock, current dollars, level


def load_series(series_code: str) -> pd.DataFrame:
    """Stream-read FixedAssets.txt and collect rows for the given series code."""
    if not FIXED_ASSETS_FILE.exists():
        raise FileNotFoundError(f"Fixed assets file not found: {FIXED_ASSETS_FILE}")

    rows = []
    # FixedAssets.txt is large; we iterate line-by-line
    with FIXED_ASSETS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # [%SeriesCode, Period, Value]
        # Normalize the first column header (sometimes prefixed with %)
        # We just parse positionally
        for scode, period, value in reader:
            if scode == series_code:
                # Remove commas from Value then to float
                v = None
                if value is not None and value != "":
                    v = float(str(value).replace(",", ""))
                rows.append((int(period), v))

    df = pd.DataFrame(rows, columns=["year", "value"]).sort_values("year")
    return df


def main() -> None:
    df = load_series(TARGET_SERIES)
    # Keep modern period coverage but export full series for transparency
  out = df.rename(columns={"value": "modern_K_st_consistent"})
  # Add normalized placeholder identical to raw; enables explicit unit/scope alignment later
  out["modern_K_st_consistent_norm"] = out["modern_K_st_consistent"]
  out.to_csv(OUT_FILE, index=False)
    print(f"Wrote modern K series to: {OUT_FILE}")
    print(f"Years: {int(out['year'].min())}-{int(out['year'].max())}; count={len(out)}")


if __name__ == "__main__":
    main()
