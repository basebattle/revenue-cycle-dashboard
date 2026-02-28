import pandas as pd
import pytest
from revenue_cycle_dashboard.data.calculator import KPICalculator
from datetime import date

def test_net_collection_rate():
    """Validates Net Collection Rate formula."""
    data = {
        'payments': [100, 200, 300],
        'allowed_amount': [110, 210, 310]
    }
    df = pd.DataFrame(data)
    calc = KPICalculator()
    result = calc.calculate_all(df)
    
    expected = (600 / 630 * 100) # 95.238...
    assert result['net_collection_rate'] == round(expected, 1)

def test_gross_collection_rate():
    """Validates Gross Collection Rate formula."""
    data = {
        'payments': [100, 200],
        'charges': [200, 400]
    }
    df = pd.DataFrame(data)
    calc = KPICalculator()
    result = calc.calculate_all(df)
    
    expected = (300 / 600 * 100) # 50.0
    assert result['gross_collection_rate'] == round(expected, 1)

def test_denial_rate():
    """Validates Denial Rate formula."""
    data = {
        'claim_status': ['Paid', 'Denied', 'Paid', 'Paid', 'Denied']
    }
    df = pd.DataFrame(data)
    calc = KPICalculator()
    result = calc.calculate_all(df)
    
    expected = (2 / 5 * 100) # 40.0
    assert result['denial_rate'] == round(expected, 1)

def test_empty_dataframe():
    """Validates calculator behavior with empty data."""
    df = pd.DataFrame()
    calc = KPICalculator()
    result = calc.calculate_all(df)
    
    assert result['net_collection_rate'] is None
    assert result['denial_rate'] is None
