"""
Cosmic Data Collector
Collects cosmic ray and particle data from public sources
"""

import requests
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CosmicDataCollector:
    """
    Collects cosmic ray and particle flux data from various sources.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Cosmic Data Collector.
        
        Args:
            config: Configuration dictionary with data source URLs
        """
        self.config = config or {}
        self.sources = {
            'noaa_proton_flux': 'https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-6-hour.json',
            'noaa_electron_flux': 'https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-plot-6-hour.json',
            'noaa_xray_flux': 'https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json'
        }
        
    def collect_realtime_data(self) -> Dict:
        """
        Collect real-time cosmic data from all configured sources.
        
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
    
    def get_particle_flux(self) -> Optional[Dict]:
        """
        Get current particle flux readings.
        
        Returns:
            Particle flux data or None if unavailable
        """
        try:
            data = self.collect_realtime_data()
            return data
        except Exception as e:
            logger.error(f"Error getting particle flux: {e}")
            return None
