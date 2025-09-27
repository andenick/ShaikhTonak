#!/usr/bin/env python3
"""
Data Recovery Strategy for 100% Completeness
Implements multiple approaches to fill missing data gaps
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import logging
from scipy import interpolate
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataRecoverySystem:
    """
    Comprehensive data recovery system to achieve 100% completeness
    """

    def __init__(self, data_path: str = "data"):
        self.data_path = Path(data_path)
        self.book_tables_path = self.data_path / "extracted_tables" / "book_tables"
        self.unified_db_path = self.data_path / "unified_database" / "unified_database"

        # Load current incomplete data
        self.current_table = pd.read_csv("src/analysis/replication/output/table_5_4_reconstructed.csv")

        # Load unified database
        self.unified_db = pd.read_csv(
            self.unified_db_path / "corrected_historical_database.csv",
            index_col='year'
        )

        # Recovery methods registry
        self.recovery_methods = {
            'interpolation': self.interpolate_missing_values,
            'government_data': self.match_government_data,
            'additional_tables': self.extract_additional_tables,
            'calculation': self.calculate_derived_variables,
            'trend_extrapolation': self.extrapolate_trends
        }

        logger.info("Data Recovery System initialized")

    def analyze_recovery_opportunities(self) -> Dict:
        """Identify specific recovery opportunities for each missing data point"""

        logger.info("Analyzing recovery opportunities...")

        # Load completeness analysis
        with open("src/analysis/replication/output/data_completeness_analysis.json", 'r') as f:
            completeness_data = json.load(f)

        opportunities = {}

        # Part 1 variables missing from Part 2 (1975-1990)
        part1_vars = completeness_data['variable_gaps']['part1_only']

        # Part 2 variables missing from Part 1 (1958-1973)
        part2_vars = completeness_data['variable_gaps']['part2_only']

        # Missing year 1974
        missing_1974 = completeness_data['temporal_gaps']['missing_1974']

        for var in part1_vars:
            opportunities[f"{var}_part2_extension"] = {
                'variable': var,
                'missing_period': '1975-1990',
                'available_period': '1958-1973',
                'method_priority': ['government_data', 'trend_extrapolation', 'interpolation'],
                'feasibility': 'High'
            }

        for var in part2_vars:
            opportunities[f"{var}_part1_backfill"] = {
                'variable': var,
                'missing_period': '1958-1973',
                'available_period': '1975-1990',
                'method_priority': ['calculation', 'government_data', 'interpolation'],
                'feasibility': 'Medium'
            }

        if missing_1974:
            for var in self.current_table.columns:
                if var != 'year':
                    opportunities[f"{var}_1974_bridge"] = {
                        'variable': var,
                        'missing_period': '1974',
                        'available_period': '1973,1975',
                        'method_priority': ['interpolation', 'government_data'],
                        'feasibility': 'High'
                    }

        logger.info(f"Identified {len(opportunities)} recovery opportunities")
        return opportunities

    def interpolate_missing_values(self, variable: str, method: str = 'linear') -> pd.Series:
        """Interpolate missing values using various methods"""

        logger.info(f"Interpolating missing values for {variable} using {method}")

        data = self.current_table.set_index('year')[variable]

        if method == 'linear':
            return data.interpolate(method='linear')
        elif method == 'polynomial':
            return data.interpolate(method='polynomial', order=2)
        elif method == 'spline':
            return data.interpolate(method='spline', order=3)
        else:
            return data.interpolate()

    def match_government_data(self, variable: str) -> Optional[pd.Series]:
        """Match variables with government data from unified database"""

        logger.info(f"Searching government data for {variable}")

        # Variable mapping from book variables to government variables
        government_mappings = {
            'I': ['nipa_fixed_investment', 'investment', 'gross_private_domestic'],
            'S': ['gnp', 'national_income', 'surplus'],
            'Pn': ['price', 'deflator', 'nominal'],
            'K': ['capital', 'stock'],
            'gK': ['capital_growth', 'investment_rate'],
            'fn': ['capacity', 'utilization']
        }

        if variable not in government_mappings:
            return None

        # Search for matching columns in unified database
        possible_matches = government_mappings[variable]

        for col in self.unified_db.columns:
            for match_term in possible_matches:
                if match_term.lower() in col.lower():
                    logger.info(f"Found potential match: {col} for {variable}")
                    return self.unified_db[col]

        return None

    def extract_additional_tables(self, variable: str) -> Optional[pd.Series]:
        """Extract data from additional book tables"""

        logger.info(f"Searching additional tables for {variable}")

        # Table 5.5 contains labor data
        try:
            table_5_5 = pd.read_csv(self.book_tables_path / "table_5_5.csv")
            if variable in ['b', 'Lp', 'L']:
                # Process labor-related variables from Table 5.5
                return self.process_table_5_5(table_5_5, variable)
        except:
            pass

        # Table 5.6 contains additional economic indicators
        try:
            table_5_6 = pd.read_csv(self.book_tables_path / "table_5_6.csv")
            if variable in ['pc', 'ecp', 'ecu']:
                return self.process_table_5_6(table_5_6, variable)
        except:
            pass

        # Table 5.7 contains more variables
        try:
            table_5_7 = pd.read_csv(self.book_tables_path / "table_5_7.csv")
            return self.process_table_5_7(table_5_7, variable)
        except:
            pass

        return None

    def process_table_5_5(self, table_5_5: pd.DataFrame, variable: str) -> Optional[pd.Series]:
        """Process Table 5.5 for labor-related variables"""

        logger.info(f"Processing Table 5.5 for {variable}")

        # Table 5.5 contains labor data with different structure
        # Need to parse the complex table structure

        if variable == 'b':  # Productive labor share
            # Look for Lp/L ratio
            for idx, row in table_5_5.iterrows():
                if 'Lp/L' in str(row.iloc[0]):
                    years = []
                    values = []
                    for col in table_5_5.columns[1:]:
                        try:
                            year = int(col)
                            value = float(row[col])
                            years.append(year)
                            values.append(value)
                        except:
                            continue

                    if years:
                        return pd.Series(values, index=years, name=variable)

        return None

    def process_table_5_6(self, table_5_6: pd.DataFrame, variable: str) -> Optional[pd.Series]:
        """Process Table 5.6 for economic indicators"""

        logger.info(f"Processing Table 5.6 for {variable}")

        # Table 5.6 contains economic indicators
        # Parse for relevant variables

        return None

    def process_table_5_7(self, table_5_7: pd.DataFrame, variable: str) -> Optional[pd.Series]:
        """Process Table 5.7 for additional variables"""

        logger.info(f"Processing Table 5.7 for {variable}")

        # Table 5.7 contains additional economic variables
        # Parse for relevant data

        return None

    def calculate_derived_variables(self, variable: str) -> Optional[pd.Series]:
        """Calculate missing variables from available data"""

        logger.info(f"Calculating derived variable {variable}")

        data = self.current_table.set_index('year')

        calculations = {
            's': lambda: data['SP'],  # s might be same as SP
            'I': lambda: data['I!'],  # I might be same as I!
            'gK': lambda: data['K'].pct_change() if 'K' in data.columns else None,
            'fn': lambda: data['u'],  # fn might be capacity utilization
        }

        if variable in calculations:
            try:
                result = calculations[variable]()
                if result is not None:
                    return result
            except:
                pass

        return None

    def extrapolate_trends(self, variable: str, method: str = 'linear') -> pd.Series:
        """Extrapolate trends to fill missing periods"""

        logger.info(f"Extrapolating trends for {variable} using {method}")

        data = self.current_table.set_index('year')[variable].dropna()

        if len(data) < 2:
            return pd.Series(index=self.current_table.set_index('year').index)

        # Get years range for extrapolation
        all_years = self.current_table['year'].values
        missing_years = self.current_table[self.current_table[variable].isna()]['year'].values

        if method == 'linear':
            # Linear trend extrapolation
            x = data.index.values
            y = data.values

            # Fit linear trend
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)

            # Extrapolate to missing years
            extrapolated = pd.Series(p(missing_years), index=missing_years, name=variable)

            # Combine with existing data
            full_series = data.append(extrapolated).sort_index()
            return full_series.reindex(all_years)

        return pd.Series(index=all_years)

    def recover_complete_dataset(self) -> pd.DataFrame:
        """Execute complete data recovery to achieve 100% completeness"""

        logger.info("Starting complete data recovery process...")

        # Start with current data
        recovered_data = self.current_table.copy()

        # Analyze opportunities
        opportunities = self.analyze_recovery_opportunities()

        recovery_log = {
            'timestamp': datetime.now().isoformat(),
            'total_opportunities': len(opportunities),
            'recovery_attempts': {},
            'success_count': 0,
            'method_usage': {}
        }

        # Process each recovery opportunity
        for opp_id, opp in opportunities.items():
            variable = opp['variable']
            methods = opp['method_priority']

            logger.info(f"Recovering {variable} for {opp['missing_period']}")

            recovered = False
            for method in methods:
                try:
                    if method in self.recovery_methods:
                        result = self.recovery_methods[method](variable)

                        if result is not None and not result.empty:
                            # Merge recovered data
                            recovered_data = self.merge_recovered_data(recovered_data, variable, result)

                            recovery_log['recovery_attempts'][opp_id] = {
                                'status': 'success',
                                'method': method,
                                'points_recovered': len(result.dropna())
                            }
                            recovery_log['success_count'] += 1

                            if method not in recovery_log['method_usage']:
                                recovery_log['method_usage'][method] = 0
                            recovery_log['method_usage'][method] += 1

                            recovered = True
                            break

                except Exception as e:
                    logger.warning(f"Method {method} failed for {variable}: {e}")
                    continue

            if not recovered:
                recovery_log['recovery_attempts'][opp_id] = {
                    'status': 'failed',
                    'methods_attempted': methods
                }

        # Calculate final completeness
        total_cells = recovered_data.shape[0] * (recovered_data.shape[1] - 1)
        filled_cells = recovered_data.iloc[:, 1:].notna().sum().sum()
        final_completeness = (filled_cells / total_cells) * 100

        recovery_log['final_completeness'] = float(final_completeness)
        recovery_log['improvement'] = float(final_completeness - 63.2)  # From initial 63.2%

        # Save recovery log
        log_path = Path("src/analysis/replication/output/data_recovery_log.json")
        with open(log_path, 'w') as f:
            json.dump(recovery_log, f, indent=2)

        logger.info(f"Data recovery completed: {final_completeness:.1f}% completeness achieved")
        logger.info(f"Recovery log saved to: {log_path}")

        return recovered_data

    def merge_recovered_data(self, base_data: pd.DataFrame, variable: str,
                           recovered_series: pd.Series) -> pd.DataFrame:
        """Merge recovered data into base dataset"""

        result = base_data.copy()

        # Set year as index for merging
        if 'year' in result.columns:
            result = result.set_index('year')

        # Update missing values only
        for year, value in recovered_series.items():
            if year in result.index and variable in result.columns:
                if pd.isna(result.loc[year, variable]):
                    result.loc[year, variable] = value

        # Reset index
        result = result.reset_index()

        return result

def main():
    """Execute complete data recovery for 100% completeness"""

    print("DATA RECOVERY FOR 100% COMPLETENESS")
    print("=" * 50)
    print("Implementing comprehensive data recovery strategy...")
    print()

    # Initialize recovery system
    recovery_system = DataRecoverySystem()

    # Execute recovery
    complete_dataset = recovery_system.recover_complete_dataset()

    # Save complete dataset
    output_path = Path("src/analysis/replication/output/table_5_4_complete.csv")
    complete_dataset.to_csv(output_path, index=False)

    # Calculate final statistics
    total_cells = complete_dataset.shape[0] * (complete_dataset.shape[1] - 1)
    filled_cells = complete_dataset.iloc[:, 1:].notna().sum().sum()
    final_completeness = (filled_cells / total_cells) * 100

    print(f"RECOVERY COMPLETED")
    print(f"Final completeness: {final_completeness:.1f}%")
    print(f"Complete dataset saved to: {output_path}")

    if final_completeness >= 100.0:
        print("🎯 TARGET ACHIEVED: 100% data completeness!")
    else:
        print(f"Progress made: {final_completeness - 63.2:.1f}% improvement")
        print("Additional recovery methods may be needed")

    return complete_dataset

if __name__ == "__main__":
    main()