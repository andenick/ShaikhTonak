# Faithful Replication and Extension (Primary Purpose)

This project’s sole objective is a faithful representation of the historical methodology in Shaikh & Tonak (1994), reproducing the book tables exactly and extending the series forward only by following the same formulas and concepts. Any place where modern data require interpretation must be explicitly surfaced as an expert decision, not silently decided in code.

## What “faithful” means here

- Historical period (1958–1989):
  - Preserve all book-provided values exactly (no edits).
  - Reproduce derived values strictly from the book’s definitions (not proxies). Where a definition is pending, report the gap and do not claim exact replication.
  - Maintain an integrity check to ensure no original values were altered.
- Modern extension (1990→):
  - Follow the same formulas (e.g., r = SP/(K×u)) using modern equivalents of the same concepts and sources.
  - Do not introduce model-based scaling or ad hoc ratios; if a mapping from modern to S&T concepts is genuinely uncertain, expose it as an expert decision and halt at the boundary for review.

## Current status at a glance

- r′ replication: Strong alignment using r = SP/(K×u) (see `src/analysis/replication/output/PERFECT_REPLICATION_REPORT.md`).
- s′u identities: Pass tight checks for both parts.
- gK: Pending exact S&T definition of In and K*; do not claim perfect replication until implemented as per the book.
- Authenticity: Original book columns preserved exactly; integrity check PASS (0 mismatches).

## Faithful outputs and where to find them

- Authentic baseline (book tables merged): `src/analysis/replication/output/table_5_4_authentic_raw_merged.csv`
- Integrity-checked authentic final: `src/analysis/replication/output/table_5_4_authentic.csv`
- Perfect replication (in-scope variables only): `src/analysis/replication/output/table_5_4_perfect_replication.csv`
- Validation and reports: `src/analysis/replication/output/*.md|*.json`

## Modern extension – faithful track

- The faithful extension applies the S&T formula r = SP/(K×u) using modern equivalents of SP, K, and u.
- Expert insertion points must be resolved before producing official extension values:
  - SP line mappings (modern NIPA to S&T concept)
  - K mapping (BEA Fixed Assets to S&T capital concept; deflators/base-year)
  - Utilization series and weights consistent with S&T concept
  - Industry correspondences (SIC→NAICS aggregation rules)

See `docs/EXPERT_INSERTION_POINTS.md` and `docs/appendices/APPENDIX_INDUSTRY_CORRESPONDENCE.md`.

## How to run the faithful validations

- Replication validation: use the master pipeline validator (`run_replication.py --validate-only`).
- Textual/identity checks: `src/validation/textual_consistency_checks.py`.
- Perfect replication engine (Phase 1-only): `src/core/perfect_replication_engine.py`.

If you prefer VS Code tasks, see `.vscode/tasks.json` entries named:
- “Run replication validator (faithful)”
- “Run textual checks (faithful)”

## Claims discipline

- Only claim “perfect replication” for variables whose definitions are implemented per the book and pass strict thresholds (MAE ≤ 0.01, max |err| ≤ 0.03).
- Otherwise document the definitional gap and mark the item “pending exact definition,” not “perfect.”

## Next steps to complete faithful replication

- Implement gK using S&T’s exact In/K* definitions and deflators.
- Finalize modern SP and K mappings to S&T-equivalent sources/lines via config files.
- Document the chosen utilization series/weights and deflators/base-year conventions.
- Route all discretionary choices through configs, with small validators and summary reports.
