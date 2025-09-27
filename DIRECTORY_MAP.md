# Directory Map (High-Signal)

- Technical/
  - Technical/src/analysis/replication — Reproduce historical tables (e.g., Table 5.4)
  - Technical/src/analysis/validation — Cross-validation utilities
  - Technical/src/extension — Modern extension (integration, faithful/academic variants)
  - Technical/scripts/ — Build scripts and utilities (latex build, chart generation)
  - Technical/docs/methodology/ — Full methodology LaTeX
  - Technical/docs/latex/ — Explainer, Validation, Bird's-Eye, charts
  - Technical/data/historical/book_tables/ — Book table CSVs (replication targets)
  - Technical/data/historical/processed/ — Processed historical outputs
  - Technical/data/unified_database/unified_database/ — Unified DB (CSV/XLSX) with metadata/logs
  - Technical/data/modern/** — Integrated inputs and final results (faithful/academic/klems)
  - Technical/data/source_pdfs/keyPDFs/ — Source publications (NIPA, BLS, BEA)
- Output/
  - Output/pdfs/** — Built PDFs (CI uploads artifacts here)

## Build Commands
- Build all LaTeX docs: `./Technical/scripts/build-latex.sh` (defaults to Output/pdfs)
- Generate charts used in Bird's-Eye: `python Technical/scripts/generate_charts.py`

## Key Documents
- Technical/docs/methodology/SHAIKH_TONAK_METHODOLOGY.tex
- Technical/docs/latex/PROJECT_LATEX_EXPLAINER.tex
- Technical/docs/latex/PROJECT_BIRDS_EYE_VIEW.tex
- Technical/docs/NICK_INSTRUCTIONS.md
- PROJECT_INDEX.md
