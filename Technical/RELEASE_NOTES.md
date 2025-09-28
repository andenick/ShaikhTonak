# v1.0.0 — Initial Organized Release

## Highlights
- Technical/Output reorganization for clarity and reproducibility
- Robust LaTeX build pipeline (latexmk) and CI artifacts
- Comprehensive methodology and navigational docs
- Figures and Bird's-Eye overview added

## Contents
- PDFs in `Output/pdfs/`:
  - BirdsEye/PROJECT_BIRDS_EYE_VIEW.pdf
  - CodeExplainer/SHAIKH_TONAK_CODE_EXPLAINER.pdf
  - Explainer/PROJECT_LATEX_EXPLAINER.pdf
  - Validation/SHAIKH_TONAK_VALIDATION_REPORT.pdf
- Code, data, and docs under `Technical/`
- Quick navigation: `PROJECT_INDEX.md` and `DIRECTORY_MAP.md`
- Contributing guidelines: `CONTRIBUTING.md`
- Full changes: `CHANGES_LOG.md`

## Build
- `./Technical/scripts/build-latex.sh` → PDFs to `Output/pdfs/`
- CI builds and uploads artifacts from `Output/pdfs/`
