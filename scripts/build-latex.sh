#!/usr/bin/env bash
set -euo pipefail

# Build all LaTeX documents in docs/latex and docs/methodology
# Usage: scripts/build-latex.sh [--outdir Output/pdfs]

OUTDIR="Output/pdfs"
if [ "${1-}" = "--outdir" ] && [ -n "${2-}" ]; then
  OUTDIR="$2"
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOC_DIRS="$ROOT_DIR/docs/latex $ROOT_DIR/docs/methodology"
LATEX_COPY_DIR="Output/latex"

build_one() {
  tex_file="$1"
  base_dir="$(dirname "$tex_file")"
  name="$(basename "$tex_file" .tex)"

  mkdir -p "$OUTDIR/$name"
  latexmk -f -pdf -outdir="$OUTDIR/$name" "$tex_file" | cat
  echo "Built: $OUTDIR/$name/$name.pdf"
}

for dir in $DOC_DIRS; do
  if [ -d "$dir" ]; then
    for tex in "$dir"/*.tex; do
      [ -e "$tex" ] || continue
      build_one "$tex"
    done
  fi
done

# Copy LaTeX sources for reference into Output/latex
mkdir -p "$LATEX_COPY_DIR"
for dir in $DOC_DIRS; do
  if [ -d "$dir" ]; then
    find "$dir" -maxdepth 1 -type f -name '*.tex' -exec cp {} "$LATEX_COPY_DIR" \;
  fi
done
