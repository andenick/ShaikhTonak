"""
KLEMS S&T Variable Analyzer for Phase 2 Extension
Analyzes existing BEA-BLS KLEMS dataset (1997-2023) to extract Shaikh & Tonak variables

This script processes the comprehensive KLEMS dataset to derive:
- K (Capital Stock) from KLEMS capital data
- Labor components from KLEMS labor data
- Value Added and Gross Output for surplus calculations
- Industry-level data with NAICS correspondence
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KLEMSSTAnalyzer:
    def __init__(self):
        """Initialize the KLEMS S&T analyzer."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.klems_dir = self.base_dir / "archive" / "deprecated_code" / "deprecated_databases" / "Database_Leontief_original" / "data" / "processed" / "klems"
        self.output_dir = self.base_dir / "data" / "modern" / "klems_processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Key S&T variables we need to extract from KLEMS
        self.st_variables = {
            'K': {
                'description': 'Capital Stock',
                'klems_sources': [
                    'BEA-BLS-industry-level-production-account-1997-2023__Capital_Art_Quantity.csv',
                    'BEA-BLS-industry-level-production-account-1997-2023__Capital_IT_Quantity.csv',
                    'BEA-BLS-industry-level-production-account-1997-2023__Capital_Other_Quantity.csv'
                ],
                'method': 'sum_capital_components'
            },
            'Labor': {
                'description': 'Labor Input',
                'klems_sources': [
                    'BEA-BLS-industry-level-production-account-1997-2023__Labor_Hours_Quantity.csv',
                    'BEA-BLS-industry-level-production-account-1997-2023__Labor_NoCol_Compensation.csv',
                    'BEA-BLS-industry-level-production-account-1997-2023__Labor_Col_Compensation.csv'
                ],
                'method': 'process_labor_components'
            },
            'GO': {
                'description': 'Gross Output',
                'klems_sources': [
                    'BEA-BLS-industry-level-production-account-1997-2023__Gross_Output.csv'
                ],
                'method': 'direct_extract'
            },
            'VA': {
                'description': 'Value Added',
                'klems_sources': [
                    'BEA-BLS-industry-level-production-account-1997-2023__Value_Added.csv'
                ],
                'method': 'direct_extract'
            }
        }

        logger.info(f"KLEMS S&T Analyzer initialized")
        logger.info(f"KLEMS data directory: {self.klems_dir}")
        logger.info(f"Output directory: {self.output_dir}")

    def load_klems_file(self, filename):
        """Load a KLEMS CSV file and return DataFrame."""
        file_path = self.klems_dir / filename
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                logger.info(f"Loaded {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
                return df
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
                return None
        else:
            logger.warning(f"File not found: {filename}")
            return None

    def get_naics_mapping(self):
        """Load NAICS codes mapping from KLEMS data."""
        naics_file = 'BEA-BLS-industry-level-production-account-1997-2023__NAICS_codes.csv'
        df = self.load_klems_file(naics_file)

        if df is not None:
            logger.info(f"NAICS mapping loaded: {len(df)} industries")
            return df
        else:
            logger.error("Failed to load NAICS mapping")
            return None

    def process_capital_stock(self):
        """Process KLEMS capital data to derive S&T capital stock (K)."""
        logger.info("Processing capital stock data...")

        capital_files = self.st_variables['K']['klems_sources']
        capital_dfs = []

        for filename in capital_files:
            df = self.load_klems_file(filename)
            if df is not None:
                # Add source identifier
                df['capital_type'] = filename.split('__')[1].split('_')[1]  # Extract type (Art, IT, Other)
                capital_dfs.append(df)

        if not capital_dfs:
            logger.error("No capital data files found")
            return None

        # Combine all capital types
        combined_capital = pd.concat(capital_dfs, ignore_index=True)

        # Aggregate by industry and year (sum across capital types)
        if 'Industry Description' in combined_capital.columns and 'Year' in combined_capital.columns:
            capital_aggregated = combined_capital.groupby(['Industry Description', 'Year']).agg({
                'Value': 'sum',  # Sum across capital types
                'Workbook': 'first',  # Take the first workbook name
                'Sheet': 'first'  # Take the first sheet name
            }).reset_index()

            logger.info(f"Capital stock processed: {len(capital_aggregated)} industry-year observations")
            return capital_aggregated
        else:
            logger.error("Required columns (Industry Description, Year) not found in capital data")
            logger.error(f"Available columns: {list(combined_capital.columns)}")
            return None

    def process_labor_data(self):
        """Process KLEMS labor data to derive S&T labor variables."""
        logger.info("Processing labor data...")

        labor_files = self.st_variables['Labor']['klems_sources']
        labor_data = {}

        for filename in labor_files:
            df = self.load_klems_file(filename)
            if df is not None:
                # Identify data type from filename
                if 'Hours' in filename:
                    labor_data['hours'] = df
                elif 'NoCol_Compensation' in filename:
                    labor_data['compensation_nocol'] = df
                elif 'Col_Compensation' in filename:
                    labor_data['compensation_col'] = df

        if not labor_data:
            logger.error("No labor data files found")
            return None

        # Process each component
        processed_labor = {}
        for data_type, df in labor_data.items():
            if 'Industry Description' in df.columns and 'Year' in df.columns:
                processed_labor[data_type] = df[['Industry Description', 'Year', 'Value']].copy()
            else:
                logger.warning(f"Required columns not found in {data_type}")
                logger.warning(f"Available columns: {list(df.columns)}")

        logger.info(f"Labor data processed: {len(processed_labor)} components")
        return processed_labor

    def process_output_data(self):
        """Process KLEMS output data (Gross Output and Value Added)."""
        logger.info("Processing output data...")

        output_data = {}

        # Process Gross Output
        go_df = self.load_klems_file(self.st_variables['GO']['klems_sources'][0])
        if go_df is not None:
            output_data['gross_output'] = go_df

        # Process Value Added
        va_df = self.load_klems_file(self.st_variables['VA']['klems_sources'][0])
        if va_df is not None:
            output_data['value_added'] = va_df

        logger.info(f"Output data processed: {len(output_data)} series")
        return output_data

    def calculate_st_surplus(self, output_data, labor_data):
        """Calculate surplus variables for S&T analysis."""
        logger.info("Calculating S&T surplus variables...")

        if 'gross_output' not in output_data or 'value_added' not in output_data:
            logger.error("Required output data not available for surplus calculation")
            return None

        if 'compensation_nocol' not in labor_data or 'compensation_col' not in labor_data:
            logger.error("Required labor compensation data not available")
            return None

        # Get the data
        go_df = output_data['gross_output'].copy()
        va_df = output_data['value_added'].copy()
        comp_nocol = labor_data['compensation_nocol'].copy()
        comp_col = labor_data['compensation_col'].copy()

        # Merge labor compensation
        total_compensation = pd.merge(
            comp_nocol[['Industry Description', 'Year', 'Value']],
            comp_col[['Industry Description', 'Year', 'Value']],
            on=['Industry Description', 'Year'],
            suffixes=('_nocol', '_col'),
            how='outer'
        )
        total_compensation['total_labor_comp'] = (
            total_compensation['Value_nocol'].fillna(0) +
            total_compensation['Value_col'].fillna(0)
        )

        # Merge with Value Added to calculate surplus
        surplus_data = pd.merge(
            va_df[['Industry Description', 'Year', 'Value']],
            total_compensation[['Industry Description', 'Year', 'total_labor_comp']],
            on=['Industry Description', 'Year'],
            how='inner'
        )

        # Calculate surplus as Value Added - Total Labor Compensation
        surplus_data['surplus'] = surplus_data['Value'] - surplus_data['total_labor_comp']
        surplus_data['surplus_rate'] = surplus_data['surplus'] / surplus_data['Value']

        logger.info(f"Surplus calculated for {len(surplus_data)} industry-year observations")
        return surplus_data

    def create_st_time_series(self):
        """Create complete S&T time series from KLEMS data."""
        logger.info("Creating S&T time series from KLEMS data...")

        # Process all components
        capital_data = self.process_capital_stock()
        labor_data = self.process_labor_data()
        output_data = self.process_output_data()

        if not all([capital_data is not None, labor_data, output_data]):
            logger.error("Failed to process required KLEMS components")
            return None

        # Calculate surplus
        surplus_data = self.calculate_st_surplus(output_data, labor_data)

        if surplus_data is None:
            logger.error("Failed to calculate surplus data")
            return None

        # Combine all S&T variables
        st_timeseries = {}

        # Capital stock (K)
        if capital_data is not None:
            st_timeseries['capital_stock'] = capital_data

        # Labor variables
        for var_name, var_data in labor_data.items():
            st_timeseries[f'labor_{var_name}'] = var_data

        # Output variables
        for var_name, var_data in output_data.items():
            st_timeseries[var_name] = var_data

        # Surplus variables
        st_timeseries['surplus'] = surplus_data

        logger.info(f"S&T time series created with {len(st_timeseries)} variable sets")
        return st_timeseries

    def save_st_data(self, st_timeseries):
        """Save the processed S&T data."""
        if not st_timeseries:
            logger.error("No S&T data to save")
            return False

        logger.info("Saving S&T data...")

        # Save each variable set
        for var_name, var_data in st_timeseries.items():
            filename = f"st_{var_name}_1997_2023.csv"
            filepath = self.output_dir / filename
            var_data.to_csv(filepath, index=False)
            logger.info(f"Saved {var_name}: {filepath}")

        # Create summary metadata
        metadata = {
            'processing_date': datetime.now().isoformat(),
            'source': 'BEA-BLS KLEMS Dataset',
            'period': '1997-2023',
            'variables_processed': list(st_timeseries.keys()),
            'description': 'Shaikh & Tonak variables derived from KLEMS industry-level production accounts',
            'total_files': len(st_timeseries)
        }

        metadata_file = self.output_dir / "st_variables_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Metadata saved: {metadata_file}")
        return True

    def run_analysis(self):
        """Run complete KLEMS S&T analysis."""
        logger.info("="*60)
        logger.info("STARTING KLEMS S&T VARIABLE ANALYSIS")
        logger.info("="*60)

        try:
            # Check if KLEMS directory exists
            if not self.klems_dir.exists():
                logger.error(f"KLEMS directory not found: {self.klems_dir}")
                return False

            # Load NAICS mapping
            naics_mapping = self.get_naics_mapping()
            if naics_mapping is None:
                logger.warning("NAICS mapping not available, proceeding without industry mapping")

            # Create S&T time series
            st_timeseries = self.create_st_time_series()

            if st_timeseries:
                # Save the data
                success = self.save_st_data(st_timeseries)

                if success:
                    logger.info("="*60)
                    logger.info("✅ KLEMS S&T ANALYSIS COMPLETE")
                    logger.info("="*60)
                    return True
                else:
                    logger.error("Failed to save S&T data")
                    return False
            else:
                logger.error("Failed to create S&T time series")
                return False

        except Exception as e:
            logger.error(f"Analysis failed with error: {e}")
            return False

def main():
    """Main execution function."""
    analyzer = KLEMSSTAnalyzer()
    success = analyzer.run_analysis()

    if success:
        print("\nSUCCESS: KLEMS S&T ANALYSIS COMPLETE")
        print("S&T variables for 1997-2023 extracted from KLEMS dataset")
        print("Next step: Data integration framework")
    else:
        print("\nFAILED: KLEMS S&T ANALYSIS")
        print("Check logs for details")

if __name__ == "__main__":
    main()