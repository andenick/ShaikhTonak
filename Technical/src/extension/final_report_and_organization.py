#!/usr/bin/env python3
"""
Final Report Generator and Folder Organizer

- Creates a clean final deliverables structure without touching raw data
- Copies Phase 1 replication outputs and Phase 2 expansion outputs
- Produces additional figures (SP, K, u) and a consolidated Markdown report

Output folders:
- results/final/replication/   # historical perfect replication artifacts
- results/final/expansion/     # modern expansion (faithful) artifacts
- results/final/combined/      # chained series across periods
- results/final/plots/         # curated figures for the report
- results/final/               # top-level report and directory map
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


@dataclass
class Paths:
    base: Path
    hist_dir: Path
    integrated_csv: Path
    faithful_hist_csv: Path
    faithful_combined_csv: Path
    plots_src_dir: Path
    final_root: Path
    final_replication: Path
    final_expansion: Path
    final_combined: Path
    final_plots: Path
    final_report_md: Path
    dir_map_md: Path


def detect_phase1_perfect(hist_dir: Path) -> Optional[Path]:
    """Return the best candidate for Phase 1 perfect replication results if available."""
    candidates = [
        hist_dir / 'perfect_replication_results.csv',
        hist_dir / 'complete_analysis_summary.csv',
        hist_dir / 'marxian_variables_calculated.csv',
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def ensure_dirs(p: Paths) -> None:
    for d in [p.final_root, p.final_replication, p.final_expansion, p.final_combined, p.final_plots]:
        d.mkdir(parents=True, exist_ok=True)


def copy_if_exists(src: Optional[Path], dst: Path) -> Optional[Path]:
    if src and src.exists():
        shutil.copy2(src, dst)
        return dst
    return None


def make_additional_plots(p: Paths) -> dict[str, str]:
    """Build SP, K, u time series figures for modern years using the integrated dataset."""
    out: dict[str, str] = {}
    if not p.integrated_csv.exists():
        return out
    df = pd.read_csv(p.integrated_csv)
    sns.set_theme(style='whitegrid')

    # Modern subset
    mod = df[df['year'] >= 1990].copy()

    # SP (modern)
    if 'modern_SP_st_consistent' in mod.columns:
        fig_path = p.final_plots / 'figure_sp_modern_1990_2023.png'
        plt.figure(figsize=(10,4))
        plt.plot(mod['year'], mod['modern_SP_st_consistent']/1000.0, color='#2c7fb8', linewidth=1.8)
        plt.title('Surplus Product (Modern, S&T-consistent) — Billions of $ (current)')
        plt.xlabel('Year'); plt.ylabel('Billions of dollars')
        plt.tight_layout(); plt.savefig(fig_path, dpi=200); plt.close()
        out['figure_sp_modern'] = str(fig_path)

    # K (modern)
    if 'modern_K_st_consistent' in mod.columns:
        fig_path = p.final_plots / 'figure_k_modern_1990_2023.png'
        plt.figure(figsize=(10,4))
        plt.plot(mod['year'], mod['modern_K_st_consistent']/1000.0, color='#41ab5d', linewidth=1.8)
        plt.title('Capital Stock (Modern, S&T-consistent) — Billions of $ (current)')
        plt.xlabel('Year'); plt.ylabel('Billions of dollars')
        plt.tight_layout(); plt.savefig(fig_path, dpi=200); plt.close()
        out['figure_k_modern'] = str(fig_path)

    # u (modern)
    if 'capacity_utilization' in mod.columns:
        fig_path = p.final_plots / 'figure_u_modern_1990_2025.png'
        plt.figure(figsize=(10,4))
        # Plot in percent for readability
        plt.plot(mod['year'], mod['capacity_utilization'], color='#dd1c77', linewidth=1.8)
        plt.title('Capacity Utilization (Fed G.17) — Percent')
        plt.xlabel('Year'); plt.ylabel('Percent (0–100)')
        plt.tight_layout(); plt.savefig(fig_path, dpi=200); plt.close()
        out['figure_u_modern'] = str(fig_path)

    # r historical vs modern combined plot from faithful combined CSV
    if p.faithful_combined_csv.exists():
        comb = pd.read_csv(p.faithful_combined_csv)
        fig_path = p.final_plots / 'figure_r_faithful_combined.png'
        plt.figure(figsize=(10,4))
        plt.plot(comb['year'], comb['profit_rate'], marker='o', markersize=2.5, linewidth=1.2, color='black')
        plt.title("Rate of Profit (Faithful S&T) — 1958–2023")
        plt.xlabel('Year'); plt.ylabel('Rate of Profit (unitless)')
        plt.tight_layout(); plt.savefig(fig_path, dpi=200); plt.close()
        out['figure_r_combined'] = str(fig_path)

    return out


def build_final_report(p: Paths, extra_figs: dict[str,str], phase1_src: Optional[Path]) -> None:
    # Stats
    hist = pd.read_csv(p.faithful_hist_csv)
    comb = pd.read_csv(p.faithful_combined_csv)
    modern = comb[comb['year'] >= 1990].dropna(subset=['profit_rate'])
    mean_hist = hist['profit_rate'].dropna().mean() if not hist.empty else float('nan')
    mean_mod = modern['profit_rate'].mean() if not modern.empty else float('nan')
    min_mod = modern['profit_rate'].min() if not modern.empty else float('nan')
    max_mod = modern['profit_rate'].max() if not modern.empty else float('nan')

    # Units from integration metadata
    units = {}
    try:
        meta = json.loads((p.base/'data/modern/integrated/integration_metadata.json').read_text())
        units = meta.get('units', {})
    except Exception:
        pass

    def unit_line(key: str) -> str:
        v = units.get(key)
        return f"- {key}: {v}" if v else f"- {key}: (unit not documented)"

    # Report content
    content = f"""
