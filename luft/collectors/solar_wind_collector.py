"""
Solar Wind Data Collector
Collects real-time solar wind data from public APIs
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SolarWindCollector:
    """
    Collects real-time solar wind data from NOAA and NASA sources.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Solar Wind Collector.
        
        Args:
            config: Configuration dictionary with data source URLs
        """
        self.config = config or {}
        self.sources = {
            'noaa_swpc': 'https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json',
            'noaa_mag': 'https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json',
            'noaa_plasma': 'https://services.swpc.noaa.gov/json/rtsw/rtsw_plasma_1m.json'
        }
        
    def collect_realtime_data(self) -> Dict:
        """
        Collect real-time solar wind data from all configured sources.
        
        Returns:
            Dictionary containing collected data with timestamps
        """
        collected_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'sources': {}
        }
        
        for source_name, url in self.sources.items():
            try:
                logger.info(f"Collecting data from {source_name}")
                data = self._fetch_data(url)
                collected_data['sources'][source_name] = {
                    'status': 'success',
                    'data': data,
                    'collected_at': datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error collecting from {source_name}: {e}")
                collected_data['sources'][source_name] = {
                    'status': 'error',
                    'error': str(e),
                    'collected_at': datetime.utcnow().isoformat()
                }
        
        return collected_data
    
    def _fetch_data(self, url: str, timeout: int = 30) -> Dict:
        """
        Fetch data from a given URL.
        
        Args:
            url: URL to fetch data from
            timeout: Request timeout in seconds
            
        Returns:
            Parsed JSON data
        """
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    def get_latest_reading(self) -> Optional[Dict]:
        """
        Get the most recent solar wind reading.
        
        Returns:
            Latest reading data or None if unavailable
        """
        try:
            data = self.collect_realtime_data()
            return data
        except Exception as e:
            logger.error(f"Error getting latest reading: {e}")
            return None
