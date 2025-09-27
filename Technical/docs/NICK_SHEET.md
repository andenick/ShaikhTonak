# Nick Sheet (Updated) — One-Page Cheat Sheet

Date: 2025-09-22

## Mission and Non-Negotiables
- Faithful replication first, then carefully documented extension.
- Zero undocumented divergences; preserve historical values exactly.
- Identity: r = SP / (K × u). r is unitless; u must be a fraction (0–1).
- Do not touch raw data directories.

## Key Deliverables (open these)
- Final report (Markdown): results/final/FAITHFUL_REPLICATION_AND_EXPANSION_REPORT.md
- Directory map: results/final/DIRECTORY_MAP.md
- Replication artifacts: results/final/replication/
- Expansion artifacts: results/final/expansion/
- Combined series: results/final/combined/
- Curated plots: results/final/plots/

## Critical Data Inputs (staged)
- SP (modern): data/modern/bea_nipa/modern_sp_st_consistent_1990_2025.csv (Millions $)
- K (modern): data/modern/processed/bea_fixed_assets/private_net_stock_current_cost.csv (Millions $)
- u (modern): data/modern/fed_capacity/capacity_utilization_*.csv (Percent in file; converted to fraction in pipeline)

## What to Run (in this order)
1) Integration (rebuilds integrated 1958–2025 dataset)
   - src/extension/phase2_data_integration.py
2) Faithful S&T-only pipeline (computes r via identity, makes plots/report)
   - src/extension/phase2_faithful_st_only.py
3) Final packaging (organizes deliverables + builds final report)
   - src/extension/final_report_and_organization.py

## Units Policy (must-haves)
- SP and K must be same currency units (Millions of current dollars).
- u must be fraction (0–1). If source shows 70, convert to 0.70.
- r is unitless. Never scale r to “look right.”

## QA Checklist (fast)
- Historical r' 1958–1989 matches book exactly (1974 blank).
- modern_SP_st_consistent and modern_K_st_consistent present for 1990+ years.
- u converted to fraction (notes in outputs indicate detection and conversion).
- Combined CSV exists: data/modern/final_results_faithful/shaikh_tonak_faithful_1958_2025.csv.
- Final report present in results/final/.

## Do / Don’t
- DO: Document every divergence and unit normalization.
- DO: Keep KLEMS diagnostic-only unless explicitly authorized.
- DON’T: Interpolate, proxy, or scale to fit; leave gaps or differences documented.

## If Something Looks Off
- Check units first (esp. u and currency units).
- Re-run integration → faithful pipeline → packaging.
- Read results/final/FAITHFUL_REPLICATION_AND_EXPANSION_REPORT.md for current status and notes.
