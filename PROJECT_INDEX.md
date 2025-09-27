# Project Index and Structure

This is the root index for agents and contributors. It provides a concise map of the project, its purpose, where things live, and how to build the documentation.

## Purpose
- Replicate and extend Shaikh & Tonak (1994) with high-fidelity historical reproduction and modern extension.
- Provide transparent methodology, validation, and reproducible outputs.

## Structure
- Technical/ — full working repository (code, data, docs, scripts)
  - Technical/src/ — analysis, replication, validation, extension
  - Technical/data/ — historical, unified database, modern inputs/outputs, source PDFs
  - Technical/docs/latex/ — focused LaTeX docs (explainer, validation, bird’s-eye)
  - Technical/docs/methodology/ — complete methodology LaTeX
  - Technical/scripts/ — build scripts and maintenance utilities
- Output/ — most important outputs for quick access
  - Output/pdfs/ — built PDFs of LaTeX docs (CI artifacts)

## Key Documents
- Technical/docs/methodology/SHAIKH_TONAK_METHODOLOGY.tex — full methodology
- Technical/docs/latex/PROJECT_LATEX_EXPLAINER.tex — navigational guide
- Technical/docs/latex/PROJECT_BIRDS_EYE_VIEW.tex — high-level context
- Technical/docs/NICK_INSTRUCTIONS.md — operational instructions

## Build Docs
- Build all PDFs: `./Technical/scripts/build-latex.sh` (outputs to Output/pdfs)
- CI builds PDFs and uploads artifacts via `.github/workflows/latex.yml`

## Data Map (high-signal)
- Book tables (replication targets): `Technical/data/historical/book_tables/`
- Historical processed: `Technical/data/historical/processed/`
- Unified database: `Technical/data/unified_database/unified_database/`
- Modern integrated: `Technical/data/modern/integrated/`
- Modern results (faithful/academic/klems): `Technical/data/modern/final_results*/`
- Source PDFs: `Technical/data/source_pdfs/keyPDFs/`

## Next Steps
- Generate plots for birds-eye figures from modern results to embed in PDFs
- Keep NICK_INSTRUCTIONS.md updated as pipelines evolve
