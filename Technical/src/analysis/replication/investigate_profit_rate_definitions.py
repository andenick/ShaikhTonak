#!/usr/bin/env python3
"""
Investigate Profit Rate Definitions in Shaikh & Tonak (1994)
============================================================

This script investigates the discrepancy between the published profit rate r'
and the textbook Marxian identity r = s'/(1+c'). It tests multiple alternative
definitions to identify the exact methodology used by Shaikh & Tonak.

Key Questions:
1. Why doesn't r' = s'/(1+c') ?
2. What definition makes r' ≈ SP/(K×u) work so well?
3. Are there alternative interpretations of c', s', or denominators?
4. Can we resolve the 1973 utilization gap?

Methodology:
- Test various profit rate formulations
- Examine period-specific patterns
- Cross-validate with other economic relationships
- Document findings for perfect replication
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Paths
BASE_DIR = Path("src/analysis/replication/output")
RAW_PATH = BASE_DIR / "table_5_4_authentic_raw_merged.csv"
CALC_PATH = BASE_DIR / "table_5_4_authentic_calculated.csv"
OUT_PATH = BASE_DIR / "profit_rate_investigation.json"
REPORT_PATH = BASE_DIR / "PROFIT_RATE_INVESTIGATION.md"

def calculate_profit_rate_alternatives(df):
    """
    Test multiple alternative profit rate definitions to identify
    which matches the published r' values.
    """
    results = {}

    # Extract key variables
    r_prime = df['r\'']
    s_prime = df['s\'']
    c_prime = df['c\'']
    SP = df['SP']
    S = df['S']
    u = df['u']

    # Create K_unified: KK (1958-1973) union K (1974-1989)
    K_unified = pd.Series(index=df.index, dtype=float)
    # Use KK where available
    if 'KK' in df.columns:
        K_unified = K_unified.fillna(df['KK'])
    # Use K where KK is not available
    if 'K' in df.columns:
        K_unified = K_unified.fillna(df['K'])

    print(f"K_unified created: {K_unified.notna().sum()} non-null values")

    # Alternative 1: Standard Marxian identity
    r_standard = s_prime / (1 + c_prime)
    results['r_standard'] = {
        'formula': 'r = s\'/(1+c\')',
        'description': 'Standard textbook Marxian profit rate',
        'data': r_standard,
        'vs_published': compare_series(r_prime, r_standard)
    }

    # Alternative 2: SP/(K×u) - the one that works well
    r_sp_ku = SP / (K_unified * u)
    results['r_sp_ku'] = {
        'formula': 'r = SP/(K×u)',
        'description': 'Surplus product over capital-utilization product',
        'data': r_sp_ku,
        'vs_published': compare_series(r_prime, r_sp_ku)
    }

    # Alternative 3: S/(K×u) using S instead of SP
    r_s_ku = S / (K_unified * u)
    results['r_s_ku'] = {
        'formula': 'r = S/(K×u)',
        'description': 'Surplus over capital-utilization product',
        'data': r_s_ku,
        'vs_published': compare_series(r_prime, r_s_ku)
    }

    # Alternative 4: SP/K (without utilization adjustment)
    r_sp_k = SP / K_unified
    results['r_sp_k'] = {
        'formula': 'r = SP/K',
        'description': 'Surplus product over capital stock',
        'data': r_sp_k,
        'vs_published': compare_series(r_prime, r_sp_k)
    }

    # Alternative 5: Alternative c' interpretation - maybe c' is C/(C+V)?
    # If c' = C/(C+V), then C = c'×(C+V), so C+V = C/c' = C×(1/c')
    # Then r = S/(C+V) = S×c'/C. But we need C...
    # Let's try: if V = SP/s', then perhaps C = (SP/s')×c'/(1-c')
    V_alt = SP / s_prime
    C_alt = V_alt * c_prime / (1 - c_prime)
    r_alt_cv = SP / (C_alt + V_alt)
    results['r_alt_composition'] = {
        'formula': 'r = SP/(C+V) where C=V×c\'/(1-c\'), V=SP/s\'',
        'description': 'Alternative organic composition interpretation',
        'data': r_alt_cv,
        'vs_published': compare_series(r_prime, r_alt_cv)
    }

    # Alternative 6: Net vs gross considerations
    # Maybe there's a depreciation adjustment we're missing
    # This is speculative without more data

    return results

def compare_series(series1, series2):
    """Compare two series and return error metrics."""
    # Ensure both are Series and align indices
    if not isinstance(series1, pd.Series):
        series1 = pd.Series(series1)
    if not isinstance(series2, pd.Series):
        series2 = pd.Series(series2)

    # Align and drop NaN
    combined = pd.DataFrame({'s1': series1, 's2': series2}).dropna()
    if len(combined) == 0:
        return {'observations': 0, 'mae': np.nan, 'max_abs_err': np.nan, 'correlation': np.nan, 'rmse': np.nan, 'mean_s1': np.nan, 'mean_s2': np.nan}

    diff = combined['s1'] - combined['s2']
    return {
        'observations': len(combined),
        'mae': float(diff.abs().mean()),
        'max_abs_err': float(diff.abs().max()),
        'rmse': float(np.sqrt((diff**2).mean())),
        'correlation': float(combined['s1'].corr(combined['s2'])),
        'mean_s1': float(combined['s1'].mean()),
        'mean_s2': float(combined['s2'].mean())
    }

def investigate_utilization_gap(df):
    """
    Investigate the 1973 utilization gap and its impact on calculations.
    """
    u_series = df['u']

    # Find the gap
    missing_years = df[u_series.isna()].index.tolist()

    # Examine surrounding years
    gap_analysis = {
        'missing_years': missing_years,
        'u_before_gap': {},
        'u_after_gap': {},
        'interpolation_candidates': {}
    }

    for year in missing_years:
        # Get values before and after
        before_years = df[df.index < year]['u'].dropna()
        after_years = df[df.index > year]['u'].dropna()

        if len(before_years) > 0:
            gap_analysis['u_before_gap'][year] = {
                'last_value': float(before_years.iloc[-1]),
                'last_year': int(before_years.index[-1])
            }

        if len(after_years) > 0:
            gap_analysis['u_after_gap'][year] = {
                'next_value': float(after_years.iloc[0]),
                'next_year': int(after_years.index[0])
            }

        # Calculate potential interpolated value
        if len(before_years) > 0 and len(after_years) > 0:
            linear_interp = (before_years.iloc[-1] + after_years.iloc[0]) / 2
            gap_analysis['interpolation_candidates'][year] = float(linear_interp)

    return gap_analysis

def analyze_period_differences(df, results):
    """
    Analyze if profit rate definitions work differently in different periods.
    """
    period_analysis = {}

    # Part 1: 1958-1973 (using KK)
    part1_mask = (df.index >= 1958) & (df.index <= 1973)
    part1_df = df[part1_mask]

    # Part 2: 1974-1989 (using K)
    part2_mask = (df.index >= 1974) & (df.index <= 1989)
    part2_df = df[part2_mask]

    for period_df, period_name in [(part1_df, 'part1_1958_1973'), (part2_df, 'part2_1974_1989')]:
        if len(period_df) > 0:
            period_analysis[period_name] = {}
            for alt_name, alt_data in results.items():
                r_pub = period_df['r\'']
                r_alt = alt_data['data'].loc[period_df.index]
                period_analysis[period_name][alt_name] = compare_series(r_pub, r_alt)

    return period_analysis

def examine_economic_relationships(df):
    """
    Examine broader economic relationships that might inform the profit rate definition.
    """
    relationships = {}

    # Create K_unified again for this function
    K_unified = pd.Series(index=df.index, dtype=float)
    if 'KK' in df.columns:
        K_unified = K_unified.fillna(df['KK'])
    if 'K' in df.columns:
        K_unified = K_unified.fillna(df['K'])

    # Investment rate vs profit rate
    I_series = df['I!'] if 'I!' in df.columns else df.get('I', pd.Series())
    if not I_series.empty and not df['r\''].empty:
        investment_rate = I_series / K_unified
        relationships['investment_vs_profit'] = compare_series(df['r\''], investment_rate)

    # Growth rate relationships
    gK = df.get('gK', pd.Series())
    if not gK.empty and not df['r\''].empty:
        relationships['growth_vs_profit'] = compare_series(df['r\''], gK)

    # Surplus relationships
    if 'SP' in df.columns and 'S' in df.columns:
        sp_s_ratio = df['SP'] / df['S']
        relationships['SP_vs_S_ratio'] = {
            'mean_ratio': float(sp_s_ratio.mean()),
            'std_ratio': float(sp_s_ratio.std()),
            'description': 'SP/S ratio - should be close to 1 if SP≈S'
        }

    return relationships

def generate_report(results, gap_analysis, period_analysis, economic_relationships):
    """Generate a comprehensive markdown report."""

    report = f"""# Profit Rate Definition Investigation

