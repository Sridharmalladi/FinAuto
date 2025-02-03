# tests/__init__.py
# Empty file to make the tests directory a Python package

# tests/test_data_processing.py
import pytest
import pandas as pd
from src.data_processing import DataLoader, DataCleaner

def test_data_loader():
    """Test data loading functionality."""
    loader = DataLoader()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02'],
        'revenue': [1000, 2000],
        'expenses': [800, 1500],
        'category': ['Sales', 'Services']
    })
    sample_data.to_csv('test_data.csv', index=False)
    
    # Test loading
    df = loader.load_data('test_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert all(col in df.columns for col in ['date', 'revenue', 'expenses', 'category'])

def test_data_cleaner():
    """Test data cleaning functionality."""
    cleaner = DataCleaner()
    
    # Create sample data with issues
    sample_data = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02'],
        'revenue': [1000, None],
        'expenses': [800, 1500],
        'category': ['Sales', None]
    })
    
    # Test cleaning
    cleaned_df = cleaner.clean_data(sample_data)
    assert cleaned_df['revenue'].isna().sum() == 0
    assert cleaned_df['category'].isna().sum() == 0

# tests/test_analysis.py
import pytest
import pandas as pd
import numpy as np
from src.analysis import FinancialAnalyzer

def test_financial_analyzer():
    """Test financial analysis functionality."""
    # Create sample data
    sample_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'revenue': np.random.normal(10000, 1000, 10),
        'expenses': np.random.normal(8000, 800, 10),
        'category': ['Sales'] * 5 + ['Services'] * 5
    })
    
    # Add derived columns
    sample_data['profit'] = sample_data['revenue'] - sample_data['expenses']
    sample_data['profit_margin'] = (sample_data['profit'] / sample_data['revenue'] * 100).round(2)
    
    # Initialize analyzer
    analyzer = FinancialAnalyzer(sample_data)
    
    # Test full analysis
    results = analyzer.generate_full_analysis()
    
    # Check results structure
    assert 'summary_metrics' in results
    assert 'trend_analysis' in results
    assert 'category_analysis' in results
    
    # Check metrics
    assert results['summary_metrics']['total_revenue'] > 0
    assert isinstance(results['trend_analysis']['revenue_trend'], str)
    assert len(results['category_analysis']) == 2

# tests/test_automation.py
import pytest
import pandas as pd
from src.automation import ReportGenerator
import os

def test_report_generator():
    """Test report generation functionality."""
    # Create sample data and analysis results
    sample_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5),
        'revenue': [1000, 1200, 1100, 1300, 1250],
        'expenses': [800, 900, 850, 950, 900],
        'category': ['Sales'] * 3 + ['Services'] * 2
    })
    
    sample_analysis = {
        'summary_metrics': {
            'total_revenue': 5850,
            'total_profit': 1000,
            'average_profit_margin': 17.5,
            'revenue_growth': 25.0
        },
        'trend_analysis': {
            'revenue_trend': 'upward',
            'profit_trend': 'stable'
        },
        'category_analysis': {
            'Sales': {
                'revenue': 3300,
                'profit': 600,
                'profit_margin': 18.2
            },
            'Services': {
                'revenue': 2550,
                'profit': 400,
                'profit_margin': 15.7
            }
        }
    }
    
    # Create report generator
    generator = ReportGenerator(sample_data, sample_analysis)
    
    # Test report generation
    test_output_path = 'test_report.md'
    generator.generate_report(test_output_path)
    
    # Check if report was created
    assert os.path.exists(test_output_path)
    
    # Clean up
    if os.path.exists(test_output_path):
        os.remove(test_output_path)