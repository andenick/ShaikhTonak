"""
Extract Corporate Profits Data from Existing NIPA Files
Found A939RC corporate profits data covering 1990-2024 in raw NIPA files!

This script extracts the corporate profits data we already have instead of
requiring manual downloads.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExistingCorporateProfitsExtractor:
    def __init__(self):
        """Initialize the corporate profits extractor."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.nipa_file = self.base_dir / "archive" / "deprecated_code" / "deprecated_databases" / "Database_Leontief_original" / "data" / "raw" / "bea-nipa" / "flatFiles" / "nipadataA.txt"
        self.output_dir = self.base_dir / "data" / "modern" / "bea_nipa"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Corporate profits series code
        self.series_code = "A939RC"  # Corporate Profits after Tax

        logger.info(f"Corporate Profits Extractor initialized")
        logger.info(f"Source file: {self.nipa_file}")

    def extract_corporate_profits(self):
        """Extract A939RC corporate profits data from NIPA file."""
        logger.info("Extracting corporate profits data...")

        if not self.nipa_file.exists():
            logger.error(f"NIPA file not found: {self.nipa_file}")
            return None

        try:
            # Read the NIPA data file
            with open(self.nipa_file, 'r') as f:
                lines = f.readlines()

            # Extract A939RC data
            corporate_profits_data = []
            for line in lines:
                if line.startswith('A939RC,'):
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        year = int(parts[1])
                        value_str = parts[2].replace('"', '').replace(',', '')
                        try:
                            value = float(value_str)
                            corporate_profits_data.append({
                                'year': year,
                                'value': value,
                                'series_code': 'A939RC',
                                'description': 'Corporate Profits After Tax'
                            })
                        except ValueError:
                            logger.warning(f"Could not parse value: {value_str} for year {year}")

            logger.info(f"Extracted {len(corporate_profits_data)} years of corporate profits data")
            return corporate_profits_data

        except Exception as e:
            logger.error(f"Failed to extract corporate profits: {e}")
            return None

    def filter_target_period(self, data, start_year=1990, end_year=2025):
        """Filter data for the target period."""
        if not data:
            return None

        filtered_data = [row for row in data if start_year <= row['year'] <= end_year]
        logger.info(f"Filtered to target period {start_year}-{end_year}: {len(filtered_data)} years")
        return filtered_data

    def save_corporate_profits_data(self, data):
        """Save the corporate profits data."""
        if not data:
            logger.error("No data to save")
            return False

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save as CSV
        csv_file = self.output_dir / "corporate_profits_1990_2024_extracted.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"Corporate profits data saved: {csv_file}")

        # Save metadata
        metadata = {
            'extraction_date': datetime.now().isoformat(),
            'source_file': str(self.nipa_file),
            'series_code': 'A939RC',
            'description': 'Corporate Profits After Tax (millions of dollars)',
            'period_start': min(row['year'] for row in data),
            'period_end': max(row['year'] for row in data),
            'total_years': len(data),
            'data_quality': 'Official BEA NIPA source'
        }

        metadata_file = self.output_dir / "corporate_profits_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved: {metadata_file}")

        return True

    def run_extraction(self):
        """Run the complete corporate profits extraction."""
        logger.info("="*60)
        logger.info("EXTRACTING EXISTING CORPORATE PROFITS DATA")
        logger.info("="*60)

        try:
            # Extract all data
            all_data = self.extract_corporate_profits()

            if all_data:
                # Filter to target period
                target_data = self.filter_target_period(all_data)

                if target_data:
                    # Save the data
                    success = self.save_corporate_profits_data(target_data)

                    if success:
                        logger.info("="*60)
                        logger.info("✅ CORPORATE PROFITS EXTRACTION COMPLETE")
                        logger.info(f"Period covered: {min(row['year'] for row in target_data)}-{max(row['year'] for row in target_data)}")
                        logger.info(f"Total years: {len(target_data)}")
                        logger.info("="*60)
                        return True
                    else:
                        logger.error("Failed to save data")
                        return False
                else:
                    logger.error("No data in target period")
                    return False
            else:
                logger.error("Failed to extract data")
                return False

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return False

def main():
    """Main execution function."""
    extractor = ExistingCorporateProfitsExtractor()
    success = extractor.run_extraction()

    if success:
        print("\nSUCCESS: CORPORATE PROFITS DATA EXTRACTION COMPLETE")
        print("Found existing BEA NIPA corporate profits data covering 1990-2024!")
        print("No manual download required for corporate profits.")
    else:
        print("\nFAILED: CORPORATE PROFITS DATA EXTRACTION")
        print("Check logs for details")

if __name__ == "__main__":
    main()