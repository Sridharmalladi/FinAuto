# src/analysis/__init__.py
from .financial_metrics import FinancialAnalyzer

# src/analysis/financial_metrics.py
import pandas as pd
import numpy as np
from typing import Dict, Any

class FinancialAnalyzer:
    """Combined class for financial metrics and trend analysis"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def generate_full_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive financial analysis."""
        return {
            'summary_metrics': self._calculate_summary_metrics(),
            'trend_analysis': self._analyze_trends(),
            'category_analysis': self._analyze_categories()
        }
    
    def _calculate_summary_metrics(self) -> Dict[str, float]:
        """Calculate key financial metrics."""
        return {
            'total_revenue': self.data['revenue'].sum(),
            'total_expenses': self.data['expenses'].sum(),
            'total_profit': self.data['profit'].sum(),
            'average_profit_margin': self.data['profit_margin'].mean(),
            'revenue_growth': self._calculate_growth('revenue'),
            'profit_growth': self._calculate_growth('profit')
        }
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends in financial metrics."""
        monthly_data = self.data.set_index('date').resample('M').sum()
        
        return {
            'monthly_revenue': monthly_data['revenue'].to_dict(),
            'monthly_profit': monthly_data['profit'].to_dict(),
            'revenue_trend': self._calculate_trend('revenue'),
            'profit_trend': self._calculate_trend('profit')
        }
    
    def _analyze_categories(self) -> Dict[str, Dict[str, float]]:
        """Analyze performance by category."""
        category_analysis = self.data.groupby('category').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).round(2)
        
        return category_analysis.to_dict('index')
    
    def _calculate_growth(self, column: str) -> float:
        """Calculate growth rate for a given metric."""
        first_value = self.data[column].iloc[0]
        last_value = self.data[column].iloc[-1]
        return ((last_value - first_value) / first_value * 100).round(2)
    
    def _calculate_trend(self, column: str) -> str:
        """Calculate trend direction using simple linear regression."""
        x = np.arange(len(self.data))
        y = self.data[column].values
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0:
            return 'upward'
        elif slope < 0:
            return 'downward'
        return 'stable'