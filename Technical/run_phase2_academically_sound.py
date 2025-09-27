"""
Run Phase 2: Academically Sound Extension (excludes KLEMS)
This script runs the conservative, economically-justified update to extend S&T to the present without using KLEMS.
"""

import sys
from pathlib import Path

# Ensure src is on the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from extension.phase2_final_academically_sound import (
    Phase2AcademicallySoundImplementation,
)


def main():
    impl = Phase2AcademicallySoundImplementation()
    success = impl.run_academically_sound_implementation()
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
