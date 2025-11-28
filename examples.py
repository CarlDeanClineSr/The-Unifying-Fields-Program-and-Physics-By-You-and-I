#!/usr/bin/env python3
"""
LUFT Example Usage
Demonstrates how to use LUFT components
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from luft.collectors import SolarWindCollector, CosmicDataCollector
from luft.storage import DataArchiver
from luft.utils import setup_logging


def example_solar_wind_collection():
    """Example: Collect solar wind data."""
    print("\n" + "=" * 60)
    print("Example 1: Solar Wind Data Collection")
    print("=" * 60)
    
    collector = SolarWindCollector()
    data = collector.collect_realtime_data()
    
    print(f"\nCollected data from {len(data['sources'])} sources")
    for source_name, source_data in data['sources'].items():
        print(f"  - {source_name}: {source_data['status']}")
    
    return data


def example_cosmic_data_collection():
    """Example: Collect cosmic data."""
    print("\n" + "=" * 60)
    print("Example 2: Cosmic Data Collection")
    print("=" * 60)
    
    collector = CosmicDataCollector()
    data = collector.collect_realtime_data()
    
    print(f"\nCollected data from {len(data['sources'])} sources")
    for source_name, source_data in data['sources'].items():
        print(f"  - {source_name}: {source_data['status']}")
    
    return data


def example_data_archiving():
    """Example: Archive collected data."""
    print("\n" + "=" * 60)
    print("Example 3: Data Archiving")
    print("=" * 60)
    
    # Collect data
    collector = SolarWindCollector()
    data = collector.collect_realtime_data()
    
    # Archive it
    archiver = DataArchiver("data/archive")
    filepath = archiver.archive_data(
        data=data,
        source='solar_wind',
        metadata={'example': True}
    )
    
    print(f"\nData archived to: {filepath}")
    
    # Retrieve and verify
    archive_package = archiver.retrieve_data(filepath)
    if archive_package:
        is_valid = archiver.verify_integrity(archive_package)
        print(f"Data integrity verified: {is_valid}")
    
    return filepath


def example_list_archives():
    """Example: List archived data."""
    print("\n" + "=" * 60)
    print("Example 4: List Archived Data")
    print("=" * 60)
    
    archiver = DataArchiver("data/archive")
    
    # List all solar wind archives
    archives = archiver.list_archives('solar_wind')
    print(f"\nFound {len(archives)} solar wind archives")
    
    if archives:
        print("\nRecent archives:")
        for archive in archives[-5:]:  # Show last 5
            print(f"  - {archive}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("LUFT - The Unifying Fields Program")
    print("Example Usage Demonstrations")
    print("=" * 60)
    
    # Set up logging
    setup_logging(log_level="INFO")
    
    try:
        # Run examples
        example_solar_wind_collection()
        example_cosmic_data_collection()
        example_data_archiving()
        example_list_archives()
        
        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("This may be due to network issues or unavailable data sources.")
        print("Try running again or check your internet connection.\n")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
