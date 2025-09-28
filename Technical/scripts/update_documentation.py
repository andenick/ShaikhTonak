#!/usr/bin/env python3
"""
Automated Documentation Update Script
Shaikh & Tonak Project

This script provides automated updating of all LaTeX documentation
to ensure PDFs are always current and reflect project status.

Usage:
    python update_documentation.py [--clean] [--force]

Options:
    --clean: Clean all intermediate LaTeX files
    --force: Force rebuild even if PDFs are newer than source
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

class DocumentationUpdater:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.latex_dir = self.project_root / "Technical" / "docs" / "latex"
        self.output_pdf_dir = self.project_root / "Output" / "PDFs"

    def check_directories(self):
        """Verify required directories exist"""
        if not self.latex_dir.exists():
            raise FileNotFoundError(f"LaTeX directory not found: {self.latex_dir}")
        if not self.output_pdf_dir.exists():
            self.output_pdf_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created output directory: {self.output_pdf_dir}")

    def get_tex_files(self):
        """Get all .tex files in the LaTeX directory"""
        return list(self.latex_dir.glob("*.tex"))

    def build_pdf(self, tex_file, quiet=True):
        """Build a single PDF from LaTeX source"""
        print(f"Building: {tex_file.name}")

        cmd = ["pdflatex", tex_file.name]
        if quiet:
            result = subprocess.run(
                cmd,
                cwd=self.latex_dir,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(cmd, cwd=self.latex_dir)

        if result.returncode != 0:
            print(f"ERROR building {tex_file.name}")
            if quiet and result.stderr:
                print(f"Error details: {result.stderr}")
            return False
        return True

    def deploy_pdfs(self):
        """Copy all PDFs to the Output directory"""
        pdf_files = list(self.latex_dir.glob("*.pdf"))
        deployed_count = 0

        for pdf_file in pdf_files:
            destination = self.output_pdf_dir / pdf_file.name
            try:
                subprocess.run(["cp", str(pdf_file), str(destination)], check=True)
                deployed_count += 1
            except subprocess.CalledProcessError:
                print(f"Warning: Failed to copy {pdf_file.name}")

        print(f"Deployed {deployed_count} PDFs to Output/PDFs/")
        return deployed_count

    def clean_intermediate_files(self):
        """Clean LaTeX intermediate files"""
        extensions = ['.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk']
        cleaned_count = 0

        for ext in extensions:
            files = list(self.latex_dir.glob(f"*{ext}"))
            for file in files:
                try:
                    file.unlink()
                    cleaned_count += 1
                except OSError:
                    pass

        if cleaned_count > 0:
            print(f"Cleaned {cleaned_count} intermediate files")

    def verify_output_structure(self):
        """Verify the Output/PDFs directory contains only PDF files"""
        items = list(self.output_pdf_dir.iterdir())
        pdf_files = [item for item in items if item.is_file() and item.suffix == '.pdf']
        directories = [item for item in items if item.is_dir()]
        other_files = [item for item in items if item.is_file() and item.suffix != '.pdf']

        print(f"Output/PDFs/ structure verification:")
        print(f"  PDF files: {len(pdf_files)}")

        if directories:
            print(f"  WARNING: Found {len(directories)} directories (should be 0)")
            for d in directories:
                print(f"    - {d.name}")

        if other_files:
            print(f"  WARNING: Found {len(other_files)} non-PDF files")
            for f in other_files:
                print(f"    - {f.name}")

        return len(directories) == 0 and len(other_files) == 0

    def update_all(self, clean=False, force=False, quiet=True):
        """Main update process"""
        print(f"LaTeX Documentation Update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Check directories
        self.check_directories()

        # Get all LaTeX files
        tex_files = self.get_tex_files()
        print(f"Found {len(tex_files)} LaTeX files")

        # Build all PDFs
        success_count = 0
        for tex_file in tex_files:
            if self.build_pdf(tex_file, quiet=quiet):
                success_count += 1

        print(f"Successfully built {success_count}/{len(tex_files)} PDFs")

        # Deploy PDFs
        deployed_count = self.deploy_pdfs()

        # Verify structure
        structure_ok = self.verify_output_structure()

        # Clean intermediate files if requested
        if clean:
            self.clean_intermediate_files()

        # Summary
        print("=" * 60)
        print("Update Summary:")
        print(f"  LaTeX files processed: {len(tex_files)}")
        print(f"  PDFs built successfully: {success_count}")
        print(f"  PDFs deployed: {deployed_count}")
        print(f"  Output structure clean: {'Yes' if structure_ok else 'No'}")

        if success_count == len(tex_files) and structure_ok:
            print("Documentation update completed successfully!")
            return True
        else:
            print("Some issues were encountered during update")
            return False

def main():
    parser = argparse.ArgumentParser(description="Update Shaikh & Tonak project documentation")
    parser.add_argument("--clean", action="store_true", help="Clean intermediate LaTeX files")
    parser.add_argument("--force", action="store_true", help="Force rebuild all PDFs")
    parser.add_argument("--verbose", action="store_true", help="Show detailed LaTeX output")

    args = parser.parse_args()

    # Find project root (assuming script is in Technical/scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    updater = DocumentationUpdater(project_root)

    try:
        success = updater.update_all(
            clean=args.clean,
            force=args.force,
            quiet=not args.verbose
        )
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()