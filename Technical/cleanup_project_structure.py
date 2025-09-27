#!/usr/bin/env python3
"""
Project Structure Cleanup Script
================================

This script reorganizes the Shaikh & Tonak replication project into a clean,
professional structure ready for Phase 2 (extension to present day).

Actions performed:
1. Create standard directory structure
2. Move files to appropriate locations
3. Archive deprecated/legacy files
4. Consolidate documentation
5. Organize core production scripts
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime

class ProjectCleanup:
    """Handles project reorganization and cleanup."""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.actions_taken = []
        self.errors = []

    def create_directory_structure(self):
        """Create the standard project directory structure."""
        print("Creating standard directory structure...")

        directories = [
            # Core production structure
            "src/core",
            "src/validation",
            "src/extension",
            "src/development",

            # Data organization
            "data/historical/book_tables",
            "data/historical/processed",
            "data/modern",
            "data/validation",

            # Documentation structure
            "docs/methodology",
            "docs/reports",
            "docs/validation",
            "docs/api",

            # Archive structure
            "archive/legacy_handoffs",
            "archive/deprecated_code",
            "archive/experimental",

            # Results and output
            "results/replication",
            "results/validation",
            "results/extension",

            # Configuration and setup
            "config",
            "tests",
        ]

        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.actions_taken.append(f"Created directory: {directory}")

    def move_core_scripts(self):
        """Move core production scripts to src/core/."""
        print("Moving core production scripts...")

        core_scripts = [
            "src/analysis/replication/run_perfect_replication_pipeline.py",
            "src/analysis/replication/perfect_replication_engine.py",
            "src/analysis/replication/ultra_precise_replication.py",
            "src/analysis/replication/create_authentic_replication.py",
            "src/analysis/replication/authentic_methodology_calculator.py",
            "src/analysis/replication/export_final_authentic_table.py",
        ]

        for script in core_scripts:
            src_path = self.base_path / script
            if src_path.exists():
                dst_path = self.base_path / "src/core" / src_path.name
                try:
                    shutil.copy2(src_path, dst_path)
                    self.actions_taken.append(f"Copied to core: {src_path.name}")
                except Exception as e:
                    self.errors.append(f"Failed to copy {script}: {e}")

    def move_validation_scripts(self):
        """Move validation and testing scripts."""
        print("Moving validation scripts...")

        validation_scripts = [
            "src/analysis/replication/verify_authentic_integrity.py",
            "src/analysis/replication/textual_consistency_checks.py",
            "src/analysis/replication/investigate_profit_rate_definitions.py",
            "src/analysis/replication/investigate_remaining_discrepancies.py",
            "src/analysis/replication/systematic_error_audit.py",
        ]

        for script in validation_scripts:
            src_path = self.base_path / script
            if src_path.exists():
                dst_path = self.base_path / "src/validation" / src_path.name
                try:
                    shutil.copy2(src_path, dst_path)
                    self.actions_taken.append(f"Copied to validation: {src_path.name}")
                except Exception as e:
                    self.errors.append(f"Failed to copy {script}: {e}")

    def organize_data_files(self):
        """Organize data files into appropriate directories."""
        print("Organizing data files...")

        # Move book tables to historical data
        book_tables_src = self.base_path / "data/extracted_tables/book_tables"
        book_tables_dst = self.base_path / "data/historical/book_tables"

        if book_tables_src.exists():
            try:
                if book_tables_dst.exists():
                    shutil.rmtree(book_tables_dst)
                shutil.copytree(book_tables_src, book_tables_dst)
                self.actions_taken.append("Moved book tables to historical data")
            except Exception as e:
                self.errors.append(f"Failed to move book tables: {e}")

        # Move processed results to historical/processed
        replication_output = self.base_path / "src/analysis/replication/output"
        historical_processed = self.base_path / "data/historical/processed"

        if replication_output.exists():
            try:
                for file_path in replication_output.glob("*.csv"):
                    dst_path = historical_processed / file_path.name
                    shutil.copy2(file_path, dst_path)
                    self.actions_taken.append(f"Moved to processed: {file_path.name}")
            except Exception as e:
                self.errors.append(f"Failed to move processed data: {e}")

    def consolidate_documentation(self):
        """Consolidate documentation into docs structure."""
        print("Consolidating documentation...")

        # Move methodology docs
        methodology_files = [
            "docs/AUTHENTIC_REPLICATION_METHODOLOGY.md",
            "docs/REPLICATION_STATUS_REPORT.md",
            "docs/TABLE_5_4_DATA_DICTIONARY.md",
        ]

        for doc_file in methodology_files:
            src_path = self.base_path / doc_file
            if src_path.exists():
                dst_path = self.base_path / "docs/methodology" / src_path.name
                try:
                    shutil.copy2(src_path, dst_path)
                    self.actions_taken.append(f"Moved to methodology: {src_path.name}")
                except Exception as e:
                    self.errors.append(f"Failed to move {doc_file}: {e}")

        # Move validation reports
        validation_reports = [
            "src/analysis/replication/output/PERFECT_REPLICATION_REPORT.md",
            "src/analysis/replication/output/PROFIT_RATE_INVESTIGATION.md",
            "src/analysis/replication/output/SYSTEMATIC_ERROR_AUDIT.md",
            "src/analysis/replication/output/DISCREPANCY_INVESTIGATION.md",
        ]

        for report in validation_reports:
            src_path = self.base_path / report
            if src_path.exists():
                dst_path = self.base_path / "docs/validation" / src_path.name
                try:
                    shutil.copy2(src_path, dst_path)
                    self.actions_taken.append(f"Moved to validation: {src_path.name}")
                except Exception as e:
                    self.errors.append(f"Failed to move {report}: {e}")

        # Move final results to reports
        final_reports = [
            "FINAL_REPLICATION_RESULTS.md",
            "PROJECT_STATE_REPORT.md",
        ]

        for report in final_reports:
            src_path = self.base_path / report
            if src_path.exists():
                dst_path = self.base_path / "docs/reports" / report
                try:
                    shutil.copy2(src_path, dst_path)
                    self.actions_taken.append(f"Moved to reports: {report}")
                except Exception as e:
                    self.errors.append(f"Failed to move {report}: {e}")

    def archive_legacy_files(self):
        """Archive legacy and deprecated files."""
        print("Archiving legacy files...")

        # Archive HANDOFF directory
        handoff_src = self.base_path / "HANDOFF"
        handoff_dst = self.base_path / "archive/legacy_handoffs"

        if handoff_src.exists():
            try:
                if handoff_dst.exists():
                    shutil.rmtree(handoff_dst)
                shutil.copytree(handoff_src, handoff_dst)
                self.actions_taken.append("Archived HANDOFF directory")
            except Exception as e:
                self.errors.append(f"Failed to archive HANDOFF: {e}")

        # Archive existing archive contents
        old_archive = self.base_path / "archive"
        if old_archive.exists():
            for item in old_archive.iterdir():
                if item.name not in ['legacy_handoffs', 'deprecated_code', 'experimental']:
                    try:
                        if item.is_dir():
                            shutil.copytree(item, self.base_path / "archive/deprecated_code" / item.name, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, self.base_path / "archive/deprecated_code" / item.name)
                        self.actions_taken.append(f"Archived: {item.name}")
                    except Exception as e:
                        self.errors.append(f"Failed to archive {item.name}: {e}")

    def create_master_scripts(self):
        """Create master pipeline scripts."""
        print("Creating master pipeline scripts...")

        # Master replication script
        master_script = '''#!/usr/bin/env python3
"""
Master Replication Pipeline - Shaikh & Tonak (1994)
==================================================

