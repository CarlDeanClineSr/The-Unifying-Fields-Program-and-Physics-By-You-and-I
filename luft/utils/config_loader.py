"""
Configuration loader for LUFT
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """
    Handles loading and managing configuration for LUFT.
    """
    
    def __init__(self, config_file: str = "config/luft_config.yml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                if self.config_file.suffix in ['.yml', '.yaml']:
                    return yaml.safe_load(f) or {}
                elif self.config_file.suffix == '.json':
                    return json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {self.config_file.suffix}")
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            'collectors': {
                'solar_wind': {
                    'enabled': True,
                    'interval': 300  # 5 minutes
                },
                'cosmic_data': {
                    'enabled': True,
                    'interval': 300  # 5 minutes
                }
            },
            'storage': {
                'archive_path': 'data/archive',
                'cache_path': 'data/cache'
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/luft.log'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def save_config(self, config_file: str = None):
        """
        Save current configuration to file.
        
        Args:
            config_file: Optional path to save to (uses default if None)
        """
        save_path = Path(config_file) if config_file else self.config_file
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            if save_path.suffix in ['.yml', '.yaml']:
                yaml.dump(self.config, f, default_flow_style=False)
            elif save_path.suffix == '.json':
                json.dump(self.config, f, indent=2)
