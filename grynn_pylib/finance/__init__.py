import warnings
import pandas as pd

def cagr(data: pd.DataFrame|pd.Series, period = None) -> float:
    """
    Calculate the Compound Annual Growth Rate (CAGR) of a time series.
    Assumptions: index is a datetime index with business days
    """
    data_len_days = (data.index[-1] - data.index[0]).days
    assert data_len_days > 365, 'Data must have at least 1 year (365 days)'
    
    if period is None:
        period = data_len_days
        
    return (data.iloc[-1] / data.iloc[0]) ** (period/252) - 1

def rolling_cagr(data: pd.DataFrame, window = 252*3) -> pd.Series:
    """
    Calculate the rolling Compound Annual Growth Rate (CAGR) of a time series.
    Assumptions: window represents a multiple of years
    """
    abs = data / data.shift(window)             # 3y absolute change
    cagr_series = abs ** (window/252) - 1               # 3y CAGR
    if (data.index[-1] - data.index[0]).days < 365:
        warnings.warn('Index is less than 1 year long. CAGR may be inaccurate.', UserWarning)     
    return cagr_series

    
