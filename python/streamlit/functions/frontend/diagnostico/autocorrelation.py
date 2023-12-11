from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def test_stationarity(time_series):
    """
    Perform Augmented Dickey-Fuller test to check stationarity of the time series.
    """
    result = adfuller(time_series)
    adf_statistic = result[0]
    p_value = result[1]
    critical_values = result[4]

    # Display the results
    st.write(f'ADF Statistic: {adf_statistic}')
    st.write(f'p-value: {p_value}')
    for key, value in critical_values.items():
        st.write(f'Critical Value ({key}): {value}')

    if p_value < 0.05:
        st.write(":green[The series is stationary.]")
    else:
        st.write(":red[The series is not stationary. Consider differencing or transforming the series.]")

def apply_transformation(time_series):
    """
    Apply transformation to time series.
    """
    transformed_series = np.log(time_series)
    return transformed_series


def plot_autocorrelation(time_series, lags=None):
    """
    Plot the autocorrelation of a time series.

    Parameters:
    - time_series (pd.Series): Time series for autocorrelation plotting.
    - lags (int): Number of lags to include in the plot (default is None).

    Returns:
    - None
    """


    # time_series = time_series.set_index('Data')

    if lags is not None:
        fig, ax = plt.subplots(figsize=(6,2))
        plot_acf(time_series, lags, auto_ylims=True, ax=ax, title=f'Autocorrelação com Lag {lags}')
        st.pyplot(fig, clear_figure=True, use_container_width=False)
    else:
        fig , ax = plt.subplots(figsize=(5,3))
        plot_acf(time_series, auto_ylims=True, ax=ax, title = "Autocorrelação")
        st.pyplot(fig, clear_figure=True, use_container_width=True) 

def plot_partial_autocorrelation(time_series, lags=None, fig_size=(10,8)):
    """
    Plot the partial autocorrelation of a time series.

    Parameters:
    - time_series (pd.Series): Time series for partial autocorrelation plotting.
    - lags (int): Number of lags to include in the plot (default is None).

    Returns:
    - None
    """

    if lags is not None:
        fig, ax = plt.subplots(figsize=(5,3))
        plot_pacf(time_series, lags=lags, auto_ylims=True, ax=ax, title=f'Autocorrelação Parcial com {lags} diferença')
        st.pyplot(fig, clear_figure=True, use_container_width=False)
    else:
        fig, ax = plt.subplots(figsize=(5,3))
        plot_pacf(time_series, auto_ylims=True, ax=ax, title="Autocorrelação Parcial")
        st.pyplot(fig, clear_figure=True, use_container_width=True)
