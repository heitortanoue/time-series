import pandas as pd
import streamlit as st
import functions.backend.sessionState as sessionState

def difference_filter():
    diff_filter = st.selectbox(
    'Selecione um lag para ver a decomposição da série diferenciada',
    ('Série Original', 'Lag 01', 'Lag 02')) 

    if diff_filter == 'Lag 01':
        sessionState.set_state('lag', 1) 
    elif diff_filter == 'Lag 02':
        sessionState.set_state('lag',2) 
    else:
        sessionState.set_state('lag', None)

    return diff_filter

def difference_time_series(time_series:pd.DataFrame, lags:int=1):
    """
    Perform differencing on a time series.

    Parameters:
    - time_series (pd.Series): Time series to be differenced.
    - lags (int): Number of lags for differencing (default is 1).

    Returns:
    - pd.Series: Differenced time series.
    """
    return time_series.diff(lags).dropna()