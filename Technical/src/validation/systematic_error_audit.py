#!/usr/bin/env python3
"""
Systematic Error Audit
======================

This script conducts a comprehensive audit to determine whether the remaining
"small" differences are truly just rounding errors, or if they mask systematic
methodological errors that we haven't identified.

Key Questions to Answer:
1. Are error patterns truly random (consistent with rounding)?
2. Do errors correlate with economic cycles, time periods, or variable magnitudes?
3. Are there systematic biases that suggest missing methodology components?
4. Could there be alternative data sources or calculation methods?
5. Are we missing deflation, depreciation, or other adjustments?

This is a critical validation step to ensure we haven't achieved "false precision"
while missing fundamental methodology issues.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import jarque_bera, shapiro
import seaborn as sns

# Configuration
BASE_DIR = Path("src/analysis/replication/output")
ULTRA_PATH = BASE_DIR / "table_5_4_ultra_precise_replication.csv"
AUTHENTIC_PATH = BASE_DIR / "table_5_4_authentic.csv"
AUDIT_PATH = BASE_DIR / "systematic_error_audit.json"
REPORT_PATH = BASE_DIR / "SYSTEMATIC_ERROR_AUDIT.md"

class SystematicErrorAuditor:
    """
    Conducts comprehensive audit for systematic vs random errors.
    """

    def __init__(self):
        self.audit_findings = {}
        self.red_flags = []
        self.validation_passed = True

    def load_data(self):
        """Load ultra-precise and authentic datasets."""
        print("Loading datasets for systematic error audit...")

        ultra_df = pd.read_csv(ULTRA_PATH, index_col='year')
        authentic_df = pd.read_csv(AUTHENTIC_PATH, index_col='year')

        print(f"Ultra-precise data: {len(ultra_df)} years")
        print(f"Authentic baseline: {len(authentic_df)} years")

        return ultra_df, authentic_df

    def analyze_error_patterns(self, ultra_df, authentic_df):
        """Analyze error patterns for signs of systematic bias."""
        print("Analyzing error patterns...")

        analysis = {}

        # Focus on profit rate - our "best" result
        r_calc = ultra_df['r_ultra_precise']
        r_pub = authentic_df['r\'']
        errors = r_calc - r_pub

        # 1. Test for randomness
        analysis['randomness_tests'] = {}

        # Runs test for randomness
        def runs_test(errors):
            """Test if errors are random or show patterns."""
            median_error = errors.median()
            runs, n1, n2 = 0, 0, 0

            # Convert to above/below median
            above_below = errors > median_error

            # Count runs
            for i in range(len(above_below)):
                if above_below.iloc[i]:
                    n1 += 1
                else:
                    n2 += 1

                if i > 0 and above_below.iloc[i] != above_below.iloc[i-1]:
                    runs += 1

            runs += 1  # Add final run

            # Calculate expected runs and standard deviation
            expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
            variance = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2)**2 * (n1 + n2 - 1))

            if variance > 0:
                z_score = (runs - expected_runs) / np.sqrt(variance)
                return runs, expected_runs, z_score, abs(z_score) < 1.96  # 95% confidence
            else:
                return runs, expected_runs, 0, True

        if len(errors.dropna()) > 5:
            runs, expected_runs, z_score, is_random = runs_test(errors.dropna())
            analysis['randomness_tests']['runs_test'] = {
                'runs': runs,
                'expected_runs': expected_runs,
                'z_score': z_score,
                'is_random': is_random,
                'interpretation': 'Errors appear random' if is_random else 'Errors show systematic pattern'
            }

        # 2. Test for normality (random errors should be normally distributed)
        if len(errors.dropna()) > 7:
            try:
                shapiro_stat, shapiro_p = shapiro(errors.dropna())
                analysis['randomness_tests']['normality_test'] = {
                    'shapiro_stat': float(shapiro_stat),
                    'shapiro_p': float(shapiro_p),
                    'is_normal': shapiro_p > 0.05,
                    'interpretation': 'Errors normally distributed' if shapiro_p > 0.05 else 'Errors not normally distributed'
                }
            except Exception as e:
                analysis['randomness_tests']['normality_test'] = {'error': str(e)}

        # 3. Autocorrelation test (systematic errors often show correlation)
        if len(errors.dropna()) > 3:
            error_series = errors.dropna()
            if len(error_series) > 1:
                autocorr_1 = error_series.autocorr(lag=1)
                analysis['randomness_tests']['autocorrelation'] = {
                    'lag_1_autocorr': float(autocorr_1) if not pd.isna(autocorr_1) else 0,
                    'is_independent': abs(autocorr_1) < 0.3 if not pd.isna(autocorr_1) else True,
                    'interpretation': 'Errors independent' if abs(autocorr_1) < 0.3 or pd.isna(autocorr_1) else 'Errors show autocorrelation'
                }

        self.audit_findings['error_patterns'] = analysis
        return analysis

    def test_magnitude_dependence(self, ultra_df, authentic_df):
        """Test if errors depend on magnitude of values."""
        print("Testing magnitude dependence...")

        analysis = {}

        # Test profit rate errors vs magnitude
        r_calc = ultra_df['r_ultra_precise']
        r_pub = authentic_df['r\'']
        errors = r_calc - r_pub
        abs_errors = errors.abs()

        # Correlate absolute errors with value magnitude
        if len(r_pub.dropna()) > 5:
            combined = pd.DataFrame({
                'magnitude': r_pub,
                'abs_error': abs_errors
            }).dropna()

            if len(combined) > 3:
                corr_coef = combined['magnitude'].corr(combined['abs_error'])
                analysis['magnitude_correlation'] = {
                    'correlation': float(corr_coef) if not pd.isna(corr_coef) else 0,
                    'is_magnitude_dependent': abs(corr_coef) > 0.5 if not pd.isna(corr_coef) else False,
                    'interpretation': 'Errors depend on value magnitude' if abs(corr_coef) > 0.5 and not pd.isna(corr_coef) else 'Errors independent of magnitude'
                }

        # Test if errors are proportional (percentage errors constant)
        relative_errors = (errors / r_pub * 100).dropna()
        if len(relative_errors) > 2:
            analysis['relative_error_analysis'] = {
                'mean_relative_error': float(relative_errors.mean()),
                'std_relative_error': float(relative_errors.std()),
                'cv_relative_error': float(relative_errors.std() / abs(relative_errors.mean())) if relative_errors.mean() != 0 else float('inf'),
                'is_proportional': relative_errors.std() / abs(relative_errors.mean()) < 0.5 if relative_errors.mean() != 0 else False
            }

        self.audit_findings['magnitude_dependence'] = analysis
        return analysis

    def analyze_temporal_patterns(self, ultra_df, authentic_df):
        """Analyze temporal patterns in errors."""
        print("Analyzing temporal patterns...")

        analysis = {}

        # Profit rate temporal analysis
        r_calc = ultra_df['r_ultra_precise']
        r_pub = authentic_df['r\'']
        errors = r_calc - r_pub

        # Test for trends over time
        if len(errors.dropna()) > 3:
            years = errors.dropna().index
            error_vals = errors.dropna().values

            # Linear trend
            if len(years) > 2:
                slope, intercept, r_value, p_value, std_err = stats.linregress(years, error_vals)
                analysis['temporal_trend'] = {
                    'slope': float(slope),
                    'r_squared': float(r_value**2),
                    'p_value': float(p_value),
                    'significant_trend': p_value < 0.05,
                    'interpretation': f'{"Significant" if p_value < 0.05 else "No significant"} temporal trend in errors'
                }

        # Test for structural breaks (Part 1 vs Part 2)
        part1_errors = errors[(errors.index >= 1958) & (errors.index <= 1973)].dropna()
        part2_errors = errors[(errors.index >= 1974) & (errors.index <= 1989)].dropna()

        if len(part1_errors) > 2 and len(part2_errors) > 2:
            # Two-sample t-test
            t_stat, p_val = stats.ttest_ind(part1_errors, part2_errors)
            analysis['structural_break'] = {
                'part1_mean_error': float(part1_errors.mean()),
                'part2_mean_error': float(part2_errors.mean()),
                't_statistic': float(t_stat),
                'p_value': float(p_val),
                'significant_break': p_val < 0.05,
                'interpretation': f'{"Significant" if p_val < 0.05 else "No significant"} difference between periods'
            }

        # Test for cyclical patterns
        if len(errors.dropna()) > 10:
            # Simple test: correlation with lagged errors
            error_series = errors.dropna()
            lags_to_test = [2, 3, 5]  # Business cycle type lags
            cyclical_correlations = {}

            for lag in lags_to_test:
                if len(error_series) > lag:
                    lagged_corr = error_series.corr(error_series.shift(lag))
                    cyclical_correlations[f'lag_{lag}'] = float(lagged_corr) if not pd.isna(lagged_corr) else 0

            analysis['cyclical_patterns'] = {
                'lagged_correlations': cyclical_correlations,
                'max_cyclical_corr': max([abs(v) for v in cyclical_correlations.values()]) if cyclical_correlations else 0,
                'shows_cycles': max([abs(v) for v in cyclical_correlations.values()]) > 0.4 if cyclical_correlations else False
            }

        self.audit_findings['temporal_patterns'] = analysis
        return analysis

    def cross_validate_methodology(self, ultra_df, authentic_df):
        """Cross-validate our methodology using alternative approaches."""
        print("Cross-validating methodology...")

        analysis = {}

        # Test alternative profit rate calculations
        SP = authentic_df['SP']
        S = authentic_df['S']
        K_unified = ultra_df['K_unified']
        u_corrected = ultra_df['u_corrected']
        r_pub = authentic_df['r\'']

        # Method 1: Using S instead of SP (where available)
        s_years = authentic_df.loc[authentic_df.index <= 1973]  # S is available in Part 1
        if 'S' in s_years.columns and not s_years['S'].empty:
            S_available = s_years['S']
            K_s_years = K_unified.loc[S_available.index]
            u_s_years = u_corrected.loc[S_available.index]

            r_from_S = S_available / (K_s_years * u_s_years)
            r_pub_s_years = r_pub.loc[S_available.index]

            common_idx = r_from_S.dropna().index.intersection(r_pub_s_years.dropna().index)
            if len(common_idx) > 2:
                mae_from_S = np.mean(np.abs(r_from_S.loc[common_idx] - r_pub_s_years.loc[common_idx]))
                analysis['alternative_S_method'] = {
                    'mae_using_S': float(mae_from_S),
                    'mae_using_SP': float(np.mean(np.abs(ultra_df.loc[common_idx, 'r_ultra_precise'] - r_pub_s_years.loc[common_idx]))),
                    'S_method_better': mae_from_S < np.mean(np.abs(ultra_df.loc[common_idx, 'r_ultra_precise'] - r_pub_s_years.loc[common_idx])),
                    'observations': len(common_idx)
                }

        # Method 2: Test if raw calculation (no rounding) has different error pattern
        r_raw = SP / (K_unified * u_corrected)
        r_raw_errors = r_raw - r_pub
        r_rounded_errors = ultra_df['r_ultra_precise'] - r_pub

        common_idx = r_raw_errors.dropna().index.intersection(r_rounded_errors.dropna().index)
        if len(common_idx) > 5:
            # Compare error distributions
            raw_error_std = r_raw_errors.loc[common_idx].std()
            rounded_error_std = r_rounded_errors.loc[common_idx].std()

            analysis['rounding_effect'] = {
                'raw_mae': float(np.mean(np.abs(r_raw_errors.loc[common_idx]))),
                'rounded_mae': float(np.mean(np.abs(r_rounded_errors.loc[common_idx]))),
                'raw_std': float(raw_error_std),
                'rounded_std': float(rounded_error_std),
                'rounding_improves': float(np.mean(np.abs(r_rounded_errors.loc[common_idx]))) < float(np.mean(np.abs(r_raw_errors.loc[common_idx]))),
                'interpretation': 'Rounding reduces errors' if float(np.mean(np.abs(r_rounded_errors.loc[common_idx]))) < float(np.mean(np.abs(r_raw_errors.loc[common_idx]))) else 'Raw calculation is better'
            }

        self.audit_findings['methodology_validation'] = analysis
        return analysis

    def identify_red_flags(self):
        """Identify red flags that suggest systematic errors rather than rounding."""
        print("Identifying red flags...")

        red_flags = []

        # Check error patterns
        if 'error_patterns' in self.audit_findings:
            patterns = self.audit_findings['error_patterns']

            # Non-random errors are a red flag
            if 'randomness_tests' in patterns:
                if 'runs_test' in patterns['randomness_tests']:
                    if not patterns['randomness_tests']['runs_test']['is_random']:
                        red_flags.append("MAJOR: Errors show systematic pattern (runs test)")

                if 'autocorrelation' in patterns['randomness_tests']:
                    if not patterns['randomness_tests']['autocorrelation']['is_independent']:
                        red_flags.append("MINOR: Errors show autocorrelation")

                if 'normality_test' in patterns['randomness_tests']:
                    if not patterns['randomness_tests']['normality_test']['is_normal']:
                        red_flags.append("MINOR: Errors not normally distributed")

        # Check magnitude dependence
        if 'magnitude_dependence' in self.audit_findings:
            mag_dep = self.audit_findings['magnitude_dependence']

            if 'magnitude_correlation' in mag_dep:
                if mag_dep['magnitude_correlation']['is_magnitude_dependent']:
                    red_flags.append("MAJOR: Errors depend on value magnitude (suggests wrong formula)")

        # Check temporal patterns
        if 'temporal_patterns' in self.audit_findings:
            temporal = self.audit_findings['temporal_patterns']

            if 'temporal_trend' in temporal:
                if temporal['temporal_trend']['significant_trend']:
                    red_flags.append("MODERATE: Significant temporal trend in errors")

            if 'structural_break' in temporal:
                if temporal['structural_break']['significant_break']:
                    red_flags.append("MODERATE: Significant structural break between periods")

            if 'cyclical_patterns' in temporal:
                if temporal['cyclical_patterns']['shows_cycles']:
                    red_flags.append("MINOR: Cyclical patterns in errors")

        # Check methodology validation
        if 'methodology_validation' in self.audit_findings:
            method_val = self.audit_findings['methodology_validation']

            if 'alternative_S_method' in method_val:
                if method_val['alternative_S_method']['S_method_better']:
                    red_flags.append("MAJOR: Alternative method (using S) performs significantly better")

            if 'rounding_effect' in method_val:
                if not method_val['rounding_effect']['rounding_improves']:
                    red_flags.append("MODERATE: Raw calculation performs better than rounded (questions rounding assumption)")

        self.red_flags = red_flags
        return red_flags

    def generate_audit_report(self):
        """Generate comprehensive audit report."""

        report = f"""# Systematic Error Audit Report

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This audit investigates whether the remaining small differences in our replication
are truly just rounding errors, or if they mask systematic methodological issues.

