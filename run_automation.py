#!/usr/bin/env python3
"""
LUFT Automation Runner
Main script for running automated data collection
"""

import time
import signal
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from luft.collectors import SolarWindCollector, CosmicDataCollector
from luft.storage import DataArchiver
from luft.utils import setup_logging, ConfigLoader


class LUFTRunner:
    """
    Main automation runner for LUFT.
    Coordinates data collection, archiving, and continuous operation.
    """
    
    def __init__(self, config_file: str = "config/luft_config.yml"):
        """
        Initialize the LUFT runner.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = ConfigLoader(config_file)
        self.logger = setup_logging(
            log_level=self.config.get('logging.level', 'INFO'),
            log_file=self.config.get('logging.file', 'logs/luft.log')
        )
        
        # Initialize collectors
        self.solar_wind_collector = SolarWindCollector()
        self.cosmic_collector = CosmicDataCollector()
        
        # Initialize archiver
        archive_path = self.config.get('storage.archive_path', 'data/archive')
        self.archiver = DataArchiver(archive_path)
        
        # Control flags
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def collect_and_archive_solar_wind(self):
        """Collect and archive solar wind data."""
        try:
            self.logger.info("Collecting solar wind data...")
            data = self.solar_wind_collector.collect_realtime_data()
            
            # Archive the data
            filepath = self.archiver.archive_data(
                data=data,
                source='solar_wind',
                metadata={
                    'collector': 'SolarWindCollector',
                    'version': '0.1.0'
                }
            )
            
            self.logger.info(f"Solar wind data archived: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error collecting solar wind data: {e}")
            return False
    
    def collect_and_archive_cosmic_data(self):
        """Collect and archive cosmic data."""
        try:
            self.logger.info("Collecting cosmic data...")
            data = self.cosmic_collector.collect_realtime_data()
            
            # Archive the data
            filepath = self.archiver.archive_data(
                data=data,
                source='cosmic',
                metadata={
                    'collector': 'CosmicDataCollector',
                    'version': '0.1.0'
                }
            )
            
            self.logger.info(f"Cosmic data archived: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error collecting cosmic data: {e}")
            return False
    
    def run_once(self):
        """Run a single collection cycle."""
        self.logger.info("=" * 60)
        self.logger.info("Starting data collection cycle")
        self.logger.info("=" * 60)
        
        # Collect solar wind data if enabled
        if self.config.get('collectors.solar_wind.enabled', True):
            self.collect_and_archive_solar_wind()
        
        # Collect cosmic data if enabled
        if self.config.get('collectors.cosmic_data.enabled', True):
            self.collect_and_archive_cosmic_data()
        
        self.logger.info("Collection cycle complete")
    
    def run_continuous(self):
        """Run continuous data collection."""
        self.logger.info("=" * 60)
        self.logger.info("LUFT - The Unifying Fields Program")
        self.logger.info("Automated Data Collection System")
        self.logger.info("=" * 60)
        
        interval = self.config.get('collectors.solar_wind.interval', 300)
        self.logger.info(f"Collection interval: {interval} seconds")
        
        while self.running:
            try:
                self.run_once()
                
                if self.running:
                    self.logger.info(f"Waiting {interval} seconds until next collection...")
                    time.sleep(interval)
                    
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                if self.running:
                    self.logger.info("Waiting 60 seconds before retry...")
                    time.sleep(60)
        
        self.logger.info("LUFT automation stopped")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='LUFT - The Unifying Fields Program Automation Runner'
    )
    parser.add_argument(
        '--config',
        default='config/luft_config.yml',
        help='Configuration file path'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no continuous loop)'
    )
    
    args = parser.parse_args()
    
    # Initialize and run
    runner = LUFTRunner(config_file=args.config)
    
    if args.once:
        runner.run_once()
    else:
        runner.run_continuous()


if __name__ == '__main__':
    main()
