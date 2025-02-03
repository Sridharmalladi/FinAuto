# src/data_processing/__init__.py
from .data_loader import DataLoader
from .data_cleaner import DataCleaner

# src/data_processing/data_loader.py
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self):
        self.required_columns = ['date', 'revenue', 'expenses', 'category']
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load financial data from CSV file."""
        try:
            df = pd.read_csv(filepath)
            return self._validate_data(df)
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate the data structure."""
        # Check required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        return df

# src/data_processing/data_cleaner.py
import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self):
        self.outlier_threshold = 3  # Standard deviations for outlier detection
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare the financial data."""
        df = df.copy()
        df = self._handle_missing_values(df)
        df = self._handle_outliers(df)
        df = self._add_derived_features(df)
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # Fill missing numerical values with median
        numerical_cols = ['revenue', 'expenses']
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        
        # Fill missing categories with mode
        df['category'] = df['category'].fillna(df['category'].mode()[0])
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using IQR method."""
        for col in ['revenue', 'expenses']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)
        return df
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived financial features."""
        df['profit'] = df['revenue'] - df['expenses']
        df['profit_margin'] = (df['profit'] / df['revenue'] * 100).round(2)
        return df