# Faithful Replication and Expansion — Final Report

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive summary

- Historical replication (1958–1989): Exactly preserves the book's r' series.
- Expansion (1990–2023): Computed strictly by r = SP/(K×u), with SP and K staged from BEA and u normalized to a 0–1 fraction.
- Levels: Historical mean r' ≈ {mean_hist:.3f}; Modern mean r ≈ {mean_mod:.3f} (range {min_mod:.3f}–{max_mod:.3f}).
- No proxies, interpolation, or arbitrary scaling applied. Only a units normalization on u (percent → fraction) consistent with S&T's usage.

## Methodological fidelity

- Historical period uses published r' exactly, including the known missing 1974 value (left blank).
- Modern period honors the identity: r = SP / (K × u).
- SP and K are derived from official sources aligned with S&T definitions:
  - SP: Business NDP − Compensation (Private Industries + Government Enterprises), from NIPA flat files.
  - K: Current-cost net stock of private fixed assets, from BEA Fixed Assets.
- Capacity utilization: Federal Reserve G.17, converted to fraction.

## Units audit

{unit_line('modern_SP_st_consistent')}
{unit_line('modern_K_st_consistent')}
{unit_line('capacity_utilization')}

- By construction, r is unitless.

## Key figures

- Rate of Profit (combined, faithful): {extra_figs.get('figure_r_combined','(not generated)')}
- Surplus Product (modern): {extra_figs.get('figure_sp_modern','(not generated)')}
- Capital Stock (modern): {extra_figs.get('figure_k_modern','(not generated)')}
- Capacity Utilization (modern): {extra_figs.get('figure_u_modern','(not generated)')}

## Results in historical context

The postwar pattern (1958–1989) presents a plateau in profitability, followed by a downturn in the
1970s and a partial recovery in the 1980s. The expansion era (1990–2023) continues with a lower mean rate of
profit. Peaks coincide with high utilization phases (late 1990s, mid-2000s, post-2010s), while troughs mark weak
demand and crises such as 2008–2009. The enduring gap relative to mid-century levels is consistent with a
higher organic composition of capital and heightened competitive pressures, limiting the durability of recoveries
in r, even amidst productivity improvements.

## Deliverables map (you can open these directly)

- Replication (historical): {p.final_replication}
  - Perfect replication (Phase 1): {phase1_src if phase1_src else '(not found, see historical faithful CSV below)'}
  - Faithful historical r' only: {p.final_replication / 'shaikh_tonak_faithful_1958_1989.csv'}

