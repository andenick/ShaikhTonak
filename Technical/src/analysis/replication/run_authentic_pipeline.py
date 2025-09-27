#!/usr/bin/env python3
"""
Run the authentic pipeline: export final table and verify integrity.
"""
from pathlib import Path
import sys
import runpy

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"

def run(module_path: Path):
    sys.path.append(str(SRC))
    runpy.run_path(str(module_path))

def main():
    export = ROOT / "src/analysis/replication/export_final_authentic_table.py"
    verify = ROOT / "src/analysis/replication/verify_authentic_integrity.py"
    print("[1/2] Exporting final authentic table…")
    run(export)
    print("[2/2] Verifying authenticity…")
    run(verify)
    print("Done.")

if __name__ == "__main__":
    main()