## Critical Question: Are These Really Just "Rounding Errors"?

"""

        # Red flags section
        if self.red_flags:
            report += f"""## RED FLAGS IDENTIFIED

The following issues suggest systematic errors rather than simple rounding:

"""
            for i, flag in enumerate(self.red_flags, 1):
                severity = flag.split(':')[0]
                description = flag.split(':', 1)[1].strip()
                report += f"{i}. **{severity}**: {description}\n"

            if any('MAJOR' in flag for flag in self.red_flags):
                report += f"""
### CRITICAL FINDING
Major red flags detected. The small differences may NOT be just rounding errors.
Further investigation required before claiming "perfect replication."

"""
                self.validation_passed = False

        else:
            report += f"""## NO MAJOR RED FLAGS

The audit found no major systematic patterns that would suggest fundamental
methodological errors. The small differences appear consistent with rounding conventions.

"""

        # Detailed findings
        report += f"""## Detailed Audit Findings

### Error Pattern Analysis
"""

        if 'error_patterns' in self.audit_findings:
            patterns = self.audit_findings['error_patterns']

            if 'randomness_tests' in patterns:
                report += f"**Randomness Tests:**\n"
                for test_name, test_result in patterns['randomness_tests'].items():
                    if isinstance(test_result, dict) and 'interpretation' in test_result:
                        report += f"- {test_name}: {test_result['interpretation']}\n"

        report += f"""
