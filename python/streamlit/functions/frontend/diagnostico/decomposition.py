import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose
from .differentiation import *
import functions.backend.sessionState as sessionState

def decomposition_filter():
    decompose_filter = st.selectbox(
    'Selecione o modelo de decomposição da série',
    ('Aditivo', 'Multiplicativo'))

    if decompose_filter == 'Aditivo':
        sessionState.set_state('decomposition_model', 'additive')
    elif decompose_filter == 'Multiplicativo':
        sessionState.set_state('decomposition_model', 'multiplicative')
    else:
        sessionState.set_state('decomposition_model', 'additive')

    return decompose_filter

def make_proper_time_series(time_series: pd.Series):
    """
    Make a time series proper for decomposition.

    Parameters:
    - time_series (pd.Series): Time series to be decomposed.

    Returns:
    - pd.Series: Proper time series for decomposition.
    """

    if time_series.empty is None:
        st.warning("Selecione uma série temporal para decompor")
        return

    # Perform seasonal decomposition
    if not isinstance(time_series.index, pd.DatetimeIndex):
        time_series = time_series.set_index('Data')
        time_series.index = pd.to_datetime(time_series.index)

    # Set frequency of time series
    if time_series.index.freq is None:
        time_series = time_series.asfreq('D')  # 'D' for daily. Adjust as needed.
    else:
        time_series = time_series.asfreq(sessionState.get_state('window'))

    # Fill missing values with last valid observation
    time_series.ffill(inplace=True)  # Forward fill

    ts_positive = time_series + 1 - time_series.min()

    return ts_positive

def filter_and_plot_decomposition(prev_time_series, lags=None):
    """
    Plot the decomposed series of a differenced time series.

    Parameters:
    - time_series (pd.Series): Differenced time series to be decomposed.
    - lags (int): Number of lags for differencing (default is 1).
    - model (str): Decomposition method: 'additive' or 'multiplicative'.

    Returns:
    - None
    """


    #Create difference and decomposition filters
    col1, col2 = st.columns(2)

    with col1:
        time_series = transformation_picker((prev_time_series))
    with col2:
        decomposition_filter()

    model = sessionState.get_state('decomposition_model')

   # Seasonal Decompose
    try:
        decomposition = seasonal_decompose(make_proper_time_series(time_series), model=model, period=52)
    except ValueError as e:
        st.error(f"Error in decomposition: {e}")
        return

    if lags is not None:

        plt.figure(figsize=(12, 8))

        plt.subplot(5, 1, 1)
        plt.plot(time_series, label='Série Original')
        plt.title('Série Temporal Original')

        plt.subplot(5, 1, 2)
        plt.plot(difference_time_series(time_series, lags=lags), label=f'Série Diferenciada (lags={lags})')
        plt.title('Série Temporal Diferenciada')

        plt.subplot(5, 1, 3)
        plt.plot(decomposition.trend, label='Tendência')
        plt.title('Componente de Tendência')

        plt.subplot(5, 1, 4)
        plt.plot(decomposition.seasonal, label='Sazonalidade')
        plt.title('Componente de Sazonalidade')

        plt.subplot(5, 1, 5)
        plt.plot(decomposition.resid, label='Resíduos')
        plt.title('Componente de Resíduos')

        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt, clear_figure=True)

    else:

        plt.figure(figsize=(12, 8))

        plt.subplot(4, 1, 1)
        plt.plot(time_series, label='Série Original')
        plt.title('Série Temporal Transformada')

        plt.subplot(4, 1, 2)
        plt.plot(decomposition.trend, label='Tendência')
        plt.title('Componente de Tendência')

        plt.subplot(4, 1, 3)
        plt.plot(decomposition.seasonal, label='Sazonalidade')
        plt.title('Componente de Sazonalidade')

        plt.subplot(4, 1, 4)
        plt.plot(decomposition.resid, label='Resíduos')
        plt.title('Componente de Resíduos')

        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt, clear_figure=True)

    return decomposition.resid.dropna()