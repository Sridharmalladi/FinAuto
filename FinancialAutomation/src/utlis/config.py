# src/utils/config.py
import yaml
from typing import Dict, Any
import os

class Config:
    def __init__(self, config_path: str = 'config.yaml'):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'data': {
                'input_path': 'data/raw/financial_data_2023.csv',
                'output_path': 'data/processed/processed_data.csv',
                'date_format': '%Y-%m-%d'
            },
            'analysis': {
                'outlier_threshold': 3,
                'min_data_points': 30,
                'categories': ['Sales', 'Services', 'Consulting']
            },
            'reporting': {
                'report_path': 'reports/financial_insights.md',
                'charts_dir': 'reports/charts',
                'include_charts': True
            },
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'recipient_email': ''
            }
        }
    
    def get(self, section: str, key: str) -> Any:
        """Get configuration value."""
        try:
            return self.config[section][key]
        except KeyError:
            return None
    
    def update(self, section: str, key: str, value: Any):
        """Update configuration value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value