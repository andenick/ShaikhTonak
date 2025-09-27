#!/usr/bin/env python3
"""
Data Completeness Analysis for 100% Target
Identifies missing data gaps and extraction opportunities
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

def analyze_data_completeness():
    """Comprehensive analysis of data completeness gaps"""

    print("DATA COMPLETENESS ANALYSIS")
    print("=" * 50)
    print("Target: 100% data completeness for Shaikh-Tonak replication")
    print()

    # Load perfect table (if available), recovered table, or reconstructed table
    perfect_path = Path("src/analysis/replication/output/table_5_4_perfect.csv")
    recovered_path = Path("src/analysis/replication/output/table_5_4_complete.csv")

    if perfect_path.exists():
        table_path = perfect_path
        print("Analyzing PERFECT dataset...")
    elif recovered_path.exists():
        table_path = recovered_path
        print("Analyzing RECOVERED dataset...")
    else:
        table_path = Path("src/analysis/replication/output/table_5_4_reconstructed.csv")
        print("Analyzing original dataset...")

    df = pd.read_csv(table_path)

    print(f"Current dataset: {df.shape[0]} years × {df.shape[1]} variables")
    print(f"Time period: {df['year'].min()}-{df['year'].max()}")
    print()

    # Calculate completeness by variable
    print("VARIABLE COMPLETENESS ANALYSIS")
    print("-" * 30)

    completeness_stats = {}
    total_years = len(df)

    for col in df.columns:
        if col == 'year':
            continue

        non_null_count = df[col].notna().sum()
        completeness_pct = (non_null_count / total_years) * 100
        missing_count = total_years - non_null_count

        completeness_stats[col] = {
            'available': int(non_null_count),
            'missing': int(missing_count),
            'completeness_pct': float(completeness_pct),
            'missing_years': [int(y) for y in df[df[col].isna()]['year'].tolist()]
        }

        status = "COMPLETE" if completeness_pct == 100 else f"MISSING {completeness_pct:.1f}%"
        print(f"{col:12} | {non_null_count:2}/{total_years} | {status}")

    print()

    # Identify temporal gaps
    print("TEMPORAL GAP ANALYSIS")
    print("-" * 20)

    # Check for missing year 1974
    if 1974 not in df['year'].values:
        print("WARNING: Missing year 1974 (gap between Part 1 and Part 2)")

    # Analyze Part 1 vs Part 2 variable availability
    part1_years = df[df['year'] <= 1973]['year'].tolist()
    part2_years = df[df['year'] >= 1975]['year'].tolist()

    print(f"Part 1 years: {len(part1_years)} ({min(part1_years)}-{max(part1_years)})")
    print(f"Part 2 years: {len(part2_years)} ({min(part2_years)}-{max(part2_years)})")
    print()

    # Variables only in Part 1
    part1_only_vars = []
    part2_only_vars = []

    for col in df.columns:
        if col == 'year':
            continue

        part1_data = df[df['year'] <= 1973][col].notna().any()
        part2_data = df[df['year'] >= 1975][col].notna().any()

        if part1_data and not part2_data:
            part1_only_vars.append(col)
        elif part2_data and not part1_data:
            part2_only_vars.append(col)

    print("VARIABLE COVERAGE BY PERIOD")
    print("-" * 27)
    print(f"Part 1 only variables ({len(part1_only_vars)}): {part1_only_vars}")
    print(f"Part 2 only variables ({len(part2_only_vars)}): {part2_only_vars}")
    print()

    # Overall completeness calculation
    total_cells = df.shape[0] * (df.shape[1] - 1)  # Exclude 'year' column
    filled_cells = df.iloc[:, 1:].notna().sum().sum()  # Exclude 'year' column
    overall_completeness = (filled_cells / total_cells) * 100

    print("OVERALL COMPLETENESS SUMMARY")
    print("-" * 28)
    print(f"Total data points: {total_cells:,}")
    print(f"Filled data points: {filled_cells:,}")
    print(f"Missing data points: {total_cells - filled_cells:,}")
    print(f"Current completeness: {overall_completeness:.1f}%")
    print(f"Target completeness: 100.0%")
    print(f"Gap to target: {100 - overall_completeness:.1f}%")
    print()

    # Identify specific missing data opportunities
    print("MISSING DATA RECOVERY OPPORTUNITIES")
    print("-" * 35)

    opportunities = []

    # 1. Year 1974 gap
    opportunities.append({
        'type': 'temporal_gap',
        'description': 'Missing year 1974 - bridge between Part 1 and Part 2',
        'impact': 'High - critical transition year',
        'method': 'Interpolation or additional table extraction'
    })

    # 2. Part 1 variables missing from Part 2
    if part1_only_vars:
        opportunities.append({
            'type': 'variable_extension',
            'description': f'Extend {len(part1_only_vars)} Part 1 variables to Part 2 period',
            'variables': part1_only_vars,
            'impact': 'High - maintains variable consistency',
            'method': 'Additional table extraction or interpolation'
        })

    # 3. Part 2 variables missing from Part 1
    if part2_only_vars:
        opportunities.append({
            'type': 'variable_backfill',
            'description': f'Backfill {len(part2_only_vars)} Part 2 variables to Part 1 period',
            'variables': part2_only_vars,
            'impact': 'Medium - extends historical coverage',
            'method': 'Government data sources or calculation'
        })

    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp['description']}")
        print(f"   Impact: {opp['impact']}")
        print(f"   Method: {opp['method']}")
        if 'variables' in opp:
            print(f"   Variables: {opp['variables']}")
        print()

    # Save detailed analysis
    analysis_results = {
        'timestamp': datetime.now().isoformat(),
        'current_completeness': float(overall_completeness),
        'target_completeness': 100.0,
        'gap_percentage': float(100 - overall_completeness),
        'total_data_points': int(total_cells),
        'missing_data_points': int(total_cells - filled_cells),
        'variable_completeness': completeness_stats,
        'temporal_gaps': {
            'missing_1974': 1974 not in df['year'].values,
            'part1_years': [int(y) for y in part1_years],
            'part2_years': [int(y) for y in part2_years]
        },
        'variable_gaps': {
            'part1_only': part1_only_vars,
            'part2_only': part2_only_vars
        },
        'recovery_opportunities': opportunities
    }

    # Export analysis
    output_path = Path("src/analysis/replication/output/data_completeness_analysis.json")
    with open(output_path, 'w') as f:
        json.dump(analysis_results, f, indent=2)

    print(f"Detailed analysis saved to: {output_path}")
    print()

    return analysis_results

if __name__ == "__main__":
    analyze_data_completeness()