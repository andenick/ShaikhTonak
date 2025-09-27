"""
Run KLEMS Analysis (separate from main S&T update)
This runner executes non-integrated KLEMS analyses to keep methodology boundaries clear.
"""

import sys
from pathlib import Path

# Ensure src is on the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from extension.klems_unit_analysis import KLEMSUnitAnalyzer


def main():
    analyzer = KLEMSUnitAnalyzer()
    results = analyzer.run_analysis()
    # Simple status print; this script intentionally does not write main outputs
    if results and results.get('best_scaling_factor'):
        print("KLEMS analysis complete. Scaling exploration results available in memory.")
    else:
        print("KLEMS analysis complete (no scaling adopted). See logs for details.")


if __name__ == "__main__":
    main()
