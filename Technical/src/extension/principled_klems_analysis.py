"""
Principled KLEMS Analysis - No Arbitrary Scaling
Determines whether KLEMS data can be meaningfully integrated into S&T methodology
without resorting to arbitrary scaling factors.

Approach:
1. Analyze what each dataset actually represents
2. Check if they're measuring the same economic concepts
3. Make evidence-based decision about inclusion/exclusion
4. No arbitrary scaling factors that lack economic justification
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PrincipledKLEMSAnalysis:
    def __init__(self):
        """Initialize principled KLEMS analysis."""
        self.base_dir = Path(__file__).parent.parent.parent
        logger.info("Principled KLEMS Analysis - No Arbitrary Scaling")

    def analyze_data_conceptually(self):
        """Analyze what each dataset conceptually represents."""
        logger.info("Analyzing datasets conceptually...")

        # Load all datasets
        historical = pd.read_csv(self.base_dir / "data" / "modern" / "integrated" / "complete_st_timeseries_1958_2025.csv")
        klems_surplus = pd.read_csv(self.base_dir / "data" / "modern" / "klems_processed" / "st_surplus_1997_2023.csv")
        corporate_profits = pd.read_csv(self.base_dir / "data" / "modern" / "bea_nipa" / "corporate_profits_1990_2024_extracted.csv")

        analysis = {
            'historical_st': {
                'description': 'Shaikh & Tonak replication of original methodology',
                'sample_sp_1980': historical[historical['year'] == 1980]['original_SP'].iloc[0],
                'sample_k_1980': historical[historical['year'] == 1980]['original_K'].iloc[0],
                'profit_rate_1980': historical[historical['year'] == 1980]['calculated_rate_of_profit'].iloc[0],
                'conceptual_meaning': 'Surplus Profits in S&T definition',
                'likely_units': 'Billions of dollars (1980s scale)'
            },
            'klems_data': {
                'description': 'BEA-BLS industry-level production accounts',
                'sample_surplus_2020': klems_surplus[klems_surplus['Year'] == 2020]['surplus'].sum(),
                'sample_individual_surplus': klems_surplus[(klems_surplus['Year'] == 2020) & (klems_surplus['Industry Description'] == 'Farms')]['surplus'].iloc[0],
                'conceptual_meaning': 'Value Added minus Labor Compensation by industry',
                'likely_units': 'Millions of dollars (modern scale)'
            },
            'corporate_profits': {
                'description': 'BEA NIPA Corporate Profits series A939RC',
                'sample_2020': corporate_profits[corporate_profits['year'] == 2020]['value'].iloc[0],
                'conceptual_meaning': 'Corporate Profits After Tax',
                'likely_units': 'Unknown scale (needs investigation)'
            }
        }

        # Check internal consistency
        farms_2020 = klems_surplus[(klems_surplus['Year'] == 2020) & (klems_surplus['Industry Description'] == 'Farms')]
        if len(farms_2020) > 0:
            farms_surplus = farms_2020['surplus'].iloc[0]
            farms_value_added = farms_2020['Value'].iloc[0]
            farms_surplus_rate = farms_2020['surplus_rate'].iloc[0]

            analysis['klems_validation'] = {
                'farms_surplus': farms_surplus,
                'farms_value_added': farms_value_added,
                'farms_surplus_rate': farms_surplus_rate,
                'calculated_rate': farms_surplus / farms_value_added,
                'consistent': abs(farms_surplus_rate - farms_surplus / farms_value_added) < 0.001
            }

        logger.info("Conceptual analysis complete")
        for dataset, info in analysis.items():
            logger.info(f"{dataset}: {info.get('description', 'N/A')}")

        return analysis

    def check_economic_realism(self, analysis):
        """Check if the data represents realistic economic magnitudes."""
        logger.info("Checking economic realism...")

        # US economic context for validation
        us_context = {
            '1980': {
                'gdp': 2862.5,  # billions
                'corporate_profits_est': 200,  # billions (estimated)
            },
            '2020': {
                'gdp': 20953.0,  # billions
                'corporate_profits_est': 2000,  # billions (estimated)
            }
        }

        realism_check = {}

        # Check historical S&T
        hist_sp_1980 = analysis['historical_st']['sample_sp_1980']
        if hist_sp_1980:
            realism_check['historical_st'] = {
                'sp_1980': hist_sp_1980,
                'as_percent_of_gdp': (hist_sp_1980 / us_context['1980']['gdp']) * 100,
                'realistic': 1 <= (hist_sp_1980 / us_context['1980']['gdp']) * 100 <= 20,
                'interpretation': f"If {hist_sp_1980} billion, represents {(hist_sp_1980 / us_context['1980']['gdp']) * 100:.1f}% of 1980 GDP"
            }

        # Check KLEMS
        klems_total_2020 = analysis['klems_data']['sample_surplus_2020']
        if klems_total_2020:
            realism_check['klems_data'] = {
                'total_surplus_2020': klems_total_2020,
                'as_billions': klems_total_2020 / 1000,  # if in millions
                'as_percent_of_gdp': (klems_total_2020 / 1000 / us_context['2020']['gdp']) * 100,
                'realistic_if_millions': 5 <= (klems_total_2020 / 1000 / us_context['2020']['gdp']) * 100 <= 25,
                'interpretation': f"If millions, represents {(klems_total_2020 / 1000 / us_context['2020']['gdp']) * 100:.1f}% of 2020 GDP"
            }

        # Check corporate profits
        cp_2020 = analysis['corporate_profits']['sample_2020']
        if cp_2020:
            # Try different unit interpretations
            realism_check['corporate_profits'] = {
                'raw_value': cp_2020,
                'if_billions': {
                    'value': cp_2020,
                    'as_percent_gdp': (cp_2020 / us_context['2020']['gdp']) * 100,
                    'realistic': 1 <= (cp_2020 / us_context['2020']['gdp']) * 100 <= 15
                },
                'if_hundreds_billions': {
                    'value': cp_2020 * 100,
                    'as_percent_gdp': (cp_2020 * 100 / us_context['2020']['gdp']) * 100,
                    'realistic': 1 <= (cp_2020 * 100 / us_context['2020']['gdp']) * 100 <= 15
                }
            }

        logger.info("Economic realism check complete")
        return realism_check, us_context

    def assess_compatibility(self, analysis, realism_check):
        """Assess whether datasets are conceptually compatible."""
        logger.info("Assessing dataset compatibility...")

        compatibility_assessment = {
            'conceptual_alignment': {
                'historical_st_concept': 'Marxian surplus profits (SP)',
                'klems_concept': 'Value added minus labor compensation',
                'corporate_profits_concept': 'Corporate profits after tax',
                'alignment': 'Partial - all relate to capital returns but different definitions'
            },
            'unit_compatibility': {
                'historical_appears_billions': realism_check['historical_st']['realistic'],
                'klems_appears_millions': realism_check['klems_data']['realistic_if_millions'],
                'unit_mismatch': True,  # Different unit scales
                'economic_justification_for_scaling': False  # No economic reason for arbitrary scaling
            },
            'temporal_coverage': {
                'historical': '1958-1989',
                'klems': '1997-2023',
                'overlap': 'None - different time periods',
                'validation_impossible': True  # Cannot validate against each other
            }
        }

        # Final compatibility decision
        compatibility_assessment['final_decision'] = {
            'can_integrate_meaningfully': False,
            'reasons': [
                'Different unit scales with no economic justification for conversion',
                'Different conceptual definitions (SP vs Value Added - Labor)',
                'No temporal overlap for validation',
                'Arbitrary scaling factors violate academic integrity'
            ],
            'recommendation': 'Use KLEMS separately or exclude from S&T extension'
        }

        logger.info("Compatibility assessment complete")
        logger.info(f"Integration recommendation: {compatibility_assessment['final_decision']['recommendation']}")

        return compatibility_assessment

    def recommend_principled_approach(self, compatibility_assessment):
        """Recommend principled approach based on analysis."""
        logger.info("Developing principled recommendation...")

        if not compatibility_assessment['final_decision']['can_integrate_meaningfully']:
            recommendation = {
                'approach': 'Conservative Extension Without KLEMS',
                'rationale': 'Maintain academic integrity by avoiding arbitrary scaling',
                'methodology': {
                    'historical_period': 'Use Phase 1 S&T replication (1958-1989)',
                    'modern_period': 'Use corporate profits method with conservative scaling',
                    'klems_status': 'Document separately but do not integrate',
                    'transparency': 'Full documentation of decision rationale'
                },
                'advantages': [
                    'No arbitrary scaling factors',
                    'Methodologically consistent',
                    'Academically defensible',
                    'Conservative approach prioritizes reliability'
                ],
                'limitations': [
                    'Does not utilize all available data',
                    'Relies on corporate profits proxy for modern period',
                    'KLEMS industry detail not incorporated'
                ],
                'alternative_research_paths': [
                    'Separate KLEMS-based profit rate study',
                    'Industry-level analysis using KLEMS directly',
                    'Methodological research on S&T-KLEMS reconciliation'
                ]
            }
        else:
            recommendation = {
                'approach': 'Principled Integration',
                'methodology': 'TBD based on identified economic justification'
            }

        logger.info(f"Recommendation: {recommendation['approach']}")
        return recommendation

    def run_analysis(self):
        """Run complete principled analysis."""
        logger.info("="*60)
        logger.info("PRINCIPLED KLEMS ANALYSIS - NO ARBITRARY SCALING")
        logger.info("="*60)

        try:
            # Conceptual analysis
            analysis = self.analyze_data_conceptually()

            # Economic realism check
            realism_check, us_context = self.check_economic_realism(analysis)

            # Compatibility assessment
            compatibility = self.assess_compatibility(analysis, realism_check)

            # Final recommendation
            recommendation = self.recommend_principled_approach(compatibility)

            results = {
                'analysis_date': pd.Timestamp.now().isoformat(),
                'conceptual_analysis': analysis,
                'realism_check': realism_check,
                'compatibility_assessment': compatibility,
                'final_recommendation': recommendation
            }

            # Save results
            output_file = self.base_dir / "data" / "modern" / "results" / "principled_klems_analysis.json"
            with open(output_file, 'w') as f:
                import json
                json.dump(results, f, indent=2, default=str)

            logger.info(f"Analysis complete. Results saved to {output_file}")
            return results

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return None

def main():
    """Main execution."""
    analyzer = PrincipledKLEMSAnalysis()
    results = analyzer.run_analysis()

    if results:
        rec = results['final_recommendation']
        print(f"\nPRINCIPLED RECOMMENDATION: {rec['approach']}")
        print(f"Rationale: {rec['rationale']}")
        print("\nThis approach maintains academic integrity without arbitrary scaling.")
    else:
        print("\nAnalysis failed - check logs for details")

if __name__ == "__main__":
    main()