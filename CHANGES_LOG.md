# Changes Log (2025-09-27)

## Repository Reorganization
- Created Technical/ (full project: code, data, docs, scripts) and Output/ (deliverables).
- Moved existing contents into Technical/, leaving .github, .gitignore, Output/, PROJECT_INDEX.md at root.
- Updated CI to build PDFs into Output/pdfs via `Technical/scripts/build-latex.sh`.

## LaTeX Build System
- Updated script: `Technical/scripts/build-latex.sh` (defaults to Output/pdfs; uses latexmk -f).
- Added chart generator: `Technical/scripts/generate_charts.py` to produce figures for LaTeX docs.
- Ensured robust LaTeX docs with file-existence checks for images.

## New/Updated Documentation
- Technical/docs/latex/PROJECT_LATEX_EXPLAINER.tex: added full path inventory and build instructions (rebuilt to Output/pdfs).
- Technical/docs/latex/PROJECT_BIRDS_EYE_VIEW.tex: generated and embedded charts for profit rate, surplus components, capital+u.
- Technical/docs/methodology/SHAIKH_TONAK_METHODOLOGY.tex: added repository paths for data, modern integration location, and Output PDF note.
- Technical/docs/NICK_INSTRUCTIONS.md: updated for Technical/Output layout and build steps.
- PROJECT_INDEX.md: root index for agents (structure, key docs, data map, build commands).
- DIRECTORY_MAP.md: high-signal directory map for quick navigation.

## Outputs
- Built PDFs into Output/pdfs:
  - BirdsEye/PROJECT_BIRDS_EYE_VIEW.pdf
  - CodeExplainer/SHAIKH_TONAK_CODE_EXPLAINER.pdf
  - Explainer/PROJECT_LATEX_EXPLAINER.pdf
  - Validation/SHAIKH_TONAK_VALIDATION_REPORT.pdf

## Data and Figures
- Figures created in Technical/docs/latex:
  - profit_rate_series.png
  - surplus_components.png
  - capital_utilization.png

## Notes
- Unified database and modern results located under Technical/data/unified_database/... and Technical/data/modern/...
- Future agents: start with PROJECT_INDEX.md and DIRECTORY_MAP.md; build docs with Technical/scripts/build-latex.sh.