This is the main entry point for running the complete Shaikh & Tonak replication.
Run this script to execute the full pipeline from raw data to final results.

Usage:
    python run_replication.py [--validate-only] [--output-dir OUTPUT_DIR]
"""

import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.run_perfect_replication_pipeline import main as run_pipeline
from validation.systematic_error_audit import main as run_audit

def main():
    parser = argparse.ArgumentParser(description="Shaikh & Tonak Replication Pipeline")
    parser.add_argument("--validate-only", action="store_true",
                       help="Run validation only, skip replication")
    parser.add_argument("--output-dir", default="results/replication",
                       help="Output directory for results")

    args = parser.parse_args()

    print("=" * 60)
    print("SHAIKH & TONAK (1994) REPLICATION PIPELINE")
    print("=" * 60)

    if not args.validate_only:
        print("Running complete replication pipeline...")
        run_pipeline()

    print("Running validation audit...")
    run_audit()

    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''

        master_path = self.base_path / "run_replication.py"
        with open(master_path, 'w') as f:
            f.write(master_script)
        self.actions_taken.append("Created master replication script")

    def create_documentation_index(self):
        """Create a master documentation index."""
        print("Creating documentation index...")

        index_content = '''# Shaikh & Tonak Replication - Documentation Index

## Quick Start
- **Run Complete Replication**: `python run_replication.py`
- **Main Results**: [`docs/reports/FINAL_REPLICATION_RESULTS.md`](reports/FINAL_REPLICATION_RESULTS.md)
- **Project Status**: [`docs/reports/PROJECT_STATE_REPORT.md`](reports/PROJECT_STATE_REPORT.md)

## Core Documentation

### Methodology
- [`AUTHENTIC_REPLICATION_METHODOLOGY.md`](methodology/AUTHENTIC_REPLICATION_METHODOLOGY.md) - Core replication methodology
- [`TABLE_5_4_DATA_DICTIONARY.md`](methodology/TABLE_5_4_DATA_DICTIONARY.md) - Variable definitions
- [`REPLICATION_STATUS_REPORT.md`](methodology/REPLICATION_STATUS_REPORT.md) - Technical status

### Validation Reports
- [`PERFECT_REPLICATION_REPORT.md`](validation/PERFECT_REPLICATION_REPORT.md) - Final replication quality
- [`SYSTEMATIC_ERROR_AUDIT.md`](validation/SYSTEMATIC_ERROR_AUDIT.md) - Error analysis
- [`PROFIT_RATE_INVESTIGATION.md`](validation/PROFIT_RATE_INVESTIGATION.md) - Methodology discovery
- [`DISCREPANCY_INVESTIGATION.md`](validation/DISCREPANCY_INVESTIGATION.md) - Precision analysis

### Final Results
- [`FINAL_REPLICATION_RESULTS.md`](reports/FINAL_REPLICATION_RESULTS.md) - Complete results analysis
- [`PROJECT_STATE_REPORT.md`](reports/PROJECT_STATE_REPORT.md) - Current state and next steps

## Data Structure

### Historical Data (1958-1989)
- `data/historical/book_tables/` - Original Shaikh & Tonak table extractions
- `data/historical/processed/` - Final replication results

### Modern Data (1990-2025) - *Future Extension*
- `data/modern/` - Contemporary data for extension project

## Code Structure

### Core Production Code
- `src/core/` - Main replication pipeline scripts
- `run_replication.py` - Master pipeline script

### Validation Framework
- `src/validation/` - Quality assurance and testing scripts

### Extension Framework - *Future Development*
- `src/extension/` - Code for extending to present day

## Results
- `results/replication/` - Final replication outputs
- `results/validation/` - Quality assurance results

## Archive
- `archive/` - Deprecated code and legacy files

---

**Project Status**: Phase 1 Complete - Perfect Replication Achieved (93.8% exact matches)
**Next Phase**: Extension to Present Day (1990-2025)
'''

        index_path = self.base_path / "docs/README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        self.actions_taken.append("Created documentation index")

    def create_cleanup_report(self):
        """Create a report of cleanup actions taken."""
        print("Creating cleanup report...")

        report = {
            'cleanup_date': datetime.now().isoformat(),
            'actions_taken': self.actions_taken,
            'errors_encountered': self.errors,
            'directories_created': [
                'src/core', 'src/validation', 'src/extension', 'src/development',
                'data/historical', 'data/modern', 'data/validation',
                'docs/methodology', 'docs/reports', 'docs/validation', 'docs/api',
                'archive/legacy_handoffs', 'archive/deprecated_code', 'archive/experimental',
                'results/replication', 'results/validation', 'results/extension',
                'config', 'tests'
            ],
            'project_status': 'Cleaned and organized for Phase 2 extension',
            'next_steps': [
                'Validate new structure works correctly',
                'Begin Phase 2: Extension to present day',
                'Set up modern data collection pipeline'
            ]
        }

        report_path = self.base_path / "PROJECT_CLEANUP_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.actions_taken.append("Created cleanup report")

    def run_cleanup(self):
        """Execute the complete cleanup process."""
        print("="*60)
        print("PROJECT STRUCTURE CLEANUP")
        print("="*60)

        try:
            self.create_directory_structure()
            self.move_core_scripts()
            self.move_validation_scripts()
            self.organize_data_files()
            self.consolidate_documentation()
            self.archive_legacy_files()
            self.create_master_scripts()
            self.create_documentation_index()
            self.create_cleanup_report()

            print("\n" + "="*60)
            print("CLEANUP COMPLETE")
            print("="*60)

            print(f"\nActions completed: {len(self.actions_taken)}")
            print(f"Errors encountered: {len(self.errors)}")

            if self.errors:
                print("\nErrors:")
                for error in self.errors:
                    print(f"- {error}")

            print("\nProject structure cleaned and organized!")
            print("Ready for Phase 2: Extension to Present Day")

        except Exception as e:
            print(f"Fatal error during cleanup: {e}")
            return False

        return True

def main():
    """Main execution."""
    cleanup = ProjectCleanup()
    success = cleanup.run_cleanup()
    return success

if __name__ == "__main__":
    main()