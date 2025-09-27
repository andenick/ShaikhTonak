#!/usr/bin/env python3
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
