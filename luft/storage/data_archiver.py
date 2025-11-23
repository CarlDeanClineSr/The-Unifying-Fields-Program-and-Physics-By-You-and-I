"""
Data Archiver
Archives collected data with proper versioning and metadata
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import hashlib

logger = logging.getLogger(__name__)


class DataArchiver:
    """
    Handles archiving and retrieval of collected scientific data.
    Ensures reproducibility through proper versioning and metadata.
    """
    
    def __init__(self, archive_path: str = "data/archive"):
        """
        Initialize the Data Archiver.
        
        Args:
            archive_path: Base path for data archive
        """
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
    def archive_data(self, data: Dict, source: str, metadata: Optional[Dict] = None) -> str:
        """
        Archive collected data with metadata.
        
        Args:
            data: Data to archive
            source: Source identifier (e.g., 'solar_wind', 'cosmic')
            metadata: Additional metadata to include
            
        Returns:
            Archive file path
        """
        timestamp = datetime.utcnow()
        date_path = self.archive_path / source / timestamp.strftime("%Y/%m/%d")
        date_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        filename = f"{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = date_path / filename
        
        # Prepare archive package
        archive_package = {
            'version': '1.0',
            'archived_at': timestamp.isoformat(),
            'source': source,
            'data': data,
            'metadata': metadata or {},
            'checksum': self._calculate_checksum(data)
        }
        
        # Write to file
        try:
            with open(filepath, 'w') as f:
                json.dump(archive_package, f, indent=2)
            logger.info(f"Data archived to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error archiving data: {e}")
            raise
    
    def retrieve_data(self, filepath: str) -> Optional[Dict]:
        """
        Retrieve archived data from file.
        
        Args:
            filepath: Path to archived data file
            
        Returns:
            Archived data package or None if not found
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Archive file not found: {filepath}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving data: {e}")
            return None
    
    def verify_integrity(self, archive_package: Dict) -> bool:
        """
        Verify data integrity using checksum.
        
        Args:
            archive_package: Archive package to verify
            
        Returns:
            True if integrity check passes, False otherwise
        """
        stored_checksum = archive_package.get('checksum')
        calculated_checksum = self._calculate_checksum(archive_package.get('data'))
        
        if stored_checksum == calculated_checksum:
            logger.info("Data integrity verified")
            return True
        else:
            logger.warning("Data integrity check failed")
            return False
    
    def _calculate_checksum(self, data: Any) -> str:
        """
        Calculate SHA-256 checksum of data.
        
        Args:
            data: Data to checksum
            
        Returns:
            Hex digest of checksum
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def list_archives(self, source: str, date: Optional[str] = None) -> list:
        """
        List available archives for a given source.
        
        Args:
            source: Source identifier
            date: Optional date filter (YYYY-MM-DD)
            
        Returns:
            List of archive file paths
        """
        source_path = self.archive_path / source
        
        if not source_path.exists():
            return []
        
        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                date_path = source_path / dt.strftime("%Y/%m/%d")
                if date_path.exists():
                    return [str(f) for f in date_path.glob("*.json")]
            except ValueError:
                logger.error(f"Invalid date format: {date}")
                return []
        
        # Return all archives if no date specified
        return [str(f) for f in source_path.rglob("*.json")]
