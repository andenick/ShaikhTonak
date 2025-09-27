"""
Phase 2 Data Integration: Complete S&T Extension to Present Day
Integrates all collected data sources into unified 1958-2025 time series

This script combines:
1. Historical S&T data (1958-1989) - Phase 1 replication
2. Corporate profits (1990-2024) - BEA NIPA A939RC
3. KLEMS S&T variables (1997-2023) - BEA-BLS industry accounts
4. Capacity utilization (1990-2025) - Federal Reserve G.17

Output: Complete S&T time series ready for profit rate analysis
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase2DataIntegrator:
    def __init__(self):
        """Initialize the Phase 2 data integration system."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.output_dir = self.base_dir / "data" / "modern" / "integrated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data source paths
        self.historical_dir = self.base_dir / "data" / "historical" / "processed"
        self.corporate_profits_file = self.base_dir / "data" / "modern" / "bea_nipa" / "corporate_profits_1990_2024_extracted.csv"
        self.klems_dir = self.base_dir / "data" / "modern" / "klems_processed"
        self.capacity_dir = self.base_dir / "data" / "modern" / "fed_capacity"
        self.fixed_assets_k_file = self.base_dir / "data" / "modern" / "processed" / "bea_fixed_assets" / "private_net_stock_current_cost.csv"
        # Optional modern SP (S&T-consistent) if staged separately
        self.modern_sp_file = self.base_dir / "data" / "modern" / "bea_nipa" / "modern_sp_st_consistent_1990_2025.csv"

        logger.info(f"Phase 2 Data Integrator initialized")
        logger.info(f"Target: Complete 1958-2025 S&T time series")

    def load_historical_data(self):
        """Load Phase 1 historical S&T data (1958-1989)."""
        logger.info("Loading historical S&T data (1958-1989)...")

        # Look for the best historical data file
        historical_files = [
            "complete_analysis_summary.csv",
            "marxian_variables_calculated.csv",
            "perfect_replication_results.csv"
        ]

        historical_data = None
        for filename in historical_files:
            file_path = self.historical_dir / filename
            if file_path.exists():
                try:
                    historical_data = pd.read_csv(file_path)
                    logger.info(f"Loaded historical data from {filename}")
                    logger.info(f"Historical period: {historical_data['year'].min()}-{historical_data['year'].max()}")
                    logger.info(f"Historical variables: {list(historical_data.columns)}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load {filename}: {e}")

        if historical_data is None:
            logger.error("No historical data found!")
            return None

        return historical_data

    def load_corporate_profits(self):
        """Load corporate profits data (1990-2024)."""
        logger.info("Loading corporate profits data (1990-2024)...")

        try:
            profits_data = pd.read_csv(self.corporate_profits_file)
            logger.info(f"Loaded corporate profits: {len(profits_data)} years")
            logger.info(f"Profits period: {profits_data['year'].min()}-{profits_data['year'].max()}")
            return profits_data
        except Exception as e:
            logger.error(f"Failed to load corporate profits: {e}")
            return None

    def load_klems_data(self):
        """Load KLEMS S&T variables (1997-2023)."""
        logger.info("Loading KLEMS S&T data (1997-2023)...")

        klems_files = {
            'capital': 'st_capital_stock_1997_2023.csv',
            'surplus': 'st_surplus_1997_2023.csv',
            'gross_output': 'st_gross_output_1997_2023.csv',
            'value_added': 'st_value_added_1997_2023.csv',
            'labor_hours': 'st_labor_hours_1997_2023.csv',
            'labor_compensation_col': 'st_labor_compensation_col_1997_2023.csv',
            'labor_compensation_nocol': 'st_labor_compensation_nocol_1997_2023.csv'
        }

        klems_data = {}
        for var_name, filename in klems_files.items():
            file_path = self.klems_dir / filename
            if file_path.exists():
                try:
                    data = pd.read_csv(file_path)
                    klems_data[var_name] = data
                    logger.info(f"Loaded KLEMS {var_name}: {len(data)} observations")
                except Exception as e:
                    logger.warning(f"Failed to load KLEMS {var_name}: {e}")

        logger.info(f"KLEMS variables loaded: {list(klems_data.keys())}")
        return klems_data

    def load_capacity_utilization(self):
        """Load capacity utilization data (1990-2025)."""
        logger.info("Loading capacity utilization data (1990-2025)...")

        # Find the best available capacity utilization series
        capacity_files = [
            'capacity_utilization_CAPUTLG331S_annual_1990_2025.csv',  # Primary Metal Industries
            'capacity_utilization_CAPUTLG3311A2S_annual_1990_2025.csv',  # Alternative Primary Metal
            'capacity_utilization_CAPUTLG321S_annual_1990_2025.csv'  # Wood Products
        ]

        capacity_data = None
        for filename in capacity_files:
            file_path = self.capacity_dir / filename
            if file_path.exists():
                try:
                    capacity_data = pd.read_csv(file_path)
                    logger.info(f"Using capacity utilization from {filename}")
                    logger.info(f"Capacity period: {capacity_data['year'].min()}-{capacity_data['year'].max()}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load {filename}: {e}")

        if capacity_data is None:
            logger.error("No capacity utilization data found!")
            return None

        return capacity_data

    def load_modern_k(self):
        """Load modern K from processed BEA Fixed Assets (private net stock, current-cost)."""
        logger.info("Loading modern K (S&T-consistent) from BEA Fixed Assets…")
        if not self.fixed_assets_k_file.exists():
            logger.warning(f"Modern K file missing: {self.fixed_assets_k_file}")
            return None
        try:
            k_df = pd.read_csv(self.fixed_assets_k_file)
            if 'year' not in k_df.columns or 'modern_K_st_consistent' not in k_df.columns:
                raise ValueError("K file must have columns: year, modern_K_st_consistent")
            logger.info(f"Loaded modern K: {k_df['year'].min()}-{k_df['year'].max()} ({len(k_df)} rows)")
            return k_df
        except Exception as e:
            logger.error(f"Failed to load modern K: {e}")
            return None

    def load_modern_sp(self):
        """Optionally load modern SP if a staged S&T-consistent file exists."""
        if not self.modern_sp_file.exists():
            logger.info("Modern SP (S&T-consistent) not staged yet; proceeding without it.")
            return None
        try:
            sp_df = pd.read_csv(self.modern_sp_file)
            # Expect columns: year, modern_SP_st_consistent
            if 'year' not in sp_df.columns or 'modern_SP_st_consistent' not in sp_df.columns:
                raise ValueError("SP file must have columns: year, modern_SP_st_consistent")
            logger.info(f"Loaded modern SP: {sp_df['year'].min()}-{sp_df['year'].max()} ({len(sp_df)} rows)")
            return sp_df
        except Exception as e:
            logger.error(f"Failed to load modern SP: {e}")
            return None

    def aggregate_klems_to_annual(self, klems_data):
        """Aggregate KLEMS industry data to economy-wide annual totals."""
        logger.info("Aggregating KLEMS data to economy-wide annual totals...")

        aggregated = {}

        for var_name, data in klems_data.items():
            if 'Year' in data.columns:
                # Sum by year across all industries
                annual_totals = data.groupby('Year').agg({
                    'Value': 'sum'
                }).reset_index()
                annual_totals = annual_totals.rename(columns={'Year': 'year', 'Value': var_name})
                aggregated[var_name] = annual_totals
                logger.info(f"Aggregated {var_name}: {len(annual_totals)} years")

        return aggregated

    def create_integrated_time_series(self):
        """Create the complete integrated 1958-2025 time series."""
        logger.info("Creating integrated 1958-2025 time series...")

        # Load all data sources
        historical_data = self.load_historical_data()
        corporate_profits = self.load_corporate_profits()
        klems_data = self.load_klems_data()
        capacity_data = self.load_capacity_utilization()
        modern_k = self.load_modern_k()
        modern_sp = self.load_modern_sp()

        # Validate required data sources (KLEMS and modern series are optional)
        if not all([
            historical_data is not None,
            corporate_profits is not None,
            capacity_data is not None
        ]):
            logger.error("Missing required core data sources (historical, corporate profits, or capacity utilization)!")
            return None

        # Aggregate KLEMS to annual totals (optional)
        klems_aggregated = {}
        if klems_data:
            klems_aggregated = self.aggregate_klems_to_annual(klems_data)

        # Create master time series (1958-2025)
        years = list(range(1958, 2026))
        integrated_data = pd.DataFrame({'year': years})

        # Add historical data (1958-1989)
        if 'year' in historical_data.columns:
            historical_subset = historical_data[historical_data['year'] <= 1989]
            integrated_data = integrated_data.merge(historical_subset, on='year', how='left')
            logger.info(f"Added historical data: {len(historical_subset)} years")

        # Add corporate profits (1990-2024)
        profits_subset = corporate_profits.rename(columns={'value': 'corporate_profits'})
        integrated_data = integrated_data.merge(profits_subset[['year', 'corporate_profits']],
                                              on='year', how='left')
        logger.info(f"Added corporate profits: {len(profits_subset)} years")

        # Add capacity utilization (1990-2025)
        capacity_subset = capacity_data.rename(columns={'value': 'capacity_utilization'})
        integrated_data = integrated_data.merge(capacity_subset[['year', 'capacity_utilization']],
                                              on='year', how='left')
        logger.info(f"Added capacity utilization: {len(capacity_subset)} years")

        # Add KLEMS variables (1997-2023) if present
        if klems_aggregated:
            for var_name, var_data in klems_aggregated.items():
                col_name = f'klems_{var_name}'
                integrated_data = integrated_data.merge(
                    var_data.rename(columns={var_name: col_name}),
                    on='year', how='left'
                )
                logger.info(f"Added KLEMS {var_name}: {len(var_data)} years")

        # Add modern K (S&T-consistent) if available
        if modern_k is not None:
            k_cols = ['modern_K_st_consistent']
            if 'modern_K_st_consistent_norm' in modern_k.columns:
                k_cols.append('modern_K_st_consistent_norm')
            integrated_data = integrated_data.merge(modern_k[['year'] + k_cols], on='year', how='left')
            logger.info("Added modern_K_st_consistent (+ normalized variant when available) from BEA Fixed Assets")

        # Add modern SP (S&T-consistent) if available
        if modern_sp is not None:
            sp_cols = ['modern_SP_st_consistent']
            if 'modern_SP_st_consistent_norm' in modern_sp.columns:
                sp_cols.append('modern_SP_st_consistent_norm')
            integrated_data = integrated_data.merge(modern_sp[['year'] + sp_cols], on='year', how='left')
            logger.info("Added modern_SP_st_consistent (+ normalized variant when available) from staged BEA NIPA construction")

        # Calculate data coverage
        total_years = len(integrated_data)
        coverage_stats = {}
        for col in integrated_data.columns:
            if col != 'year':
                non_null_count = integrated_data[col].notna().sum()
                coverage_stats[col] = f"{non_null_count}/{total_years} ({non_null_count/total_years*100:.1f}%)"

        logger.info("Data coverage summary:")
        for var, coverage in coverage_stats.items():
            logger.info(f"  {var}: {coverage}")

        return integrated_data

    def save_integrated_data(self, integrated_data):
        """Save the integrated time series."""
        if integrated_data is None:
            logger.error("No data to save")
            return False

        # Save main integrated dataset
        main_file = self.output_dir / "complete_st_timeseries_1958_2025.csv"
        integrated_data.to_csv(main_file, index=False)
        logger.info(f"Integrated time series saved: {main_file}")

        # Save metadata
        # Known units for key variables (best-known defaults)
        units = {
            'year': 'year',
            'corporate_profits': 'Millions of dollars (NIPA A939RC)',
            'capacity_utilization': 'Percent (0-100, Fed G.17 annualized)',
            'modern_K_st_consistent': 'Millions of current dollars (BEA Fixed Assets, net stock, current-cost, private)',
            'modern_K_st_consistent_norm': 'Millions of current dollars (normalized to match SP scope; identical to raw unless noted)',
            'modern_SP_st_consistent': 'Millions of current dollars (constructed from NIPA: Business NDP minus compensation)',
            'modern_SP_st_consistent_norm': 'Millions of current dollars (normalized to match K scope; identical to raw unless noted)',
        }

        metadata = {
            'integration_date': datetime.now().isoformat(),
            'period_coverage': '1958-2025',
            'total_years': len(integrated_data),
            'data_sources': {
                'historical_st': '1958-1989 (Phase 1)',
                'corporate_profits': '1990-2024 (BEA NIPA A939RC)',
                'klems_variables': '1997-2023 (BEA-BLS Industry Accounts)',
                'capacity_utilization': '1990-2025 (Federal Reserve G.17)'
            },
            'variables_included': list(integrated_data.columns),
            'units': {col: units.get(col) for col in integrated_data.columns},
            'data_completeness': {}
        }

        # Add completeness stats
        for col in integrated_data.columns:
            if col != 'year':
                non_null_count = integrated_data[col].notna().sum()
                total_count = len(integrated_data)
                metadata['data_completeness'][col] = {
                    'available_years': int(non_null_count),
                    'total_years': int(total_count),
                    'coverage_percentage': round(non_null_count/total_count*100, 1)
                }

        metadata_file = self.output_dir / "integration_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved: {metadata_file}")

        return True

    def run_integration(self):
        """Run the complete Phase 2 data integration."""
        logger.info("="*60)
        logger.info("STARTING PHASE 2 DATA INTEGRATION")
        logger.info("Target: Complete Shaikh & Tonak Extension 1958-2025")
        logger.info("="*60)

        try:
            # Create integrated time series
            integrated_data = self.create_integrated_time_series()

            if integrated_data is not None:
                # Save results
                success = self.save_integrated_data(integrated_data)

                if success:
                    logger.info("="*60)
                    logger.info("✅ PHASE 2 DATA INTEGRATION COMPLETE")
                    logger.info(f"Complete time series: 1958-2025 ({len(integrated_data)} years)")
                    logger.info("Ready for profit rate calculation and analysis")
                    logger.info("="*60)
                    return True
                else:
                    logger.error("Failed to save integrated data")
                    return False
            else:
                logger.error("Failed to create integrated time series")
                return False

        except Exception as e:
            logger.error(f"Integration failed: {e}")
            return False

def main():
    """Main execution function."""
    integrator = Phase2DataIntegrator()
    success = integrator.run_integration()

    if success:
        print("\nSUCCESS: PHASE 2 DATA INTEGRATION COMPLETE")
        print("Complete S&T time series (1958-2025) ready for analysis!")
        print("Next step: Profit rate calculation and validation")
    else:
        print("\nFAILED: PHASE 2 DATA INTEGRATION")
        print("Check logs for details")

if __name__ == "__main__":
    main()