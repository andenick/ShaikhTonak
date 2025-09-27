#!/usr/bin/env python3
"""
Debug script to understand table structure
"""

import pandas as pd
from pathlib import Path

# Load the tables
data_path = Path("data/extracted_tables/book_tables")
part1 = pd.read_csv(data_path / "table_p36_camelot[page]_0.csv")
part2 = pd.read_csv(data_path / "table_p37_camelot[page]_0.csv")

print("=== PART 1 STRUCTURE ===")
print("Shape:", part1.shape)
print("Columns:", list(part1.columns))
print("First few rows:")
print(part1.head())
print()

print("=== PART 2 STRUCTURE ===")
print("Shape:", part2.shape)
print("Columns:", list(part2.columns))
print("First few rows:")
print(part2.head())
print()

# Check if Part 2 columns are offsets from 1974
print("=== PART 2 YEAR ANALYSIS ===")
for i, col in enumerate(part2.columns[1:]):  # Skip first column
    try:
        offset = int(col)
        year = 1974 + offset
        print(f"Column '{col}' -> Year {year}")
    except:
        print(f"Column '{col}' -> Not numeric")

print()
print("Expected range for Part 2: 1974-1989")
print("Column range:", part2.columns[1], "to", part2.columns[-1])