import pandas as pd
import numpy as np
from scipy.stats import boxcox
from scipy.special import inv_boxcox
import streamlit as st

def log_transform(time_series: pd.Series, reverse_tranformation:bool = False):
    if reverse_tranformation:
        original_ts = np.exp(time_series) 
        return original_ts
    
    # remove zeros
    time_series = time_series.replace(0, np.nan).dropna()
    return np.log(time_series).dropna()

def boxcox_transform(time_series: pd.Series, reverse_tranformation:bool=False):
    """
    Apply Box-Cox transformation to a time series.

    Parameters:
    - time_series (pd.Series): Time series to transform.

    Returns:
    - pd.Series: Box-Cox transformed time series.
    """ 

    if reverse_tranformation:
        pass

    # Adicionar uma constante para evitar valores zero ou negativos
    ts_positive = time_series + 1 - time_series.min()

    # Tenta aplicar a transformação Box-Cox
    try:
        transformed, _ = boxcox(ts_positive['Valor'])
        return pd.Series(transformed, index=ts_positive.index)
    except Exception as e:
        st.error(f'Erro ao aplicar a transformação Box-Cox: {e}')
        return time_series

def difference_time_series(time_series: pd.Series, lags: int = 1, reverse_tranformation:bool=False):
    if reverse_tranformation:
        return time_series.shift(-lags).cumsum()
    return time_series.diff(lags).dropna() 

def difference_01_and_difference_07(time_series: pd.Series, reverse_tranformation:bool=False):
    if reverse_tranformation:
        reverse_diff7 = time_series.shift(-7).cumsum() 
        original_ts = reverse_diff7.cumsum() 
        return original_ts
    
    detrended_serie = time_series.diff(periods=1).dropna() 
    remove_seasonality = detrended_serie.diff(periods=7).dropna() 
    return remove_seasonality

def transformation_picker(time_series: pd.Series):
    transform_filter = st.selectbox(
        'Selecione uma transformação para aplicar à série temporal',
        ('Série Original', 'Logarítmica', 'Box-Cox', 'Diferenciação Lag 01', 'Diferenciação Lag 02', 'Diferenciação Lag 01 + Diferenciação Lag 07'))

    if transform_filter == 'Logarítmica':
        return log_transform(time_series)
    elif transform_filter == 'Box-Cox':
        return boxcox_transform(time_series)
    elif transform_filter == 'Diferenciação Lag 01':
        return difference_time_series(time_series, 1)
    elif transform_filter == 'Diferenciação Lag 02':
        return difference_time_series(time_series, 2) 
    elif transform_filter == 'Diferenciação Lag 01 + Diferenciação Lag 07':
        return difference_01_and_difference_07(time_series)
    else:
        return time_series