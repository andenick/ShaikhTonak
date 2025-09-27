# latexmk configuration for reproducible, non-interactive builds
# Engine: pdflatex (UTF-8 inputenc used in project)
$pdf_mode = 1;            # generate pdf via pdflatex
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error';

# Re-run rules
$max_repeat = 5;

# Silence most chatter, but keep errors
$recorder = 1;
$silent = 1;

# Auxiliary directories (keep tree clean if latexmk -outdir is used)
# Users can call: latexmk -outdir=build/<name>

# Default preview disabled in CI
$preview_continuous_mode = 0;

# Clean-up list
@generated_exts = (@generated_exts, 'aux','bbl','bcf','blg','fdb_latexmk','fls','log','out','run.xml','toc','synctex.gz','lot','lof','idx','ilg','ind','nav','snm','vrb','xdy');