### Magnitude Dependence Analysis
"""
        if 'magnitude_dependence' in self.audit_findings:
            mag_dep = self.audit_findings['magnitude_dependence']
            if 'magnitude_correlation' in mag_dep:
                corr_result = mag_dep['magnitude_correlation']
                report += f"- Correlation with magnitude: {corr_result['correlation']:.4f}\n"
                report += f"- Interpretation: {corr_result['interpretation']}\n"

        report += f"""
### Temporal Pattern Analysis
"""
        if 'temporal_patterns' in self.audit_findings:
            temporal = self.audit_findings['temporal_patterns']
            for analysis_name, analysis_result in temporal.items():
                if isinstance(analysis_result, dict) and 'interpretation' in analysis_result:
                    report += f"- {analysis_name}: {analysis_result['interpretation']}\n"

        # Final verdict
        report += f"""
## Final Audit Verdict

"""
        if self.validation_passed:
            report += f"""**VALIDATION PASSED**

The systematic error audit confirms that the remaining small differences are
consistent with rounding conventions and measurement precision. No evidence
of fundamental methodological errors was found.

**Conclusion:** The replication can be considered methodologically sound with
differences attributable to computational precision rather than systematic errors.
"""
        else:
            report += f"""**VALIDATION FAILED**

The systematic error audit identified patterns that suggest the remaining
differences may not be simple rounding errors. Further investigation is required.

