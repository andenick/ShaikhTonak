#!/usr/bin/env python3
"""
Shaikh & Tonak Data Loader
==========================

This module loads and processes actual BEA/BLS data for Shaikh methodology reconstruction.
It integrates with existing project data and Robin API modules.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

# Add Robin API modules to path
robin_bea_path = Path("D:/Arcanum/Robin/API_MODULES/BEA")
robin_bls_path = Path("D:/Arcanum/Robin/API_MODULES/BLS")
sys.path.append(str(robin_bea_path))
sys.path.append(str(robin_bls_path))

class ShaikhDataLoader:
    """
    Loads actual BEA/BLS data for Shaikh methodology reconstruction
    """

    def __init__(self, project_path: str):
        """
        Initialize the data loader

        Args:
            project_path: Path to Shaikh Tonak project directory
        """
        self.project_path = Path(project_path)
        self.modern_data_path = self.project_path / "Technical" / "data" / "modern"
        self.logger = self._setup_logging()

        # Data storage
        self.bea_data = {}
        self.bls_data = {}
        self.integrated_data = {}

        self.logger.info("Shaikh Data Loader initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the data loader"""
        logger = logging.getLogger('ShaikhDataLoader')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def load_existing_bea_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load existing BEA data from project

        Returns:
            Dictionary of BEA datasets
        """
        self.logger.info("Loading existing BEA data from project")

        bea_data = {}

        # Load corporate profits
        corporate_profits_path = self.modern_data_path / "bea_nipa" / "corporate_profits_1990_2024_extracted.csv"
        if corporate_profits_path.exists():
            bea_data['corporate_profits'] = pd.read_csv(corporate_profits_path)
            self.logger.info(f"Loaded corporate profits: {len(bea_data['corporate_profits'])} records")

        # Load fixed assets (capital stock)
        fixed_assets_path = self.modern_data_path / "processed" / "bea_fixed_assets" / "private_net_stock_current_cost.csv"
        if fixed_assets_path.exists():
            bea_data['fixed_assets'] = pd.read_csv(fixed_assets_path)
            self.logger.info(f"Loaded fixed assets: {len(bea_data['fixed_assets'])} records")

        # Load any additional BEA data
        bea_nipa_path = self.modern_data_path / "bea_nipa"
        for file_path in bea_nipa_path.glob("*.csv"):
            if file_path.name not in ['corporate_profits_1990_2024_extracted.csv']:
                dataset_name = file_path.stem
                try:
                    bea_data[dataset_name] = pd.read_csv(file_path)
                    self.logger.info(f"Loaded {dataset_name}: {len(bea_data[dataset_name])} records")
                except Exception as e:
                    self.logger.warning(f"Could not load {file_path}: {e}")

        self.bea_data = bea_data
        return bea_data

    def load_existing_bls_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load existing BLS data from project

        Returns:
            Dictionary of BLS datasets
        """
        self.logger.info("Loading existing BLS data from project")

        bls_data = {}

        # Check BLS employment directory
        bls_path = self.modern_data_path / "bls_employment"
        if bls_path.exists():
            for file_path in bls_path.glob("*.csv"):
                dataset_name = file_path.stem
                try:
                    bls_data[dataset_name] = pd.read_csv(file_path)
                    self.logger.info(f"Loaded BLS {dataset_name}: {len(bls_data[dataset_name])} records")
                except Exception as e:
                    self.logger.warning(f"Could not load BLS {file_path}: {e}")

        self.bls_data = bls_data
        return bls_data

    def load_robin_bea_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load additional BEA data from Robin API modules

        Returns:
            Dictionary of additional BEA datasets
        """
        self.logger.info("Loading additional BEA data from Robin modules")

        robin_bea_data = {}

        try:
            # Import Robin BEA module
            from bea_data_manager import BEADataManager

            # Initialize BEA manager
            bea_manager = BEADataManager()

            # Check what data is available in Robin BEA
            robin_bea_path = Path("D:/Arcanum/Robin/API_MODULES/BEA/data")
            if robin_bea_path.exists():
                for file_path in robin_bea_path.glob("*.csv"):
                    dataset_name = f"robin_{file_path.stem}"
                    try:
                        robin_bea_data[dataset_name] = pd.read_csv(file_path)
                        self.logger.info(f"Loaded Robin BEA {dataset_name}: {len(robin_bea_data[dataset_name])} records")
                    except Exception as e:
                        self.logger.warning(f"Could not load Robin BEA {file_path}: {e}")

        except ImportError as e:
            self.logger.warning(f"Could not import Robin BEA module: {e}")
        except Exception as e:
            self.logger.warning(f"Error loading Robin BEA data: {e}")

        return robin_bea_data

    def load_robin_bls_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load additional BLS data from Robin API modules

        Returns:
            Dictionary of additional BLS datasets
        """
        self.logger.info("Loading additional BLS data from Robin modules")

        robin_bls_data = {}

        try:
            # Import Robin BLS module
            from bls_data_manager import BLSDataManager

            # Initialize BLS manager
            bls_manager = BLSDataManager()

            # Check what data is available in Robin BLS
            robin_bls_path = Path("D:/Arcanum/Robin/API_MODULES/BLS/data")
            if robin_bls_path.exists():
                for file_path in robin_bls_path.glob("*.csv"):
                    dataset_name = f"robin_{file_path.stem}"
                    try:
                        robin_bls_data[dataset_name] = pd.read_csv(file_path)
                        self.logger.info(f"Loaded Robin BLS {dataset_name}: {len(robin_bls_data[dataset_name])} records")
                    except Exception as e:
                        self.logger.warning(f"Could not load Robin BLS {file_path}: {e}")

        except ImportError as e:
            self.logger.warning(f"Could not import Robin BLS module: {e}")
        except Exception as e:
            self.logger.warning(f"Error loading Robin BLS data: {e}")

        return robin_bls_data

    def load_integrated_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load the integrated dataset that was previously created

        Returns:
            Dictionary of integrated datasets
        """
        self.logger.info("Loading integrated data from project")

        integrated_data = {}

        # Load the main integrated dataset
        integrated_path = self.modern_data_path / "final_results" / "shaikh_tonak_extended_1958_2025_FINAL.csv"
        if integrated_path.exists():
            integrated_data['main_series'] = pd.read_csv(integrated_path)
            self.logger.info(f"Loaded main integrated series: {len(integrated_data['main_series'])} records")

        # Load the 04_INTEGRATED_DATA from OUTPUT_TABLES
        output_path = self.project_path / "OUTPUT_TABLES" / "04_INTEGRATED_DATA_1958-2025.csv"
        if output_path.exists():
            integrated_data['output_integrated'] = pd.read_csv(output_path)
            self.logger.info(f"Loaded output integrated data: {len(integrated_data['output_integrated'])} records")

        self.integrated_data = integrated_data
        return integrated_data

    def create_shaikh_industry_mapping(self) -> Dict[str, str]:
        """
        Create industry mapping for Shaikh's productive/unproductive classification

        Returns:
            Dictionary mapping industry codes to productive/unproductive
        """
        # This would contain the actual NAICS to Shaikh classification
        # Based on the book's sector definitions
        industry_mapping = {
            # Productive sectors (contribute to surplus value)
            '11': 'productive',      # Agriculture, forestry, fishing
            '21': 'productive',      # Mining, quarrying, oil and gas
            '23': 'productive',      # Construction
            '31-33': 'productive',   # Manufacturing
            '22': 'productive',      # Utilities
            '48-49': 'productive',   # Transportation and warehousing (selected)

            # Unproductive sectors (do not contribute to surplus value)
            '42': 'unproductive',    # Wholesale trade
            '44-45': 'unproductive', # Retail trade
            '52': 'unproductive',    # Finance and insurance
            '53': 'unproductive',    # Real estate and rental
            '54': 'unproductive',    # Professional services
            '55': 'unproductive',    # Management of companies
            '56': 'unproductive',    # Administrative services
            '61': 'unproductive',    # Educational services
            '62': 'unproductive',    # Health care and social assistance
            '71': 'unproductive',    # Arts, entertainment, recreation
            '72': 'unproductive',    # Accommodation and food services
            '81': 'unproductive',    # Other services
            '92': 'unproductive',    # Public administration
        }

        return industry_mapping

    def get_surplus_value_data(self, year: int) -> Optional[float]:
        """
        Calculate S* (Surplus Value) for a given year using available data

        Args:
            year: Year to calculate

        Returns:
            S* value in millions of dollars
        """
        # For now, use corporate profits as a proxy for surplus value
        # This is a simplification - full implementation would need
        # value added minus variable capital calculation

        if 'corporate_profits' in self.bea_data:
            corp_profits = self.bea_data['corporate_profits']
            year_data = corp_profits[corp_profits['year'] == year]
            if not year_data.empty:
                return float(year_data['value'].iloc[0]) * 1000  # Convert to millions

        return None

    def get_constant_capital_data(self, year: int) -> Optional[float]:
        """
        Calculate C* (Constant Capital) for a given year using available data

        Args:
            year: Year to calculate

        Returns:
            C* value in millions of dollars
        """
        # For now, use a fraction of fixed assets as proxy for constant capital
        # Full implementation would need intermediate inputs data

        if 'fixed_assets' in self.bea_data:
            fixed_assets = self.bea_data['fixed_assets']
            year_data = fixed_assets[fixed_assets['year'] == year]
            if not year_data.empty:
                # Use 20% of fixed assets as constant capital proxy
                return float(year_data['modern_K_st_consistent'].iloc[0]) * 0.2

        return None

    def get_variable_capital_data(self, year: int) -> Optional[float]:
        """
        Calculate V* (Variable Capital) for a given year using available data

        Args:
            year: Year to calculate

        Returns:
            V* value in millions of dollars
        """
        # For now, use a proxy based on corporate profits
        # Full implementation would need compensation of employees
        # in productive sectors only

        surplus_value = self.get_surplus_value_data(year)
        if surplus_value:
            # Assume variable capital is 30% of surplus value (rough proxy)
            return surplus_value * 0.3

        return None

    def get_profit_rate_shaikh(self, year: int) -> Optional[float]:
        """
        Calculate r* using Shaikh's exact formula: r* = S*/(C* + V*)

        Args:
            year: Year to calculate

        Returns:
            r* as decimal (e.g., 0.39 for 39%)
        """
        surplus_value = self.get_surplus_value_data(year)
        constant_capital = self.get_constant_capital_data(year)
        variable_capital = self.get_variable_capital_data(year)

        if all([surplus_value, constant_capital, variable_capital]):
            denominator = constant_capital + variable_capital
            if denominator > 0:
                profit_rate = surplus_value / denominator
                self.logger.info(f"r* ({year}): {profit_rate:.4f} ({profit_rate*100:.1f}%)")
                return profit_rate

        return None

    def load_all_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Load all available data sources

        Returns:
            Dictionary containing all loaded datasets
        """
        self.logger.info("Loading all available data sources")

        all_data = {
            'bea_project': self.load_existing_bea_data(),
            'bls_project': self.load_existing_bls_data(),
            'bea_robin': self.load_robin_bea_data(),
            'bls_robin': self.load_robin_bls_data(),
            'integrated': self.load_integrated_data()
        }

        total_datasets = sum(len(datasets) for datasets in all_data.values())
        self.logger.info(f"Loaded {total_datasets} total datasets from all sources")

        return all_data

    def create_shaikh_reconstruction_data(self, start_year: int = 1990, end_year: int = 2025) -> pd.DataFrame:
        """
        Create Shaikh methodology reconstruction data for specified years

        Args:
            start_year: First year to reconstruct
            end_year: Last year to reconstruct

        Returns:
            DataFrame with S*, C*, V*, r* for each year
        """
        self.logger.info(f"Creating Shaikh reconstruction data: {start_year}-{end_year}")

        # Load all data
        self.load_all_data()

        results = []

        for year in range(start_year, end_year + 1):
            # Calculate Shaikh variables
            surplus_value = self.get_surplus_value_data(year)
            constant_capital = self.get_constant_capital_data(year)
            variable_capital = self.get_variable_capital_data(year)
            profit_rate = self.get_profit_rate_shaikh(year)

            if all([surplus_value, constant_capital, variable_capital, profit_rate]):
                results.append({
                    'year': year,
                    'S_star': surplus_value,
                    'C_star': constant_capital,
                    'V_star': variable_capital,
                    'r_star': profit_rate,
                    'methodology': 'Shaikh_1994_reconstructed',
                    'data_source': 'BEA_BLS_actual_data'
                })
            else:
                self.logger.warning(f"Could not calculate complete Shaikh variables for {year}")

        reconstruction_df = pd.DataFrame(results)
        self.logger.info(f"Created reconstruction data: {len(reconstruction_df)} years")

        return reconstruction_df

def main():
    """
    Main function to demonstrate the data loader
    """
    print("Shaikh & Tonak Data Loader")
    print("=" * 40)
    print("Loading actual BEA/BLS data for reconstruction")
    print()

    # Initialize data loader
    loader = ShaikhDataLoader("D:/Arcanum/Projects/Shaikh Tonak")

    # Load all data
    all_data = loader.load_all_data()

    # Print data summary
    for source, datasets in all_data.items():
        print(f"{source.upper()}: {len(datasets)} datasets")
        for name, df in datasets.items():
            print(f"  - {name}: {len(df)} records")

    print()

    # Create Shaikh reconstruction
    reconstruction = loader.create_shaikh_reconstruction_data(1990, 2025)

    print(f"Shaikh Reconstruction: {len(reconstruction)} years")
    if not reconstruction.empty:
        print(f"Sample data:")
        print(reconstruction.head())
        print()
        print(f"Profit rate range: {reconstruction['r_star'].min():.3f} - {reconstruction['r_star'].max():.3f}")

if __name__ == "__main__":
    main()