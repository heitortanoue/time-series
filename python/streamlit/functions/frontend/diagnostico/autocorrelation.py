from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import streamlit as st

def plot_autocorrelation(time_series, lags=None):
    """
    Plot the autocorrelation of a time series.

    Parameters:
    - time_series (pd.Series): Time series for autocorrelation plotting.
    - lags (int): Number of lags to include in the plot (default is None).

    Returns:
    - None
    """

    time_series = time_series.set_index('Data')

    if lags is not None:
        
        plot_acf(time_series, lags)
        plt.title(f'Autocorrelação com Lag {lags}')
        st.pyplot(plt, clear_figure=True)
    else:
        plot_acf(time_series)
        plt.title('Autocorrelação')
        st.pyplot(plt, clear_figure=True)

 