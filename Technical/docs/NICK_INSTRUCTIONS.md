# Nick Instructions (Updated)

Date: 2025-09-22

## Scope
This document tells you exactly how to run the current project, what to verify, where outputs live, and how to keep everything faithful to Shaikh & Tonak.

## Prerequisites
- Python environment with pandas, matplotlib, seaborn installed.
- Data already staged in data/historical/processed and data/modern/* (we don't touch raw).

## Run order
1. Phase 2 Integration
   - Purpose: Merge historical data, modern SP and K, capacity utilization, and diagnostics into one integrated file.
   - How: python src/extension/phase2_data_integration.py
   - Output: data/modern/integrated/complete_st_timeseries_1958_2025.csv
   - Metadata: data/modern/integrated/integration_metadata.json (includes units)

2. Faithful S&T-only Pipeline
   - Purpose: Preserve historical r' exactly; compute modern r via r = SP/(K×u) strictly.
   - How: python src/extension/phase2_faithful_st_only.py
   - Outputs:
     - data/modern/final_results_faithful/shaikh_tonak_faithful_1958_1989.csv
     - data/modern/final_results_faithful/shaikh_tonak_faithful_1958_2025.csv
     - results/extension/plots/*.png
     - results/extension/FAITHFUL_UPDATE_REPORT.md

3. Final Packaging & Report
   - Purpose: Organize deliverables and produce a consolidated final report with plots.
   - How: python src/extension/final_report_and_organization.py
   - Outputs (folders under results/final/):
     - replication/ (historical, includes faithful 1958–1989 and copies of perfect replication if present)
     - expansion/ (faithful 1990–2023 slice)
     - combined/ (faithful 1958–2025 chained CSV)
     - plots/ (curated figures)
     - FAITHFUL_REPLICATION_AND_EXPANSION_REPORT.md
     - DIRECTORY_MAP.md

## Units and Identity Policy
- r is unitless and must be computed as r = SP/(K×u).
- SP (modern) and K (modern) must be in the same currency (Millions of current dollars).
- u must be a 0–1 fraction. The pipeline will convert percent to fraction when detected.
- Never scale or “fix” levels arbitrarily. If something diverges, document it.

## Quick validation checklist
- Historical r' (1958–1989) in combined CSV equals book values; 1974 is blank.
- modern_SP_st_consistent and modern_K_st_consistent have coverage in integrated CSV (check metadata coverage counts).
- Capacity utilization detected as percent and converted (notes column in faithful CSV should record this).
- Final report exists and shows modern mean r ~0.12 with sensible range.

## Where to find things (Repository Layout)
- Integrated: Technical/data/modern/integrated/
- Faithful outputs: Technical/data/modern/final_results_faithful/
- Academically-sound: Technical/data/modern/final_results_academically_sound/
- KLEMS variants: Technical/data/modern/final_results_with_klems/
- Unified database bundle: Technical/data/unified_database/unified_database/
- Historical processed: Technical/data/historical/processed/
- Book tables (replication targets): Technical/data/historical/book_tables/
- Source PDFs: Technical/data/source_pdfs/keyPDFs/
- LaTeX docs: Technical/docs/latex/ and Technical/docs/methodology/
- Built PDFs: Output/pdfs/

## Maintenance
- Don’t edit raw data.
- When adding new data years, update the staged modern SP and K files first, then rerun integration → faithful → packaging.
- Document any changes to sources or definitions in results/extension/FAITHFUL_UPDATE_REPORT.md.

## Build Documentation (PDFs)
- Build all PDFs: `./Technical/scripts/build-latex.sh` (outputs to Output/pdfs)
- CI builds and uploads artifacts from Output/pdfs via .github/workflows/latex.yml

## Optional diagnostics (keep separate from faithful)
- Corporate profits and KLEMS-based series for sensitivity analysis.
- Keep these labeled “diagnostic” and out of faithful computations.

## Contact & Collaboration
- When in doubt, check docs/NICK_SHEET.md first.
- Keep communication crisp: what changed, why it matters, and where to see it.
