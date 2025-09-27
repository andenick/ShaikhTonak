#!/usr/bin/env python3
"""
Build modern SP (S&T-consistent) from BEA NIPA flat files
=========================================================

Constructs modern_SP_st_consistent using only official BEA NIPA series,
following a faithful mapping aligned to Shaikh & Tonak's surplus product (SP):

Core identity target: r = SP / (K × u)

Mapping (documented):
- Use Net Domestic Product of Business (current dollars): A363RC
- Subtract Compensation of Employees paid by Private Industries: A4003C
- Subtract Compensation of Employees paid by Government Enterprises: A4081C

Thus, SP_business ≈ NDP_business − (Comp_private + Comp_govt_enterprises)

Rationale:
- NDP (net of CFC) ensures consistency with book’s net capital concept.
- Removing all business compensation isolates surplus product accruing to
  capital (profits-like flows including TPI less subsidies and NOS), consistent
  with the numerator used in r' in Table 5.4.

Validation:
- Compares the constructed SP against historical SP (1958–1989) from
  data/historical/processed/table_5_4_authentic.csv and reports error summary.
  No scaling or interpolation is applied—differences are documented only.

Output:
- data/modern/bea_nipa/modern_sp_st_consistent_1990_2025.csv
  Columns: year, modern_SP_st_consistent

Notes:
- Uses archived BEA flat file: archive/.../bea-nipa/flatFiles/nipadataA.txt
- If some years are missing for any input, those years are omitted (no fill).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd


@dataclass(frozen=True)
class SeriesSpec:
    code: str
    label: str


def read_nipa_series(flat_file: Path, codes: Iterable[str]) -> pd.DataFrame:
    """Read selected series (annual) from BEA nipadataA flat file into wide DF.

    Returns DataFrame with columns: year (int), and one column per code (float).
    """
    wanted = set(codes)
    rows: Dict[str, Dict[int, float]] = {c: {} for c in wanted}
    with flat_file.open('r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for code, year_str, val_str in reader:
            if code not in wanted:
                continue
            try:
                y = int(year_str)
            except ValueError:
                continue
            # Strip commas and quotes, convert to float
            v = None
            s = val_str.strip().replace(',', '').replace('"', '')
            if s in ('', '.', 'NA'):
                continue
            try:
                v = float(s)
            except ValueError:
                continue
            rows[code][y] = v

    # Build DataFrame
    years = sorted(set().union(*[set(d.keys()) for d in rows.values()]))
    df = pd.DataFrame({'year': years})
    for c in wanted:
        df[c] = df['year'].map(rows[c]).astype(float)
    return df


def build_sp(df: pd.DataFrame, ndp_business: str, comp_private: str, comp_gov_enterprises: str) -> pd.DataFrame:
    """Compute SP_business = NDP_business − (Comp_private + Comp_govt_enterprises)."""
    need = [ndp_business, comp_private, comp_gov_enterprises]
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing required series: {missing}")
    out = df[['year']].copy()
    out['modern_SP_st_consistent'] = df[ndp_business] - (df[comp_private] + df[comp_gov_enterprises])
    # Keep rows where all inputs are present
    mask = df[need].notna().all(axis=1)
    out = out[mask]
    return out


def validate_against_historical(sp_df: pd.DataFrame, base_dir: Path) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Join with historical SP to assess fit over 1958–1989; return comparison and stats."""
    hist_file = base_dir / 'data' / 'historical' / 'processed' / 'table_5_4_authentic.csv'
    if not hist_file.exists():
        return pd.DataFrame(), {}
    hist = pd.read_csv(hist_file)
    if 'SP' not in hist.columns:
        return pd.DataFrame(), {}
    comp = hist[['year', 'SP']].merge(sp_df, on='year', how='inner')
    # Limit to historical period
    comp = comp[(comp['year'] >= 1958) & (comp['year'] <= 1989)].copy()
    if comp.empty:
        return comp, {}
    comp['abs_err'] = (comp['modern_SP_st_consistent'] - comp['SP']).abs()
    comp['rel_err'] = comp['abs_err'] / comp['SP'].replace(0, pd.NA)
    stats = {
        'n_overlap': int(comp.shape[0]),
        'mae': float(comp['abs_err'].mean()),
        'mape_pct': float((comp['rel_err'] * 100.0).mean(skipna=True)),
        'corr': float(comp[['SP', 'modern_SP_st_consistent']].corr().iloc[0, 1]) if comp.shape[0] > 1 else float('nan'),
    }
    return comp, stats


def main() -> None:
    base = Path(__file__).resolve().parents[2]
    # Inputs
    flat = base / 'archive' / 'deprecated_code' / 'deprecated_databases' / 'Database_Leontief_original' / 'data' / 'raw' / 'bea-nipa' / 'flatFiles' / 'nipadataA.txt'
    if not flat.exists():
        raise FileNotFoundError(f"BEA flat file not found: {flat}")

    # Target output
    out_dir = base / 'data' / 'modern' / 'bea_nipa'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / 'modern_sp_st_consistent_1990_2025.csv'

    # Series specs
    NDP_BUS = SeriesSpec('A363RC', 'Net domestic product: Business (current $)')
    COMP_PRIV = SeriesSpec('A4003C', 'Compensation of employees: Private industries (current $)')
    COMP_GOV_ENT = SeriesSpec('A4081C', 'Compensation of employees: Government enterprises (current $)')

    codes = [NDP_BUS.code, COMP_PRIV.code, COMP_GOV_ENT.code]
    raw = read_nipa_series(flat, codes)

    # Build SP
    sp = build_sp(raw, NDP_BUS.code, COMP_PRIV.code, COMP_GOV_ENT.code)

    # Validation vs historical (no scaling; diagnostics only)
    comp, stats = validate_against_historical(sp, base)
    if stats:
        val_dir = base / 'data' / 'modern' / 'bea_nipa' / 'validation'
        val_dir.mkdir(parents=True, exist_ok=True)
        comp.to_csv(val_dir / 'modern_sp_validation_vs_historical.csv', index=False)
        (val_dir / 'modern_sp_validation_stats.json').write_text(pd.Series(stats).to_json(indent=2), encoding='utf-8')

    # Add a normalized column (currently identical; reserved for future scope/unit adjustments)
    sp['modern_SP_st_consistent_norm'] = sp['modern_SP_st_consistent']

    # Restrict to modern years for output
    sp_out = sp[sp['year'] >= 1990].copy()
    # Clip to 2025 inclusive if present
    sp_out = sp_out[sp_out['year'] <= 2025]
    sp_out[['year', 'modern_SP_st_consistent', 'modern_SP_st_consistent_norm']].to_csv(out_csv, index=False)

    # Simple stdout summary
    first, last = (int(sp_out['year'].min()) if not sp_out.empty else None,
                   int(sp_out['year'].max()) if not sp_out.empty else None)
    print(f"Wrote modern SP to {out_csv} covering years {first}-{last} ({len(sp_out)} rows)")
    if stats:
        print("Validation vs historical SP (1958–1989):", stats)


if __name__ == '__main__':
    main()