**Recommendation:** Do not claim "perfect replication" until red flags are resolved.
"""

        report += f"""
## Technical Notes

- All tests conducted on profit rate calculations (primary variable)
- Statistical tests applied with appropriate confidence levels
- Cross-validation performed using alternative calculation methods
- Temporal and magnitude dependence tested systematically

This audit ensures we distinguish between acceptable measurement precision
and unacceptable systematic errors.
"""

        return report

    def run_systematic_audit(self):
        """Execute the complete systematic error audit."""

        print("=" * 60)
        print("SYSTEMATIC ERROR AUDIT")
        print("=" * 60)
        print("Verifying: Are small differences truly just rounding errors?")
        print("=" * 60)

        # Load data
        ultra_df, authentic_df = self.load_data()

        # Run audit analyses
        self.analyze_error_patterns(ultra_df, authentic_df)
        self.test_magnitude_dependence(ultra_df, authentic_df)
        self.analyze_temporal_patterns(ultra_df, authentic_df)
        self.cross_validate_methodology(ultra_df, authentic_df)

        # Identify red flags
        red_flags = self.identify_red_flags()

        # Save results
        print(f"Saving audit results to {AUDIT_PATH}...")
        with open(AUDIT_PATH, 'w') as f:
            json.dump({
                'audit_findings': self.audit_findings,
                'red_flags': self.red_flags,
                'validation_passed': self.validation_passed,
                'timestamp': pd.Timestamp.now().isoformat()
            }, f, indent=2, default=str)

        # Generate report
        print(f"Generating audit report to {REPORT_PATH}...")
        report = self.generate_audit_report()
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)

        print("=" * 60)
        print("SYSTEMATIC ERROR AUDIT COMPLETE")
        print("=" * 60)

        # Print verdict
        if self.validation_passed:
            print("AUDIT PASSED: Differences consistent with rounding errors")
        else:
            print("AUDIT FAILED: Systematic patterns detected")

        print(f"\nRed flags identified: {len(red_flags)}")
        for flag in red_flags[:3]:  # Show top 3
            print(f"- {flag}")

        return self.audit_findings, self.validation_passed

def main():
    """Main execution."""
    auditor = SystematicErrorAuditor()
    findings, validation_passed = auditor.run_systematic_audit()

    return findings, validation_passed

if __name__ == "__main__":
    main()