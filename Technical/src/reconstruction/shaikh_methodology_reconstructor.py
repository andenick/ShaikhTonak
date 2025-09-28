#!/usr/bin/env python3
"""
Shaikh & Tonak Methodology Reconstructor
========================================

This module implements the exact reconstruction of modern data (1990-2025)
using Shaikh's original methodology from the 1994 book.

CRITICAL OBJECTIVE:
Create a unified 67-year profit rate series using the consistent formula:
r* = S*/(C* + V*)

Where:
- S* = Surplus Value (VA* - V*)
- C* = Constant Capital (intermediate inputs, productive sectors)
- V* = Variable Capital (productive worker wages)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
import json

class ShaikhMethodologyReconstructor:
    """
    Reconstructs modern profit rates using Shaikh's exact 1994 methodology
    """

    def __init__(self, data_path: str, config_path: str):
        """
        Initialize the reconstructor with data and configuration paths

        Args:
            data_path: Path to modern data sources (BEA, BLS, etc.)
            config_path: Path to configuration files (sector mappings, etc.)
        """
        self.data_path = Path(data_path)
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()

        # Core variables for Shaikh methodology
        self.surplus_value = {}  # S* by year
        self.constant_capital = {}  # C* by year
        self.variable_capital = {}  # V* by year
        self.profit_rate = {}  # r* by year

        # Sector classifications
        self.productive_sectors = []
        self.unproductive_sectors = []
        self.sector_mapping = {}

        self.logger.info("Shaikh Methodology Reconstructor initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the reconstruction process"""
        logger = logging.getLogger('ShaikhReconstructor')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def load_sector_mapping(self) -> None:
        """
        Load Shaikh's exact sector definitions and NAICS→SIC mappings

        From book methodology:
        Productive: Manufacturing, Mining, Construction, Transportation, Agriculture, Utilities
        Unproductive: Finance/Insurance/Real Estate, Government, Professional Services, Trade
        """

        # Shaikh's exact productive sectors (1994 SIC basis)
        self.productive_sectors = [
            'Agriculture, Forestry, Fishing',  # SIC 01-09
            'Mining',  # SIC 10-14
            'Construction',  # SIC 15-17
            'Manufacturing',  # SIC 20-39
            'Transportation, Communications, Utilities'  # SIC 40-49 (selected)
        ]

        # Shaikh's exact unproductive sectors
        self.unproductive_sectors = [
            'Wholesale Trade',  # SIC 50-51
            'Retail Trade',  # SIC 52-59
            'Finance, Insurance, Real Estate',  # SIC 60-67
            'Services',  # SIC 70-89 (selected)
            'Government'  # Government enterprises
        ]

        # Modern NAICS to Shaikh classification mapping
        self.sector_mapping = {
            # Productive sectors (NAICS codes)
            '11': 'productive',  # Agriculture, forestry, fishing
            '21': 'productive',  # Mining, quarrying, oil and gas
            '23': 'productive',  # Construction
            '31-33': 'productive',  # Manufacturing
            '22': 'productive',  # Utilities
            '48-49': 'productive',  # Transportation and warehousing (selected)

            # Unproductive sectors (NAICS codes)
            '42': 'unproductive',  # Wholesale trade
            '44-45': 'unproductive',  # Retail trade
            '52': 'unproductive',  # Finance and insurance
            '53': 'unproductive',  # Real estate and rental
            '54': 'unproductive',  # Professional services
            '55': 'unproductive',  # Management of companies
            '56': 'unproductive',  # Administrative services
            '61': 'unproductive',  # Educational services
            '62': 'unproductive',  # Health care and social assistance
            '71': 'unproductive',  # Arts, entertainment, recreation
            '72': 'unproductive',  # Accommodation and food services
            '81': 'unproductive',  # Other services
            '92': 'unproductive',  # Public administration
        }

        self.logger.info(f"Loaded sector mapping: {len(self.productive_sectors)} productive, {len(self.unproductive_sectors)} unproductive")

    def calculate_variable_capital(self, year: int, industry_data: pd.DataFrame) -> float:
        """
        Calculate V* (Variable Capital) = Productive worker wage bill

        From book: V* = Wp = total variable capital (productive sectors only)

        Args:
            year: Year to calculate
            industry_data: BEA/BLS compensation data by industry

        Returns:
            V* in millions of dollars
        """

        # Filter to productive sectors only
        productive_data = industry_data[
            industry_data['naics_code'].map(
                lambda x: self.sector_mapping.get(x, 'unproductive') == 'productive'
            )
        ]

        # Sum compensation of employees in productive sectors
        variable_capital = productive_data['compensation_of_employees'].sum()

        self.logger.info(f"V* ({year}): ${variable_capital:,.0f} million")
        return variable_capital

    def calculate_constant_capital(self, year: int, io_data: pd.DataFrame) -> float:
        """
        Calculate C* (Constant Capital) = Intermediate inputs (productive sectors)

        From book: C* = M'P = Materials inputs into production

        Args:
            year: Year to calculate
            io_data: BEA Input-Output intermediate inputs data

        Returns:
            C* in millions of dollars
        """

        # Filter to productive sectors only
        productive_data = io_data[
            io_data['naics_code'].map(
                lambda x: self.sector_mapping.get(x, 'unproductive') == 'productive'
            )
        ]

        # Sum intermediate inputs for productive sectors
        constant_capital = productive_data['intermediate_inputs'].sum()

        self.logger.info(f"C* ({year}): ${constant_capital:,.0f} million")
        return constant_capital

    def calculate_surplus_value(self, year: int, industry_data: pd.DataFrame) -> float:
        """
        Calculate S* (Surplus Value) = VA* - V*

        From book: S* = VA* - V* = surplus value (in money form)
        Alternative: S* = SP* = FP* - NP* = surplus product

        Args:
            year: Year to calculate
            industry_data: BEA industry accounts data

        Returns:
            S* in millions of dollars
        """

        # Filter to productive sectors only
        productive_data = industry_data[
            industry_data['naics_code'].map(
                lambda x: self.sector_mapping.get(x, 'unproductive') == 'productive'
            )
        ]

        # Calculate Marxian Value Added (VA*) - productive sectors only
        value_added_marxian = productive_data['gross_value_added'].sum()

        # Get Variable Capital (V*) for this year
        variable_capital = self.variable_capital.get(year, 0)

        # S* = VA* - V*
        surplus_value = value_added_marxian - variable_capital

        self.logger.info(f"S* ({year}): ${surplus_value:,.0f} million (VA*: ${value_added_marxian:,.0f}, V*: ${variable_capital:,.0f})")
        return surplus_value

    def calculate_profit_rate(self, year: int) -> float:
        """
        Calculate r* using Shaikh's exact formula: r* = S*/(C* + V*)

        Args:
            year: Year to calculate

        Returns:
            r* as decimal (e.g., 0.39 for 39%)
        """

        surplus_value = self.surplus_value.get(year, 0)
        constant_capital = self.constant_capital.get(year, 0)
        variable_capital = self.variable_capital.get(year, 0)

        if constant_capital + variable_capital == 0:
            self.logger.error(f"Cannot calculate r* for {year}: C* + V* = 0")
            return 0.0

        profit_rate = surplus_value / (constant_capital + variable_capital)

        self.logger.info(f"r* ({year}): {profit_rate:.4f} ({profit_rate*100:.1f}%)")
        return profit_rate

    def reconstruct_year(self, year: int) -> Dict[str, float]:
        """
        Reconstruct all Shaikh variables for a single year

        Args:
            year: Year to reconstruct

        Returns:
            Dictionary with S*, C*, V*, r* for the year
        """

        self.logger.info(f"Reconstructing Shaikh methodology for {year}")

        # Load modern data for this year
        industry_data = self.load_modern_industry_data(year)
        io_data = self.load_modern_io_data(year)

        # Calculate Shaikh variables using exact methodology
        self.variable_capital[year] = self.calculate_variable_capital(year, industry_data)
        self.constant_capital[year] = self.calculate_constant_capital(year, io_data)
        self.surplus_value[year] = self.calculate_surplus_value(year, industry_data)
        self.profit_rate[year] = self.calculate_profit_rate(year)

        results = {
            'year': year,
            'S_star': self.surplus_value[year],
            'C_star': self.constant_capital[year],
            'V_star': self.variable_capital[year],
            'r_star': self.profit_rate[year]
        }

        return results

    def load_modern_industry_data(self, year: int) -> pd.DataFrame:
        """
        Load modern BEA industry data for a specific year

        This is a placeholder - actual implementation would load from:
        - BEA Industry Economic Accounts
        - BLS Current Employment Statistics
        """

        # Placeholder: In real implementation, load actual BEA/BLS data
        self.logger.warning(f"Loading placeholder data for {year} - implement actual BEA/BLS data loading")

        # Return empty DataFrame for now
        return pd.DataFrame({
            'naics_code': [],
            'industry_name': [],
            'gross_value_added': [],
            'compensation_of_employees': []
        })

    def load_modern_io_data(self, year: int) -> pd.DataFrame:
        """
        Load modern BEA Input-Output data for a specific year

        This is a placeholder - actual implementation would load from:
        - BEA Input-Output Tables (5-year benchmarks with annual interpolation)
        """

        # Placeholder: In real implementation, load actual I-O data
        self.logger.warning(f"Loading placeholder I-O data for {year} - implement actual BEA I-O data loading")

        # Return empty DataFrame for now
        return pd.DataFrame({
            'naics_code': [],
            'industry_name': [],
            'intermediate_inputs': []
        })

    def reconstruct_modern_period(self, start_year: int = 1990, end_year: int = 2025) -> pd.DataFrame:
        """
        Reconstruct the entire modern period using Shaikh's methodology

        Args:
            start_year: First year to reconstruct (default 1990)
            end_year: Last year to reconstruct (default 2025)

        Returns:
            DataFrame with reconstructed Shaikh variables for all years
        """

        self.logger.info(f"Reconstructing modern period: {start_year}-{end_year}")

        # Load sector mapping
        self.load_sector_mapping()

        results = []

        for year in range(start_year, end_year + 1):
            try:
                year_results = self.reconstruct_year(year)
                results.append(year_results)
            except Exception as e:
                self.logger.error(f"Failed to reconstruct {year}: {e}")
                continue

        # Convert to DataFrame
        modern_series = pd.DataFrame(results)

        self.logger.info(f"Successfully reconstructed {len(results)} years using Shaikh methodology")

        return modern_series

    def validate_reconstruction(self, historical_data: pd.DataFrame, modern_data: pd.DataFrame) -> Dict[str, float]:
        """
        Validate the reconstruction by checking consistency and transition smoothness

        Args:
            historical_data: Original book data (1958-1989)
            modern_data: Reconstructed modern data (1990-2025)

        Returns:
            Validation metrics
        """

        self.logger.info("Validating reconstruction against historical methodology")

        # Check 1989-1990 transition
        r_1989 = historical_data[historical_data['year'] == 1989]['r_star'].iloc[0] if not historical_data.empty else 0
        r_1990 = modern_data[modern_data['year'] == 1990]['r_star'].iloc[0] if not modern_data.empty else 0

        transition_ratio = abs(r_1989 - r_1990) / r_1989 if r_1989 != 0 else float('inf')

        # Calculate trend consistency
        historical_trend = historical_data['r_star'].iloc[-5:].mean() if len(historical_data) >= 5 else 0
        modern_trend = modern_data['r_star'].iloc[:5].mean() if len(modern_data) >= 5 else 0

        validation_results = {
            'transition_discontinuity': transition_ratio,
            'historical_final_rate': r_1989,
            'modern_initial_rate': r_1990,
            'historical_trend': historical_trend,
            'modern_trend': modern_trend,
            'methodology_consistent': transition_ratio < 0.5  # Less than 50% change
        }

        self.logger.info(f"Validation results: {validation_results}")

        return validation_results

    def create_unified_series(self, historical_data: pd.DataFrame, modern_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create the final unified 1958-2025 series using consistent Shaikh methodology

        Args:
            historical_data: Book data (1958-1989)
            modern_data: Reconstructed data (1990-2025)

        Returns:
            Unified 67-year DataFrame with consistent r* = S*/(C* + V*) methodology
        """

        self.logger.info("Creating unified 67-year series with consistent Shaikh methodology")

        # Ensure consistent column names
        historical_clean = historical_data[['year', 'S_star', 'C_star', 'V_star', 'r_star']].copy()
        modern_clean = modern_data[['year', 'S_star', 'C_star', 'V_star', 'r_star']].copy()

        # Combine the series
        unified_series = pd.concat([historical_clean, modern_clean], ignore_index=True)
        unified_series = unified_series.sort_values('year').reset_index(drop=True)

        # Add metadata
        unified_series['methodology'] = 'Shaikh_1994'
        unified_series['formula'] = 'r_star = S_star / (C_star + V_star)'
        unified_series['data_source'] = unified_series['year'].apply(
            lambda x: 'Book_Table_5.4' if x <= 1989 else 'BEA_BLS_Reconstructed'
        )

        self.logger.info(f"Created unified series: {len(unified_series)} years (1958-2025)")

        return unified_series

def main():
    """
    Main function to demonstrate the reconstruction process
    """

    # Initialize the reconstructor
    reconstructor = ShaikhMethodologyReconstructor(
        data_path="../../data/modern",
        config_path="../../config"
    )

    print("Shaikh & Tonak Methodology Reconstructor")
    print("=" * 50)
    print("OBJECTIVE: Reconstruct modern data using exact 1994 book methodology")
    print("FORMULA: r* = S*/(C* + V*)")
    print("PERIOD: 1990-2025")
    print()

    # Reconstruct modern period
    modern_data = reconstructor.reconstruct_modern_period(1990, 2025)

    # Note: In actual implementation, would load historical data from book
    # For demonstration, create placeholder historical data
    historical_data = pd.DataFrame({
        'year': range(1958, 1990),
        'S_star': [100] * 32,  # Placeholder values
        'C_star': [200] * 32,
        'V_star': [50] * 32,
        'r_star': [0.4] * 32
    })

    # Validate reconstruction
    validation = reconstructor.validate_reconstruction(historical_data, modern_data)

    # Create unified series
    unified_series = reconstructor.create_unified_series(historical_data, modern_data)

    print(f"Reconstruction complete!")
    print(f"Unified series: {len(unified_series)} years")
    print(f"Validation: {'PASS' if validation['methodology_consistent'] else 'FAIL'}")

if __name__ == "__main__":
    main()