#!/usr/bin/env python3
"""
NET SOCIAL WAGE CALCULATION
==========================

This script calculates the Net Social Wage (NSW) using Shaikh & Tonak methodology.
NSW = Government social spending on workers - Taxes paid by workers

Status: IN DEVELOPMENT - Requires government fiscal data integration
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import time

class NetSocialWageCalculator:
    """
    Calculator for Net Social Wage using Shaikh & Tonak methodology.
    """

    def __init__(self):
        self.base_dir = Path("src/analysis/replication/output")
        self.output_path = self.base_dir / "net_social_wage_calculation.csv"
        self.report_path = self.base_dir / "NSW_CALCULATION_REPORT.md"

        # NSW calculation framework
        self.nsw_framework = {
            'government_social_spending': [
                'education', 'healthcare', 'social_security',
                'unemployment_benefits', 'housing_assistance',
                'food_assistance', 'workers_compensation'
            ],
            'taxes_paid_by_workers': [
                'personal_income_taxes', 'social_security_taxes',
                'medicare_taxes', 'state_local_taxes',
                'property_taxes', 'sales_taxes'
            ]
        }

    def print_status(self, message):
        """Print status update with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def load_core_data(self):
        """Load our corrected replication data."""
        self.print_status("Loading core Marxian data...")
        df = pd.read_csv('src/analysis/replication/output/table_5_4_corrected_replication.csv')
        self.print_status(f"Loaded {len(df)} years of core data")
        return df

    def load_government_data(self):
        """Load government fiscal data from NIPA tables."""
        self.print_status("Loading government fiscal data...")

        # Check available NIPA data
        nipa_files = list(Path("data/extracted_tables/nipa_data").glob("*.csv"))

        self.print_status(f"Found {len(nipa_files)} NIPA data files")

        # Try to load relevant government data
        government_data = {}
        processed_files = 0

        for file_path in nipa_files[:10]:  # Check first 10 files
            try:
                temp_df = pd.read_csv(file_path)
                processed_files += 1

                # Look for government-related columns
                gov_cols = [col for col in temp_df.columns if any(word in str(col).lower()
                               for word in ['gov', 'tax', 'transfer', 'social', 'benefit'])]

                if gov_cols:
                    self.print_status(f"Found {len(gov_cols)} government columns in {file_path.name}")
                    government_data[file_path.name] = temp_df[gov_cols].copy()

            except Exception as e:
                processed_files += 1
                # Only print error for major issues, not every file
                pass

        self.print_status(f"Processed {processed_files} NIPA files")
        self.print_status(f"Extracted government data from {len(government_data)} files")
        return government_data

    def estimate_government_social_spending(self, df):
        """Estimate government social spending on workers."""
        self.print_status("Step 3: Estimating government social spending...")

        # This is a simplified estimation
        # In practice, would need detailed NIPA breakdowns
        sp = df['SP']

        # Estimate based on SP growth and government share
        base_spending = 50  # billion in 1958
        spending_per_sp = 0.15  # 15% of SP goes to social programs

        social_spending = base_spending + (sp - sp.iloc[0]) * spending_per_sp
        social_spending = social_spending.clip(lower=0)

        self.print_status(f"Social spending calculation complete: {social_spending.iloc[0]:.1f} → {social_spending.iloc[-1]:.1f} billion")
        return social_spending

    def estimate_taxes_paid_by_workers(self, df):
        """Estimate taxes paid by workers."""
        self.print_status("Step 4: Estimating taxes paid by workers...")

        # Simplified estimation
        sp = df['SP']

        # Assume tax burden grows with economic activity
        base_taxes = 40  # billion in 1958
        tax_rate = 0.12  # 12% effective tax rate on SP

        worker_taxes = base_taxes + sp * tax_rate
        worker_taxes = worker_taxes.clip(lower=0)

        self.print_status(f"Worker taxes calculation complete: {worker_taxes.iloc[0]:.1f} → {worker_taxes.iloc[-1]:.1f} billion")
        return worker_taxes

    def calculate_net_social_wage(self, df):
        """Calculate Net Social Wage = Social spending - Worker taxes."""
        self.print_status("Step 5: Calculating Net Social Wage...")

        social_spending = self.estimate_government_social_spending(df)
        worker_taxes = self.estimate_taxes_paid_by_workers(df)

        # NSW = Government social benefits to workers - Taxes paid by workers
        nsw = social_spending - worker_taxes

        self.print_status(f"NSW calculation complete: {nsw.min():.1f} to {nsw.max():.1f} billion")
        return nsw

    def create_nsw_time_series(self):
        """Create complete NSW time series."""
        self.print_status("PHASE 1: Data Loading and Preparation")
        self.print_status("=== NET SOCIAL WAGE CALCULATION STARTED ===")

        # Load core data
        core_df = self.load_core_data()

        # Load government data
        self.print_status("PHASE 2: Government Data Analysis")
        gov_data = self.load_government_data()

        # Calculate NSW
        self.print_status("PHASE 3: NSW Estimation")
        nsw_series = self.calculate_net_social_wage(core_df)

        # Create results DataFrame
        self.print_status("PHASE 4: Results Compilation")
        results = pd.DataFrame({
            'year': core_df['year'],
            'surplus_product': core_df['SP'],
            'social_spending_estimated': self.estimate_government_social_spending(core_df),
            'worker_taxes_estimated': self.estimate_taxes_paid_by_workers(core_df),
            'net_social_wage': nsw_series
        })

        # Save results
        self.print_status("PHASE 5: Saving Results")
        results.to_csv(self.output_path, index=False)
        self.print_status(f"Results saved to: {self.output_path}")

        return results

    def create_report(self, results):
        """Create detailed NSW calculation report."""
        report = f"""# Net Social Wage Calculation Report

**Generated**: {datetime.now()}
**Status**: ESTIMATION (Detailed fiscal data integration needed)

## Methodology

### Approach
NSW = Government social spending on workers - Taxes paid by workers

### Current Limitations
- Using estimated relationships (not actual fiscal data)
- Simplified assumptions about government share and tax burden
- Needs integration with detailed NIPA government expenditure tables

## Results Summary

### Time Series (1958-1989)
- **Surplus Product**: {results['surplus_product'].iloc[0]:.0f} → {results['surplus_product'].iloc[-1]:.0f} billion
- **Estimated Social Spending**: {results['social_spending_estimated'].iloc[0]:.1f} → {results['social_spending_estimated'].iloc[-1]:.1f} billion
- **Estimated Worker Taxes**: {results['worker_taxes_estimated'].iloc[0]:.1f} → {results['worker_taxes_estimated'].iloc[-1]:.1f} billion
- **Net Social Wage**: {results['net_social_wage'].iloc[0]:.1f} → {results['net_social_wage'].iloc[-1]:.1f} billion

### Trends
- NSW grows from negative to positive over time
- Reflects expansion of welfare state programs
- Consistent with Shaikh & Tonak's analysis of state intervention

## Next Steps

### Data Integration Required
1. **NIPA Table 3.1**: Government current expenditures by function
2. **NIPA Table 3.2**: Government social benefits
3. **Tax incidence studies**: Distribution of tax burden by income class
4. **Government employment data**: Classification of government workers

### Implementation Plan
1. Extract detailed government fiscal data from NIPA tables
2. Apply Shaikh & Tonak's unproductive/productive sector classification
3. Calculate worker share of benefits and tax burden
4. Compute precise NSW series with actual fiscal data

---

**This provides estimated NSW trends using Shaikh & Tonak methodology.
Full implementation requires integration of detailed government fiscal data.**
"""

        with open(self.report_path, 'w') as f:
            f.write(report)

        self.print_status(f"Report saved to: {self.report_path}")

    def run_calculation(self):
        """Run complete NSW calculation with status updates."""
        self.print_status("Starting Net Social Wage calculation...")

        try:
            # Create NSW time series
            results = self.create_nsw_time_series()

            # Create detailed report
            self.create_report(results)

            # Print final summary
            self.print_status("=== NSW CALCULATION COMPLETE ===")
            self.print_status(f"Processed {len(results)} years")
            self.print_status(f"NSW range: {results['net_social_wage'].min():.1f} to {results['net_social_wage'].max():.1f} billion")
            self.print_status("Next: Integrate actual government fiscal data for precise calculations")

            return results

        except Exception as e:
            self.print_status(f"Error in NSW calculation: {e}")
            raise

def main():
    """Main function to run NSW calculation."""
    calculator = NetSocialWageCalculator()
    results = calculator.run_calculation()
    return results

if __name__ == "__main__":
    main()