## Executive Summary

This investigation examines why the published profit rate r' in Shaikh & Tonak (1994) Table 5.4
does not match the textbook Marxian identity r = s'/(1+c'), and identifies which alternative
definition best explains the observed values.

## Key Findings

### Best Matching Definition
"""

    # Find the best matching alternative
    best_match = None
    best_mae = float('inf')

    for alt_name, alt_data in results.items():
        if alt_data['vs_published']['observations'] > 0:
            mae = alt_data['vs_published']['mae']
            if mae < best_mae:
                best_mae = mae
                best_match = alt_name

    if best_match:
        best_data = results[best_match]
        report += f"""
**{best_data['formula']}**
- Description: {best_data['description']}
- MAE vs published r': {best_data['vs_published']['mae']:.6f}
- Max absolute error: {best_data['vs_published']['max_abs_err']:.6f}
- Correlation: {best_data['vs_published']['correlation']:.4f}
- Observations: {best_data['vs_published']['observations']}
"""

    report += f"""
## Alternative Definitions Tested

| Formula | Description | MAE | Max Error | Correlation | Obs |
|---------|-------------|-----|-----------|-------------|-----|
"""

    for alt_name, alt_data in results.items():
        vs_pub = alt_data['vs_published']
        if vs_pub['observations'] > 0:
            report += f"| {alt_data['formula']} | {alt_data['description']} | {vs_pub['mae']:.6f} | {vs_pub['max_abs_err']:.6f} | {vs_pub['correlation']:.4f} | {vs_pub['observations']} |\n"

    report += f"""
