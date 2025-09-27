#!/usr/bin/env python3
import sys
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent
    sys.path.append(str(base / 'src'))
    from extension.phase2_faithful_st_only import main as run
    run()


if __name__ == '__main__':
    main()
