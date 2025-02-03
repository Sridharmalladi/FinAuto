# src/utils/helpers.py
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories(dirs: List[str]):
    """Create necessary directories if they don't exist."""
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info(f"Created directory: {dir_path}")

def validate_numerical_columns(df: pd.DataFrame, columns: List[str]) -> bool:
    """Validate that specified columns are numerical."""
    for col in columns:
        if not np.issubdtype(df[col].dtype, np.number):
            logger.error(f"Column {col} is not numerical")
            return False
    return True

def calculate_growth_rate(old_value: float, new_value: float) -> float:
    """Calculate growth rate between two values."""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / abs(old_value) * 100).round(2)

def format_currency(value: float) -> str:
    """Format number as currency string."""
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Format number as percentage string."""
    return f"{value:.2f}%"

def get_date_range(df: pd.DataFrame, date_column: str) -> Dict[str, str]:
    """Get the date range of the dataset."""
    start_date = df[date_column].min().strftime('%Y-%m-%d')
    end_date = df[date_column].max().strftime('%Y-%m-%d')
    return {'start_date': start_date, 'end_date': end_date}

def save_to_json(data: Dict[str, Any], filepath: str):
    """Save dictionary data to JSON file."""
    import json
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, default=str)
        logger.info(f"Data saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving to JSON: {str(e)}")

def load_from_json(filepath: str) -> Dict[str, Any]:
    """Load dictionary data from JSON file."""
    import json
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON: {str(e)}")
        return {}

def create_timestamp() -> str:
    """Create a timestamp string."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def validate_email(email: str) -> bool:
    """Simple email validation."""
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))