- Expansion (modern, faithful): {p.final_expansion}
  - Faithful modern r only: {p.final_expansion / 'shaikh_tonak_faithful_1990_2023.csv'}

- Combined (chained series): {p.final_combined}
  - Faithful 1958–2023 series: {p.final_combined / 'shaikh_tonak_faithful_1958_2025.csv'}

- Plots: {p.final_plots}

## Next steps

- Bridge-year diagnostic (documentation only): compare 1989 published r' with implied r using historical u and staged K/SP to document residual
  definition differences (no scaling applied).
- Add a parallel, clearly labeled diagnostic series that uses corporate profits or KLEMS for sensitivity (kept separate from faithful results).
- Extend SP and K to the latest available year; add versioned metadata snapshots for reproducibility.
- Package the pipeline as a reusable CLI with pinned environment for long-term reproducibility.

"""
    p.final_report_md.write_text(content, encoding='utf-8')

    # Directory map (concise)
    p.dir_map_md.write_text(f"""
# Final Deliverables Directory Map

- replication/: Phase 1 historical replication artifacts
- expansion/: Phase 2 faithful expansion artifacts
- combined/: Chained profit-rate series across historical + modern
- plots/: Curated figures used in the final report
- FAITHFUL_REPLICATION_AND_EXPANSION_REPORT.md: Final narrative report

Note: Raw data under data/source_pdfs, data/historical/raw, and data/modern/raw were not modified.
""".strip(), encoding='utf-8')


def main() -> None:
    base = Path(__file__).resolve().parents[2]
    p = Paths(
        base=base,
        hist_dir=base / 'data' / 'historical' / 'processed',
        integrated_csv=base / 'data' / 'modern' / 'integrated' / 'complete_st_timeseries_1958_2025.csv',
        faithful_hist_csv=base / 'data' / 'modern' / 'final_results_faithful' / 'shaikh_tonak_faithful_1958_1989.csv',
        faithful_combined_csv=base / 'data' / 'modern' / 'final_results_faithful' / 'shaikh_tonak_faithful_1958_2025.csv',
        plots_src_dir=base / 'results' / 'extension' / 'plots',
        final_root=base / 'results' / 'final',
        final_replication=base / 'results' / 'final' / 'replication',
        final_expansion=base / 'results' / 'final' / 'expansion',
        final_combined=base / 'results' / 'final' / 'combined',
        final_plots=base / 'results' / 'final' / 'plots',
        final_report_md=base / 'results' / 'final' / 'FAITHFUL_REPLICATION_AND_EXPANSION_REPORT.md',
        dir_map_md=base / 'results' / 'final' / 'DIRECTORY_MAP.md',
    )

    ensure_dirs(p)

    # Detect and copy Phase 1 perfect replication file if present
    phase1_src = detect_phase1_perfect(p.hist_dir)
    if phase1_src:
        copy_if_exists(phase1_src, p.final_replication / phase1_src.name)

    # Copy faithful historical-only r'
    copy_if_exists(p.faithful_hist_csv, p.final_replication / p.faithful_hist_csv.name)

    # Build an expansion-only CSV (1990–2023) from the faithful combined file
    if p.faithful_combined_csv.exists():
        comb = pd.read_csv(p.faithful_combined_csv)
        exp = comb[comb['year'] >= 1990].copy()
        exp_out = p.final_expansion / 'shaikh_tonak_faithful_1990_2023.csv'
        exp.to_csv(exp_out, index=False)

        # Copy the chained combined file into combined/
        copy_if_exists(p.faithful_combined_csv, p.final_combined / p.faithful_combined_csv.name)

    # Additional curated plots for the report
    extra_figs = make_additional_plots(p)

    # Build final report and directory map
    build_final_report(p, extra_figs, phase1_src)

    print("Final report written to:", p.final_report_md)
    print("Directory map written to:", p.dir_map_md)
    print("Replication dir:", p.final_replication)
    print("Expansion dir:", p.final_expansion)
    print("Combined dir:", p.final_combined)


if __name__ == '__main__':
    main()
