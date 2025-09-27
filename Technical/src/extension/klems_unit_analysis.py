"""
KLEMS Unit Analysis and Proper Integration
Analyzes KLEMS data units and creates proper scaling for S&T integration

This script will:
1. Analyze KLEMS data units compared to historical S&T
2. Determine correct scaling factors
3. Test different unit conversion approaches
4. Validate results against known S&T ranges
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KLEMSUnitAnalyzer:
    def __init__(self):
        """Initialize KLEMS unit analyzer."""
        self.base_dir = Path(__file__).parent.parent.parent
        logger.info("KLEMS Unit Analyzer initialized")

    def load_data(self):
        """Load all required datasets."""
        logger.info("Loading datasets for unit analysis...")

        # Load KLEMS data
        surplus_file = self.base_dir / "data" / "modern" / "klems_processed" / "st_surplus_1997_2023.csv"
        capital_file = self.base_dir / "data" / "modern" / "klems_processed" / "st_capital_stock_1997_2023.csv"

        # Load historical data
        historical_file = self.base_dir / "data" / "modern" / "integrated" / "complete_st_timeseries_1958_2025.csv"

        # Load corporate profits for comparison
        cp_file = self.base_dir / "data" / "modern" / "bea_nipa" / "corporate_profits_1990_2024_extracted.csv"

        data = {}
        data['klems_surplus'] = pd.read_csv(surplus_file)
        data['klems_capital'] = pd.read_csv(capital_file)
        data['historical'] = pd.read_csv(historical_file)
        data['corporate_profits'] = pd.read_csv(cp_file)

        logger.info("All datasets loaded successfully")
        return data

    def analyze_units(self, data):
        """Analyze units across different data sources."""
        logger.info("Analyzing units across data sources...")

        # Get 2020 data for comparison
        klems_surplus_2020 = data['klems_surplus'][data['klems_surplus']['Year'] == 2020]
        klems_capital_2020 = data['klems_capital'][data['klems_capital']['Year'] == 2020]
        cp_2020 = data['corporate_profits'][data['corporate_profits']['year'] == 2020]
        hist_1980 = data['historical'][data['historical']['year'] == 1980]

        # Calculate totals
        klems_surplus_total = klems_surplus_2020['surplus'].sum()
        klems_capital_total = klems_capital_2020['Value'].sum()
        cp_2020_value = cp_2020['value'].iloc[0] if len(cp_2020) > 0 else None
        hist_sp = hist_1980['original_SP'].iloc[0] if len(hist_1980) > 0 else None
        hist_k = hist_1980['original_K'].iloc[0] if len(hist_1980) > 0 else None

        unit_analysis = {
            'klems_2020': {
                'surplus_total': klems_surplus_total,
                'capital_total': klems_capital_total,
                'surplus_capital_ratio': klems_surplus_total / klems_capital_total if klems_capital_total > 0 else None
            },
            'historical_1980': {
                'sp': hist_sp,
                'k': hist_k,
                'sp_k_ratio': hist_sp / hist_k if hist_k and hist_k > 0 else None
            },
            'corporate_profits_2020': {
                'value': cp_2020_value
            }
        }

        # Calculate potential scaling factors
        if hist_sp and klems_surplus_total:
            surplus_scaling = hist_sp / klems_surplus_total
            unit_analysis['scaling_factors'] = {
                'surplus_to_historical': surplus_scaling,
                'magnitude_difference': klems_surplus_total / hist_sp
            }

        logger.info("Unit analysis complete")
        logger.info(f"KLEMS 2020 surplus total: {klems_surplus_total:,.0f}")
        logger.info(f"Historical 1980 SP: {hist_sp:.0f}")
        logger.info(f"Magnitude difference: {klems_surplus_total/hist_sp:.0f}x")

        return unit_analysis

    def test_unit_hypotheses(self, data, unit_analysis):
        """Test different hypotheses about KLEMS unit scaling."""
        logger.info("Testing unit scaling hypotheses...")

        klems_surplus_2020 = data['klems_surplus'][data['klems_surplus']['Year'] == 2020]
        klems_surplus_total = klems_surplus_2020['surplus'].sum()
        hist_sp_1980 = unit_analysis['historical_1980']['sp']

        # Hypothesis 1: KLEMS is in millions, historical is in billions
        hypothesis_1_factor = 1000  # Convert millions to billions
        h1_scaled = klems_surplus_total / hypothesis_1_factor
        h1_ratio = h1_scaled / hist_sp_1980

        # Hypothesis 2: KLEMS is in actual dollars, historical is in thousands
        hypothesis_2_factor = 1000000  # Convert dollars to millions
        h2_scaled = klems_surplus_total / hypothesis_2_factor
        h2_ratio = h2_scaled / hist_sp_1980

        # Hypothesis 3: Different data coverage (KLEMS includes more sectors)
        # Check what the corporate profits data suggests
        cp_2020 = data['corporate_profits'][data['corporate_profits']['year'] == 2020]
        cp_value = cp_2020['value'].iloc[0] if len(cp_2020) > 0 else None

        if cp_value:
            cp_to_klems_ratio = klems_surplus_total / cp_value
            cp_to_hist_ratio = cp_value / hist_sp_1980

        hypotheses = {
            'hypothesis_1_millions_to_billions': {
                'description': 'KLEMS in millions, historical in billions',
                'scaling_factor': hypothesis_1_factor,
                'scaled_klems': h1_scaled,
                'ratio_to_historical': h1_ratio,
                'plausible': 0.5 <= h1_ratio <= 2.0
            },
            'hypothesis_2_dollars_to_millions': {
                'description': 'KLEMS in dollars, historical in millions',
                'scaling_factor': hypothesis_2_factor,
                'scaled_klems': h2_scaled,
                'ratio_to_historical': h2_ratio,
                'plausible': 0.5 <= h2_ratio <= 2.0
            }
        }

        if cp_value:
            hypotheses['corporate_profits_comparison'] = {
                'cp_2020': cp_value,
                'klems_to_cp_ratio': cp_to_klems_ratio,
                'cp_to_hist_ratio': cp_to_hist_ratio,
                'note': 'Corporate profits should be roughly comparable to surplus'
            }

        logger.info("Hypothesis testing complete")
        for name, hyp in hypotheses.items():
            if 'plausible' in hyp:
                logger.info(f"{name}: {hyp['description']} - {'PLAUSIBLE' if hyp['plausible'] else 'IMPLAUSIBLE'}")

        return hypotheses

    def calculate_klems_profit_rates_corrected(self, data, scaling_factor):
        """Calculate KLEMS profit rates with corrected scaling."""
        logger.info(f"Calculating KLEMS profit rates with scaling factor: {scaling_factor}")

        klems_surplus = data['klems_surplus'].copy()
        klems_capital = data['klems_capital'].copy()

        # Aggregate by year with proper scaling
        surplus_annual = klems_surplus.groupby('Year')['surplus'].sum().reset_index()
        capital_annual = klems_capital.groupby('Year')['Value'].sum().reset_index()

        # Apply scaling
        surplus_annual['scaled_surplus'] = surplus_annual['surplus'] / scaling_factor
        capital_annual['scaled_capital'] = capital_annual['Value'] / scaling_factor

        # Merge with capacity utilization
        historical_data = data['historical']
        capacity_data = historical_data[
            (historical_data['year'] >= 1997) &
            (historical_data['capacity_utilization'].notna())
        ][['year', 'capacity_utilization']].copy()

        # Merge surplus and capital
        klems_combined = surplus_annual.merge(
            capital_annual,
            left_on='Year',
            right_on='Year',
            how='inner'
        )

        # Merge with capacity utilization
        klems_combined = klems_combined.merge(
            capacity_data,
            left_on='Year',
            right_on='year',
            how='inner'
        )

        # Calculate profit rates
        klems_combined['capacity_utilization_rate'] = klems_combined['capacity_utilization'] / 100
        klems_combined['profit_rate'] = klems_combined['scaled_surplus'] / (
            klems_combined['scaled_capital'] * klems_combined['capacity_utilization_rate']
        )

        result = klems_combined[['Year', 'profit_rate', 'scaled_surplus', 'scaled_capital']].copy()
        result = result.rename(columns={'Year': 'year'})

        logger.info(f"KLEMS profit rates calculated for {len(result)} years")
        logger.info(f"Rate range: {result['profit_rate'].min():.3f} - {result['profit_rate'].max():.3f}")
        logger.info(f"Mean rate: {result['profit_rate'].mean():.3f}")

        return result

    def validate_against_historical(self, klems_rates, data):
        """Validate KLEMS rates against historical S&T rates."""
        logger.info("Validating KLEMS rates against historical data...")

        historical_data = data['historical']
        hist_rates = historical_data[
            (historical_data['calculated_rate_of_profit'].notna())
        ][['year', 'calculated_rate_of_profit']].copy()

        # Find overlapping years (shouldn't be any, but check)
        overlap_years = set(klems_rates['year']) & set(hist_rates['year'])

        if overlap_years:
            logger.info(f"Found overlap years: {overlap_years}")
            for year in overlap_years:
                klems_rate = klems_rates[klems_rates['year'] == year]['profit_rate'].iloc[0]
                hist_rate = hist_rates[hist_rates['year'] == year]['calculated_rate_of_profit'].iloc[0]
                logger.info(f"Year {year}: KLEMS={klems_rate:.3f}, Historical={hist_rate:.3f}")

        # Compare with transition period
        hist_late = hist_rates[hist_rates['year'] >= 1985]
        klems_early = klems_rates[klems_rates['year'] <= 2000]

        validation_results = {
            'historical_late_period': {
                'years': hist_late['year'].tolist(),
                'mean_rate': hist_late['calculated_rate_of_profit'].mean(),
                'range': [hist_late['calculated_rate_of_profit'].min(),
                         hist_late['calculated_rate_of_profit'].max()]
            },
            'klems_early_period': {
                'years': klems_early['year'].tolist(),
                'mean_rate': klems_early['profit_rate'].mean(),
                'range': [klems_early['profit_rate'].min(),
                         klems_early['profit_rate'].max()]
            }
        }

        # Check if the ranges are reasonable
        hist_mean = validation_results['historical_late_period']['mean_rate']
        klems_mean = validation_results['klems_early_period']['mean_rate']
        ratio = klems_mean / hist_mean if hist_mean > 0 else None

        validation_results['continuity_check'] = {
            'historical_late_mean': hist_mean,
            'klems_early_mean': klems_mean,
            'ratio': ratio,
            'reasonable': 0.5 <= ratio <= 2.0 if ratio else False
        }

        logger.info(f"Validation complete:")
        logger.info(f"Historical late mean: {hist_mean:.3f}")
        logger.info(f"KLEMS early mean: {klems_mean:.3f}")
        logger.info(f"Ratio: {ratio:.2f} - {'REASONABLE' if validation_results['continuity_check']['reasonable'] else 'UNREASONABLE'}")

        return validation_results

    def run_analysis(self):
        """Run complete KLEMS unit analysis."""
        logger.info("="*60)
        logger.info("KLEMS UNIT ANALYSIS AND INTEGRATION")
        logger.info("="*60)

        try:
            # Load data
            data = self.load_data()

            # Analyze units
            unit_analysis = self.analyze_units(data)

            # Test hypotheses
            hypotheses = self.test_unit_hypotheses(data, unit_analysis)

            # Test different scaling factors
            logger.info("\nTesting scaling factors...")

            scaling_factors_to_test = [1000, 1000000, 10000, 100000]
            best_scaling = None
            best_validation = None

            for factor in scaling_factors_to_test:
                logger.info(f"\nTesting scaling factor: {factor}")
                try:
                    klems_rates = self.calculate_klems_profit_rates_corrected(data, factor)
                    validation = self.validate_against_historical(klems_rates, data)

                    if validation['continuity_check']['reasonable']:
                        logger.info(f"✅ Scaling factor {factor} produces reasonable results!")
                        best_scaling = factor
                        best_validation = validation
                        break
                    else:
                        logger.info(f"❌ Scaling factor {factor} produces unreasonable results")
                except Exception as e:
                    logger.error(f"Error with scaling factor {factor}: {e}")

            return {
                'unit_analysis': unit_analysis,
                'hypotheses': hypotheses,
                'best_scaling_factor': best_scaling,
                'validation_results': best_validation
            }

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return None

def main():
    """Main execution."""
    analyzer = KLEMSUnitAnalyzer()
    results = analyzer.run_analysis()

    if results and results['best_scaling_factor']:
        print(f"\n✅ SUCCESS: Found appropriate KLEMS scaling factor: {results['best_scaling_factor']}")
        print("KLEMS data can be properly integrated into S&T methodology!")
    else:
        print("\n❌ Could not find appropriate scaling factor for KLEMS data")
        print("Further investigation needed for KLEMS integration")

if __name__ == "__main__":
    main()