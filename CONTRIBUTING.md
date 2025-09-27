# Contributing Guide

Welcome, future agents. This guide outlines coding and documentation conventions to keep the project consistent and reproducible.

## Philosophy
- Reproducibility first: every transformation must be traceable to inputs and code.
- Book fidelity: preserve historical values; document any deviations separately.
- Transparency: prefer explicit names and clear structure over clever shortcuts.

## Code Conventions
- Language: Python 3.10+ for data/analysis scripts.
- Style: PEP 8 with meaningful identifiers (avoid 1–2 letter names). Prefer full words.
- Types: Add type hints for public functions; keep signatures explicit.
- Control flow: use guard clauses; avoid deep nesting; handle edge cases first.
- Errors: don’t silently swallow exceptions; log or raise with context.
- IO: never mutate raw data; write outputs to `Technical/data/**/processed` or `Technical/data/modern/**` as appropriate.
- Paths: use repository-relative paths documented in methodology (`Technical/data/...`).
- Notebooks: if used, commit trusted notebooks only if they are small and necessary; otherwise, convert to scripts.

## Documentation Conventions
- LaTeX
  - Sources: `Technical/docs/latex/` and `Technical/docs/methodology/`.
  - Build: `./Technical/scripts/build-latex.sh` (outputs to `Output/pdfs/`).
  - Images: place generated figures in `Technical/docs/latex/`. LaTeX should compile without images using file-existence guards.
- Markdown
  - Root overview: `PROJECT_INDEX.md`.
  - High-signal map: `DIRECTORY_MAP.md` (keep concise and current).
  - Operational instructions: `Technical/docs/NICK_INSTRUCTIONS.md`.
  - Changes history: `CHANGES_LOG.md`.

## Data Management
- Historical book tables: `Technical/data/historical/book_tables/`.
- Processed historical outputs: `Technical/data/historical/processed/`.
- Unified database bundle: `Technical/data/unified_database/unified_database/`.
- Modern data and results: `Technical/data/modern/**`.
- Source PDFs: `Technical/data/source_pdfs/keyPDFs/`.
- Do not edit raw sources; stage changes through scripts and document them.

## Scripts
- LaTeX build: `Technical/scripts/build-latex.sh`.
- Chart generation: `Technical/scripts/generate_charts.py` (produces figures for Bird’s-Eye).
- Reorg (if needed): `scripts/reorganize_to_technical_output.py` (already applied).

## CI
- GitHub Actions at `.github/workflows/latex.yml` builds PDFs and uploads artifacts from `Output/pdfs/`.

## PR Checklist
- [ ] Code passes lint and runs non-interactively.
- [ ] Paths use `Technical/...` layout; no hardcoded local absolute paths.
- [ ] Outputs written under `Technical/data/**` or `Output/` as appropriate.
- [ ] Documentation updated (methodology, explainer, DIRECTORY_MAP) if paths or processes changed.
- [ ] Rebuild LaTeX and verify PDFs under `Output/pdfs/`.

Thank you for keeping the project in top shape.