## Utilization Gap Analysis

Missing utilization data: {gap_analysis['missing_years']}

"""

    for year in gap_analysis['missing_years']:
        if year in gap_analysis['interpolation_candidates']:
            report += f"- {year}: Could interpolate as {gap_analysis['interpolation_candidates'][year]:.3f}\n"

    report += f"""
## Period-Specific Analysis

### Part 1 (1958-1973) vs Part 2 (1974-1989)

The profit rate definition may work differently across periods due to:
- Different capital stock measures (KK vs K)
- Methodological changes in national accounts
- Economic structural changes
"""

    # Add period comparison if available
    if 'part1_1958_1973' in period_analysis and 'part2_1974_1989' in period_analysis:
        report += f"""
| Definition | Part 1 MAE | Part 2 MAE | Part 1 Corr | Part 2 Corr |
|------------|-------------|-------------|--------------|-------------|
"""
        for alt_name in results.keys():
            if alt_name in period_analysis['part1_1958_1973'] and alt_name in period_analysis['part2_1974_1989']:
                p1 = period_analysis['part1_1958_1973'][alt_name]
                p2 = period_analysis['part2_1974_1989'][alt_name]
                if p1['observations'] > 0 and p2['observations'] > 0:
                    report += f"| {results[alt_name]['formula']} | {p1['mae']:.6f} | {p2['mae']:.6f} | {p1['correlation']:.4f} | {p2['correlation']:.4f} |\n"

    report += f"""
## Recommendations for Perfect Replication

1. **Use the best-matching definition** ({results[best_match]['formula'] if best_match else 'TBD'}) for calculating profit rates from raw data
2. **Investigate the 1973 utilization gap** - consider whether to interpolate or leave as missing
3. **Validate period consistency** - ensure the same definition works across both periods
4. **Cross-reference with book text** - confirm theoretical justification for the empirical definition

## Technical Notes

- All calculations preserve authentic book values exactly
- Missing values are not interpolated in this analysis
- Error metrics calculated only on years with complete data
- Results suggest specific definitional conventions in Shaikh & Tonak's methodology
"""

    return report

def main():
    """Main investigation workflow."""

    # Load data
    print("Loading authentic data...")
    # Use the final authentic table which has everything combined
    final_path = BASE_DIR / "table_5_4_authentic.csv"
    df = pd.read_csv(final_path)
    df = df.set_index('year')
    print(f"Loaded data shape: {df.shape}")
    print(f"Columns: {list(df.columns[:10])}...")  # Show first 10 columns

    print("Testing profit rate alternatives...")
    results = calculate_profit_rate_alternatives(df)

    print("Investigating utilization gap...")
    gap_analysis = investigate_utilization_gap(df)

    print("Analyzing period differences...")
    period_analysis = analyze_period_differences(df, results)

    print("Examining economic relationships...")
    economic_relationships = examine_economic_relationships(df)

    # Prepare output data
    output_data = {
        'profit_rate_alternatives': {
            alt_name: {
                'formula': alt_data['formula'],
                'description': alt_data['description'],
                'vs_published': alt_data['vs_published']
            }
            for alt_name, alt_data in results.items()
        },
        'utilization_gap_analysis': gap_analysis,
        'period_analysis': period_analysis,
        'economic_relationships': economic_relationships,
        'methodology_notes': [
            'No interpolation performed',
            'Authentic book values preserved exactly',
            'Error metrics calculated on complete observations only'
        ]
    }

    # Save JSON results
    print(f"Saving results to {OUT_PATH}...")
    with open(OUT_PATH, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    # Generate and save report
    print(f"Generating report to {REPORT_PATH}...")
    report = generate_report(results, gap_analysis, period_analysis, economic_relationships)
    with open(REPORT_PATH, 'w') as f:
        f.write(report)

    print("Investigation complete!")
    print(f"Results: {OUT_PATH}")
    print(f"Report: {REPORT_PATH}")

if __name__ == "__main__":
    main()