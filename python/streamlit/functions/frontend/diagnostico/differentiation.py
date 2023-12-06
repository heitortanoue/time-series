import pandas as pd
import numpy as np
from scipy.stats import boxcox
import streamlit as st

def log_transform(time_series: pd.Series):
    # remove zeros
    time_series = time_series.replace(0, np.nan).dropna()
    return np.log(time_series).dropna()

def boxcox_transform(time_series: pd.Series):
    """
    Apply Box-Cox transformation to a time series.

    Parameters:
    - time_series (pd.Series): Time series to transform.

    Returns:
    - pd.Series: Box-Cox transformed time series.
    """
    # Adicionar uma constante para evitar valores zero ou negativos
    ts_positive = time_series + 1 - time_series.min()

    # Tenta aplicar a transformação Box-Cox
    try:
        transformed, _ = boxcox(ts_positive['Valor'])
        return pd.Series(transformed, index=ts_positive.index)
    except Exception as e:
        st.error(f'Erro ao aplicar a transformação Box-Cox: {e}')
        return time_series



def difference_time_series(time_series: pd.Series, lags: int = 1):
    return time_series.diff(lags).dropna()

def transformation_picker(time_series: pd.Series):
    transform_filter = st.selectbox(
        'Selecione uma transformação para aplicar à série temporal',
        ('Série Original', 'Logarítmica', 'Box-Cox', 'Diferenciação Lag 01', 'Diferenciação Lag 02'))

    if transform_filter == 'Logarítmica':
        return log_transform(time_series)
    elif transform_filter == 'Box-Cox':
        return boxcox_transform(time_series)
    elif transform_filter == 'Diferenciação Lag 01':
        return difference_time_series(time_series, 1)
    elif transform_filter == 'Diferenciação Lag 02':
        return difference_time_series(time_series, 2)
    else:
        return time_series