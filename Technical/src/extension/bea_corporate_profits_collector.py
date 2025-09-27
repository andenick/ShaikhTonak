"""
BEA Corporate Profits Data Collector for Phase 2 Extension
Collects NIPA Table 6.16D - Corporate Profits by Industry (1990-2025)

This script collects corporate profits data required for Surplus (SP) calculation
in the Shaikh & Tonak extension to present day.
"""

import requests
import pandas as pd
import json
import time
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BEACorporateProfitsCollector:
    def __init__(self, api_key_file=".secrets/bea_api_key.txt"):
        """Initialize the BEA data collector."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.api_key = self._load_api_key(api_key_file)
        self.base_url = "https://apps.bea.gov/api/data"
        self.output_dir = self.base_dir / "data" / "modern" / "bea_nipa"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Corporate profits table specifications
        self.table_name = "T61600D"  # Table 6.16D - Corporate Profits by Industry
        self.dataset_name = "NIPA"
        self.frequency = "A"  # Annual
        self.start_year = 1990
        self.end_year = 2025

        logger.info(f"BEA Corporate Profits Collector initialized")
        logger.info(f"Target: Table {self.table_name}, Years {self.start_year}-{self.end_year}")

    def _load_api_key(self, api_key_file):
        """Load BEA API key from file."""
        try:
            key_path = self.base_dir / api_key_file
            with open(key_path, 'r') as f:
                api_key = f.read().strip()
            logger.info("BEA API key loaded successfully")
            return api_key
        except Exception as e:
            logger.error(f"Failed to load API key: {e}")
            raise

    def get_table_data(self):
        """Collect corporate profits data from BEA NIPA Table 6.16D."""
        logger.info(f"Starting data collection for {self.table_name}")

        # Build API request parameters
        params = {
            'UserID': self.api_key,
            'method': 'GetData',
            'datasetname': self.dataset_name,
            'TableName': self.table_name,
            'Frequency': self.frequency,
            'Year': f"{self.start_year},{self.end_year}",
            'ResultFormat': 'json'
        }

        try:
            logger.info("Sending request to BEA API...")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info("Data received from BEA API")

            # Check for API errors
            if 'BEAAPI' in data and 'Error' in data['BEAAPI']:
                error_msg = data['BEAAPI']['Error']['ErrorDetail']['Description']
                logger.error(f"BEA API Error: {error_msg}")
                return None

            # Debug: Log the response structure
            logger.info(f"API Response keys: {list(data.keys())}")
            if 'BEAAPI' in data:
                logger.info(f"BEAAPI keys: {list(data['BEAAPI'].keys())}")
                if 'Results' in data['BEAAPI']:
                    logger.info(f"Results keys: {list(data['BEAAPI']['Results'].keys())}")

            # Extract data
            if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
                if 'Data' in data['BEAAPI']['Results']:
                    results = data['BEAAPI']['Results']['Data']
                    logger.info(f"Successfully retrieved {len(results)} data points")
                    return results
                else:
                    logger.error("No 'Data' key in Results")
                    # Save the response for debugging
                    debug_file = self.output_dir / "debug_response.json"
                    with open(debug_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    logger.info(f"Debug response saved to {debug_file}")
                    return None
            else:
                logger.error("Unexpected API response structure")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return None

    def process_and_save_data(self, raw_data):
        """Process and save the corporate profits data."""
        if not raw_data:
            logger.error("No data to process")
            return False

        logger.info("Processing corporate profits data...")

        # Convert to DataFrame for easier processing
        df = pd.DataFrame(raw_data)

        # Log basic info about the data
        logger.info(f"Data shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")

        # Save raw data
        raw_file = self.output_dir / f"corporate_profits_raw_{self.start_year}_{self.end_year}.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f, indent=2)
        logger.info(f"Raw data saved to {raw_file}")

        # Process and save as CSV
        csv_file = self.output_dir / f"corporate_profits_{self.start_year}_{self.end_year}.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"Processed data saved to {csv_file}")

        # Save metadata
        metadata = {
            'collection_date': datetime.now().isoformat(),
            'source': 'BEA NIPA API',
            'table': self.table_name,
            'description': 'Corporate Profits by Industry',
            'frequency': self.frequency,
            'period': f"{self.start_year}-{self.end_year}",
            'total_records': len(raw_data),
            'api_key_used': self.api_key[:8] + "..." if self.api_key else "None"
        }

        metadata_file = self.output_dir / f"corporate_profits_metadata_{self.start_year}_{self.end_year}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_file}")

        return True

    def run_collection(self):
        """Run the complete data collection process."""
        logger.info("="*50)
        logger.info("STARTING BEA CORPORATE PROFITS DATA COLLECTION")
        logger.info("="*50)

        try:
            # Get data from API
            raw_data = self.get_table_data()

            if raw_data:
                # Process and save
                success = self.process_and_save_data(raw_data)

                if success:
                    logger.info("="*50)
                    logger.info("✅ CORPORATE PROFITS DATA COLLECTION COMPLETE")
                    logger.info("="*50)
                    return True
                else:
                    logger.error("❌ Data processing failed")
                    return False
            else:
                logger.error("❌ Data collection failed")
                return False

        except Exception as e:
            logger.error(f"❌ Collection failed with error: {e}")
            return False

def main():
    """Main execution function."""
    collector = BEACorporateProfitsCollector()
    success = collector.run_collection()

    if success:
        print("\nSUCCESS: CORPORATE PROFITS DATA COLLECTION COMPLETE")
        print("Next step: Federal Reserve Capacity Utilization data")
    else:
        print("\nFAILED: CORPORATE PROFITS DATA COLLECTION")
        print("Check logs for details")

if __name__ == "__main__":
    main()