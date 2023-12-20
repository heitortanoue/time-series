import streamlit as st
import pandas as pd
from typing import Union, Optional
import matplotlib.pyplot as plt 
import numpy as np
from statsmodels.tsa.ar_model import AutoReg, ar_select_order 
from statsmodels.tsa.arima.model import ARIMA 
from pmdarima.arima import auto_arima
import statsmodels.api as sm


def AutoRegressiveModel(train: pd.Series, steps, lags: Optional[Union[list[int], int]]=None, max_lags: Optional[int | None] = None):
    if lags is None:
        if max_lags is None:
            raise ValueError("argumento `max_lags` não pode ser vazio quando `lags` é vazio")
        # Realiza seleção automática de Lags
        selector = ar_select_order(train, maxlag=max_lags)
        ar_model = AutoReg(train, lags=selector.ar_lags)
        ar_model_fit = ar_model.fit()

        # Get forecast, confidence intervals and residuals
        forecast_results = ar_model_fit.get_prediction(start=len(train), end=len(train) + steps - 1, dynamic=False)
        forecast_values = forecast_results.predicted_mean
        confidence_intervals = forecast_results.conf_int() 
        residuals = ar_model_fit.resid

        return ar_model_fit, forecast_values, confidence_intervals, residuals

    else:
        if max_lags is not None:
            raise ValueError("O argumento `max_lags` deve ser usado apenas quando o argumento `lags` não é especificado")
        else:
            ar_model = AutoReg(train, lags=lags)
            ar_model_fit = ar_model.fit() 

            # Get forecast and confidence intervals
            forecast_results = ar_model_fit.get_prediction(start=len(train), end=len(train) + steps - 1, dynamic=False)
            forecast_values = forecast_results.predicted_mean
            confidence_intervals = forecast_results.conf_int()
            residuals = ar_model_fit.resid

            return ar_model_fit, forecast_values, confidence_intervals, residuals
        
def MovingAverageModel(train:pd.Series, q:int, steps:int):
    ma_model = ARIMA(endog=train, order=(0,0,q)).fit() 

    #Forecasts 
    forecasts = ma_model.get_forecast(steps=steps) 
    forecast_values = forecasts.predicted_mean 
    forecast_conf_int = forecasts.conf_int()
    residuals = ma_model.resid
    
    return ma_model, forecast_values, forecast_conf_int, residuals

def ARMAModel(train:pd.Series, p:int, q:int, steps:int):
    arma_model = ARIMA(endog=train, order=(p,0,q)).fit() 

    #Forecasts 
    forecasts = arma_model.get_forecast(steps=steps) 
    forecast_values = forecasts.predicted_mean 
    forecast_conf_int = forecasts.conf_int()
    residuals = arma_model.resid
    
    return arma_model, forecast_values, forecast_conf_int, residuals

def ARIMAModel(train: pd.Series, steps:int, p: Optional[int] = None, d: Optional[int] = None, q: Optional[int] = None, auto: bool = False):

    if auto:
        auto_arima_model = auto_arima(train, alpha=0.05, stepwise=True, n_jobs=-1)
        model_order = auto_arima_model.order 
        auto_arima_model_fit = auto_arima_model.fit(train) 

        # Forecast future values (adjust the forecast horizon as needed)
        forecast, conf_int = auto_arima_model_fit.predict(n_periods=steps, return_conf_int=True)
        conf_int = pd.DataFrame(conf_int)
        residuals = auto_arima_model_fit.resid()
        
        return auto_arima_model_fit, forecast, conf_int, residuals, model_order
    
    arima_model_fit = ARIMA(train, order=(p,d,q)).fit() 

    #Forecasts 
    forecasts = arima_model_fit.get_forecast(steps=steps) 
    forecast_values = forecasts.predicted_mean 
    forecast_conf_int = forecasts.conf_int()
    residuals = arima_model_fit.resid
    
    return arima_model_fit, forecast_values, forecast_conf_int, residuals

def SARIMAModel(train:pd.Series, steps, p = None, d = None, q = None, s = None):
    if s <= 1 or s is None:
        sarima_model_fit = sm.tsa.SARIMAX(train, order=(p,d,q)).fit()
    else:
        sarima_model_fit = sm.tsa.SARIMAX(train, seasonal_order=(p,d,q,s)).fit()

    #Forecasts 
    forecasts = sarima_model_fit.get_forecast(steps=steps) 
    forecast_values = forecasts.predicted_mean 
    forecast_conf_int = forecasts.conf_int()
    residuals = sarima_model_fit.resid

    return sarima_model_fit, forecast_values, forecast_conf_int, residuals

#Plotting Functions 

def plot_test_data_forecast(test:pd.Series, forecasts:pd.Series, conf_int:pd.DataFrame):
    # Plot the test data against the forecasted values
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(np.arange(len(test)), test, label='Dado de Teste', linestyle='--')
    ax.plot(np.arange(len(test)), forecasts, label='Previsão')
    ax.fill_between(np.arange(len(test)),
                    conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='gray', alpha=0.2, label='95% IC')
    ax.legend()
    st.pyplot(fig)