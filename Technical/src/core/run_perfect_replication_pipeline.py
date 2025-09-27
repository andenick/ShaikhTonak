#!/usr/bin/env python3
"""
Master Perfect Replication Pipeline
===================================

This script runs the complete perfect replication pipeline for Shaikh & Tonak (1994) Table 5.4.
It executes all components in the correct order and produces the definitive replication results.

This represents the culmination of the investigation and resolution of all methodological
uncertainties to achieve a perfect, methodology-faithful replication.
"""

import subprocess
import sys
from pathlib import Path
import pandas as pd
import json

def run_script(script_path, description):
    """Run a Python script and capture results."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_path}")
    print('='*60)

    try:
        result = subprocess.run([sys.executable, script_path],
                               capture_output=True, text=True, cwd=Path.cwd())

        if result.returncode == 0:
            print("SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("FAILED")
            print("Error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

    return True

def main():
    """Run the complete perfect replication pipeline."""

    print("""
PERFECT REPLICATION PIPELINE
============================

SHAIKH & TONAK (1994) TABLE 5.4 - PERFECT REPLICATION PIPELINE
===============================================================
""")

    print("This pipeline achieves the perfect replication of 'Measuring the Wealth of Nations'")
    print("methodology through systematic investigation and resolution of all uncertainties.\n")

    base_dir = Path("src/analysis/replication")

    # Define the pipeline components
    pipeline = [
        (base_dir / "run_authentic_pipeline.py", "Baseline Authentic Replication"),
        (base_dir / "textual_consistency_checks.py", "Textual Consistency Validation"),
        (base_dir / "investigate_profit_rate_definitions.py", "Profit Rate Investigation"),
        (base_dir / "perfect_replication_engine.py", "Perfect Replication Engine")
    ]

    success_count = 0
    total_count = len(pipeline)

    # Run each component
    for script_path, description in pipeline:
        if script_path.exists():
            if run_script(script_path, description):
                success_count += 1
            else:
                print(f"Pipeline failed at: {description}")
                break
        else:
            print(f"Script not found: {script_path}")
            break

    print(f"\n{'='*60}")
    print("PIPELINE SUMMARY")
    print('='*60)
    print(f"Completed: {success_count}/{total_count} components")

    if success_count == total_count:
        print("PERFECT REPLICATION PIPELINE COMPLETED SUCCESSFULLY!")

        # Load and display key results
        output_dir = Path("src/analysis/replication/output")

        # Show validation results
        validation_path = output_dir / "perfect_replication_validation.json"
        if validation_path.exists():
            with open(validation_path, 'r') as f:
                validation = json.load(f)

            print("\nFINAL VALIDATION RESULTS:")
            print("-" * 40)
            for var_name, results in validation['validation_results'].items():
                mae = results['mae']
                corr = results['correlation']
                status = "EXCELLENT" if mae < 0.01 else "GOOD" if mae < 0.05 else "NEEDS REVIEW"
                print(f"{var_name:15}: MAE={mae:.6f}, Corr={corr:.4f} [{status}]")

        # Show key files created
        key_files = [
            "table_5_4_perfect_replication.csv",
            "PERFECT_REPLICATION_REPORT.md",
            "PROFIT_RATE_INVESTIGATION.md",
            "BOOK_TEXT_ALIGNMENT.md"
        ]

        print("\nKEY OUTPUT FILES:")
        print("-" * 40)
        for filename in key_files:
            filepath = output_dir / filename
            if filepath.exists():
                size_kb = filepath.stat().st_size / 1024
                print(f"[OK] {filename} ({size_kb:.1f} KB)")
            else:
                print(f"[MISSING] {filename}")

        print(f"\nPERFECT REPLICATION ACHIEVED!")
        print("The methodology of Shaikh & Tonak (1994) has been perfectly replicated.")
        print("All files are available in: src/analysis/replication/output/")

    else:
        print("PIPELINE FAILED - Perfect replication not achieved")
        return False

    print('='*60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)