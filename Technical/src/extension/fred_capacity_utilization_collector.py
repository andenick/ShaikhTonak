"""
Federal Reserve Capacity Utilization Data Collector for Phase 2 Extension
Collects G.17 Industrial Production and Capacity Utilization (1990-2025)

This script collects capacity utilization data required for the utilization rate (u)
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

class FREDCapacityUtilizationCollector:
    def __init__(self, api_key="22896375f58f5dd747eaf30b32df94d3"):
        """Initialize the FRED data collector."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.output_dir = self.base_dir / "data" / "modern" / "fed_capacity"
        self.raw_dir = self.base_dir / "archive" / "deprecated_code" / "deprecated_databases" / "Database_Leontief_original" / "data" / "raw" / "fred"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        # Capacity utilization series specifications
        self.series_list = {
            'CAPUTLG3311A2S': 'Capacity Utilization: Manufacturing (NAICS = 31-33): Primary Metal Industries',
            'CAPUTLG331S': 'Capacity Utilization: Manufacturing (NAICS = 31-33): Primary Metal Industries',
            'CAPUTLB00004S': 'Capacity Utilization: Total Manufacturing',
            'CAPUTLB50001S': 'Capacity Utilization: Manufacturing (NAICS = 31-33): Durable Goods',
            'CAPUTLG321S': 'Capacity Utilization: Manufacturing (NAICS = 31-33): Wood Products'
        }

        # Use the total manufacturing series as our primary
        self.primary_series = 'CAPUTLB00004S'
        self.start_date = '1990-01-01'
        self.end_date = '2025-12-31'

        logger.info(f"FRED Capacity Utilization Collector initialized")
        logger.info(f"Primary series: {self.primary_series}")
        logger.info(f"Raw data will be saved to: {self.raw_dir}")
        logger.info(f"Processed data will be saved to: {self.output_dir}")

    def save_raw_data(self, series_id, raw_response):
        """Save raw API response for future use."""
        raw_file = self.raw_dir / f"raw_{series_id}_1990_2025.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_response, f, indent=2)
        logger.info(f"Raw data saved to {raw_file}")
        return raw_file

    def get_series_data(self, series_id):
        """Collect capacity utilization data from FRED API."""
        logger.info(f"Collecting data for series: {series_id}")

        # Build API request parameters
        params = {
            'series_id': series_id,
            'observation_start': self.start_date,
            'observation_end': self.end_date,
            'frequency': 'm',  # Monthly data
            'file_type': 'json'
        }

        if self.api_key:
            params['api_key'] = self.api_key

        try:
            logger.info(f"Sending request to FRED API for {series_id}...")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info("Data received from FRED API")

            # Save raw data
            self.save_raw_data(series_id, data)

            # Extract observations
            if 'observations' in data:
                observations = data['observations']
                logger.info(f"Successfully retrieved {len(observations)} observations for {series_id}")
                return observations
            else:
                logger.error("No observations found in response")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return None

    def process_monthly_to_annual(self, monthly_data):
        """Convert monthly capacity utilization data to annual averages."""
        if not monthly_data:
            return None

        logger.info("Converting monthly data to annual averages...")

        # Convert to DataFrame
        df = pd.DataFrame(monthly_data)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['year'] = df['date'].dt.year

        # Filter out missing values
        df = df.dropna(subset=['value'])

        # Calculate annual averages
        annual_data = df.groupby('year')['value'].mean().reset_index()
        annual_data['value'] = annual_data['value'].round(3)

        logger.info(f"Converted to {len(annual_data)} annual observations")
        return annual_data

    def save_data(self, series_id, monthly_data, annual_data):
        """Save both monthly and annual data."""
        # Save monthly data
        monthly_file = self.output_dir / f"capacity_utilization_{series_id}_monthly_1990_2025.csv"
        monthly_df = pd.DataFrame(monthly_data)
        monthly_df.to_csv(monthly_file, index=False)
        logger.info(f"Monthly data saved to {monthly_file}")

        # Save annual data
        annual_file = self.output_dir / f"capacity_utilization_{series_id}_annual_1990_2025.csv"
        annual_data.to_csv(annual_file, index=False)
        logger.info(f"Annual data saved to {annual_file}")

        # Save metadata
        metadata = {
            'collection_date': datetime.now().isoformat(),
            'source': 'Federal Reserve Bank of St. Louis (FRED)',
            'series_id': series_id,
            'description': self.series_list.get(series_id, f'Capacity Utilization Series {series_id}'),
            'frequency_original': 'monthly',
            'frequency_processed': 'annual',
            'period': f"1990-2025",
            'monthly_records': len(monthly_data),
            'annual_records': len(annual_data),
            'api_key_used': 'Yes' if self.api_key else 'Public access'
        }

        metadata_file = self.output_dir / f"capacity_utilization_{series_id}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_file}")

        return True

    def run_collection(self):
        """Run the complete capacity utilization data collection."""
        logger.info("="*60)
        logger.info("STARTING FEDERAL RESERVE CAPACITY UTILIZATION COLLECTION")
        logger.info("="*60)

        success_count = 0
        total_series = len(self.series_list)

        try:
            for series_id, description in self.series_list.items():
                logger.info(f"\nProcessing series: {series_id}")
                logger.info(f"Description: {description}")

                # Get monthly data
                monthly_data = self.get_series_data(series_id)

                if monthly_data:
                    # Convert to annual
                    annual_data = self.process_monthly_to_annual(monthly_data)

                    if annual_data is not None:
                        # Save data
                        save_success = self.save_data(series_id, monthly_data, annual_data)
                        if save_success:
                            success_count += 1
                            logger.info(f"✅ Successfully processed {series_id}")
                        else:
                            logger.error(f"❌ Failed to save data for {series_id}")
                    else:
                        logger.error(f"❌ Failed to process monthly data for {series_id}")
                else:
                    logger.error(f"❌ Failed to collect data for {series_id}")

                # Small delay between requests
                time.sleep(1)

            logger.info("="*60)
            logger.info(f"CAPACITY UTILIZATION COLLECTION COMPLETE")
            logger.info(f"Success: {success_count}/{total_series} series collected")
            logger.info("="*60)

            return success_count > 0

        except Exception as e:
            logger.error(f"Collection failed with error: {e}")
            return False

def main():
    """Main execution function."""
    collector = FREDCapacityUtilizationCollector()
    success = collector.run_collection()

    if success:
        print(f"\nSUCCESS: CAPACITY UTILIZATION DATA COLLECTION COMPLETE")
        print(f"Primary series for S&T analysis: {collector.primary_series}")
        print("Next step: Historical gap fill (1990-1996)")
    else:
        print(f"\nFAILED: CAPACITY UTILIZATION DATA COLLECTION")
        print("Check logs for details")

if __name__ == "__main__":
    main()