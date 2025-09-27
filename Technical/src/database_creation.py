#!/usr/bin/env python3
"""
Corrected Historical Database Creation for Shaikh & Tonak Replication
====================================================================

This corrected version properly handles the extracted data structure where:
- Years are in column headers (2, 3, 4, etc.)
- Variable names are in the first column
- Data values are in the matrix
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class CorrectedDatabaseCreator:
    """Creates unified historical database with corrected data structure handling"""

    def __init__(self, base_path: str = "outputs/comprehensive_extraction"):
        self.base_path = Path(base_path)
        self.book_tables_path = Path("Database_Leontief/book_tables/final")
        self.output_path = self.base_path / "unified_database"
        self.output_path.mkdir(exist_ok=True)

        self.setup_logging()
        self.unified_data = {}

    def setup_logging(self):
        """Configure logging"""
        log_file = self.output_path / "corrected_database_creation.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ],
            force=True
        )
        self.logger = logging.getLogger(__name__)

    def parse_extracted_table(self, file_path: Path) -> pd.DataFrame:
        """Parse extracted table with years as columns"""
        try:
            df = pd.read_csv(file_path)

            # Check if this has the standard extracted format:
            # Column 0: variable names
            # Columns 1+: year data (may start from column 2, 3, etc.)

            if df.shape[1] > 10 and df.shape[0] > 2:  # Likely time series data
                # First column contains variable names
                variable_col = df.iloc[:, 0]

                # Remaining columns are years - try to identify year columns
                year_columns = []
                year_values = []

                for col_idx in range(1, df.shape[1]):
                    col_name = df.columns[col_idx]

                    # Check if column name could be a year offset
                    try:
                        year_offset = int(col_name)
                        # Assume base year (need to determine from context)
                        # Many tables seem to start around 1960s-1970s
                        if year_offset >= 0 and year_offset < 100:
                            estimated_year = 1960 + year_offset  # Rough estimate
                            year_columns.append(col_name)
                            year_values.append(estimated_year)
                    except:
                        # Column name is not numeric, skip
                        continue

                if len(year_columns) > 5:  # If we found reasonable year structure
                    # Reshape data
                    reshaped_data = []

                    for row_idx in range(df.shape[0]):
                        variable_name = df.iloc[row_idx, 0]
                        if pd.notna(variable_name) and str(variable_name).strip():
                            for col_idx, year_col in enumerate(year_columns):
                                value = df.iloc[row_idx, df.columns.get_loc(year_col)]
                                estimated_year = year_values[col_idx]

                                if pd.notna(value):
                                    try:
                                        numeric_value = float(value)
                                        reshaped_data.append({
                                            'variable': variable_name,
                                            'year': estimated_year,
                                            'value': numeric_value
                                        })
                                    except:
                                        pass

                    if reshaped_data:
                        result_df = pd.DataFrame(reshaped_data)
                        return result_df

            # If not in expected format, return as-is
            return df

        except Exception as e:
            self.logger.error(f"Error parsing {file_path}: {e}")
            return pd.DataFrame()

    def process_nipa_data(self) -> Dict[str, pd.DataFrame]:
        """Process NIPA data files"""
        self.logger.info("Processing NIPA data...")

        nipa_path = self.base_path / "nipa_data"
        nipa_results = {}

        # Key NIPA tables
        key_files = {
            'table_1_1.csv': 'gnp_components',
            'table_1_9.csv': 'national_income',
            'table_1_22.csv': 'government_receipts',
            'table_2_9.csv': 'personal_income',
            'table_3_16.csv': 'fixed_investment'
        }

        for filename, table_name in key_files.items():
            file_path = nipa_path / filename
            if file_path.exists():
                df = self.parse_extracted_table(file_path)
                if not df.empty:
                    nipa_results[table_name] = df
                    self.logger.info(f"Processed {table_name}: {df.shape}")

        return nipa_results

    def process_bls_data(self) -> Dict[str, pd.DataFrame]:
        """Process BLS employment data"""
        self.logger.info("Processing BLS employment data...")

        bls_path = self.base_path / "bls_employment"
        bls_results = {}

        # Look for table with substantial employment time series
        for csv_file in bls_path.glob("*.csv"):
            if csv_file.name.endswith('_1.csv'):  # Main employment tables
                df = self.parse_extracted_table(csv_file)
                if not df.empty and 'year' in df.columns:
                    table_name = csv_file.stem
                    bls_results[table_name] = df
                    self.logger.info(f"Processed {table_name}: {df.shape}")

        return bls_results

    def process_book_tables(self) -> Dict[str, pd.DataFrame]:
        """Process book table extractions"""
        self.logger.info("Processing book table extractions...")

        book_results = {}

        # Key Shaikh-Tonak tables
        key_tables = {
            'table_5_4_economic_vars': ['table_p36_camelot[page]_0.csv', 'table_p37_camelot[page]_0.csv'],
            'table_5_5_labor': ['table_5_5.csv'],
            'table_5_6_depreciation': ['table_p46_camelot[page]_0.csv'],
            'table_5_7_real_income': ['table_p47_camelot[page]_0.csv']
        }

        for table_name, filenames in key_tables.items():
            combined_data = []

            for filename in filenames:
                file_path = self.book_tables_path / filename
                if file_path.exists():
                    try:
                        df = pd.read_csv(file_path)
                        # Book tables may have years in first row or column
                        # Look for year-like patterns

                        if df.shape[1] > 10:  # Wide table, years likely in columns
                            # Check first row for years
                            first_row = df.iloc[0, :].astype(str)
                            year_pattern = first_row.str.match(r'19[4-9]\d')

                            if year_pattern.any():
                                # Years found in first row
                                years = first_row[year_pattern].astype(int).tolist()
                                variable_names = df.iloc[1:, 0].dropna().tolist()

                                for var_idx, var_name in enumerate(variable_names):
                                    if var_idx + 1 < df.shape[0]:
                                        for year_idx, year in enumerate(years):
                                            if year_idx + 1 < df.shape[1]:
                                                value = df.iloc[var_idx + 1, year_idx + 1]
                                                try:
                                                    numeric_value = float(value)
                                                    combined_data.append({
                                                        'variable': var_name,
                                                        'year': year,
                                                        'value': numeric_value
                                                    })
                                                except:
                                                    pass

                    except Exception as e:
                        self.logger.error(f"Error processing {filename}: {e}")

            if combined_data:
                book_results[table_name] = pd.DataFrame(combined_data)
                self.logger.info(f"Processed {table_name}: {len(combined_data)} observations")

        return book_results

    def create_time_series_database(self) -> pd.DataFrame:
        """Create unified time series database"""
        self.logger.info("Creating unified time series database...")

        # Process all data sources
        nipa_data = self.process_nipa_data()
        bls_data = self.process_bls_data()
        book_data = self.process_book_tables()

        # Combine all data
        all_data = []

        for source_name, source_dict in [('nipa', nipa_data), ('bls', bls_data), ('book', book_data)]:
            for table_name, df in source_dict.items():
                if not df.empty and 'year' in df.columns and 'variable' in df.columns:
                    df['source'] = source_name
                    df['table'] = table_name
                    all_data.append(df)

        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)

            # Create pivot table with variables as columns
            pivot_df = combined_df.pivot_table(
                index='year',
                columns=['source', 'table', 'variable'],
                values='value',
                aggfunc='mean'  # Average if duplicates
            )

            # Flatten column names
            pivot_df.columns = [f"{source}_{table}_{var}" for source, table, var in pivot_df.columns]

            # Filter to Shaikh-Tonak period
            analysis_period = pivot_df.loc[1947:1989] if 1947 in pivot_df.index else pivot_df

            self.logger.info(f"Created unified database: {pivot_df.shape}")
            self.logger.info(f"Analysis period: {analysis_period.shape}")

            return pivot_df, analysis_period

        else:
            self.logger.warning("No data found to combine")
            return pd.DataFrame(), pd.DataFrame()

    def export_results(self, full_df: pd.DataFrame, analysis_df: pd.DataFrame):
        """Export results"""
        self.logger.info("Exporting corrected database results...")

        # Export full database
        full_path = self.output_path / "corrected_historical_database.csv"
        full_df.to_csv(full_path)

        # Export analysis period
        analysis_path = self.output_path / "shaikh_tonak_analysis_period.csv"
        analysis_df.to_csv(analysis_path)

        # Create metadata
        metadata = {
            'creation_date': datetime.now().isoformat(),
            'full_database': {
                'shape': full_df.shape,
                'years': f"{full_df.index.min()}-{full_df.index.max()}",
                'variables': len(full_df.columns)
            },
            'analysis_period': {
                'shape': analysis_df.shape,
                'years': f"{analysis_df.index.min()}-{analysis_df.index.max()}" if not analysis_df.empty else "Empty",
                'variables': len(analysis_df.columns)
            }
        }

        metadata_path = self.output_path / "corrected_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        # Summary report
        report_lines = [
            "# CORRECTED SHAIKH & TONAK DATABASE SUMMARY",
            "=" * 50,
            "",
            f"Creation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## FULL DATABASE",
            f"Shape: {full_df.shape}",
            f"Years: {full_df.index.min()}-{full_df.index.max()}" if not full_df.empty else "No data",
            f"Variables: {len(full_df.columns)}",
            "",
            "## ANALYSIS PERIOD (1947-1989)",
            f"Shape: {analysis_df.shape}",
            f"Years: {analysis_df.index.min()}-{analysis_df.index.max()}" if not analysis_df.empty else "No data",
            f"Variables: {len(analysis_df.columns)}",
            "",
            "## VARIABLE SUMMARY (Top 20)",
            ""
        ]

        if not full_df.empty:
            # Add top variables by data coverage
            coverage = full_df.notna().sum().sort_values(ascending=False).head(20)
            for var_name, count in coverage.items():
                report_lines.append(f"{var_name}: {count} observations")

        report_path = self.output_path / "corrected_summary_report.txt"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))

        self.logger.info(f"Results exported to: {self.output_path}")

        return full_path, analysis_path, metadata_path, report_path


def main():
    """Main execution"""
    print("Creating Corrected Shaikh & Tonak Historical Database...")
    print("=" * 60)

    creator = CorrectedDatabaseCreator()
    full_df, analysis_df = creator.create_time_series_database()

    if not full_df.empty:
        paths = creator.export_results(full_df, analysis_df)

        print("")
        print("SUCCESS: Corrected Database Created")
        print(f"Full Database: {full_df.shape}")
        print(f"Analysis Period: {analysis_df.shape}")
        print("")
        print("Files Created:")
        for path in paths:
            print(f"- {path.name}")
    else:
        print("WARNING: No data found to process")


if __name__ == "__main__":
    main()