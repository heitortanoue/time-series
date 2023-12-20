import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot 
from statsmodels.graphics.tsaplots import plot_acf

def residual_analysis(residual:pd.Series):

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(13,6.5))

    # plot[1,1]
    residual.plot(ax=axs[0,0])
    axs[0,0].set_title("Resíduos");

    # plot
    sns.distplot(residual, ax=axs[0,1]);
    axs[0,1].set_title("Densidade - Resíduos");

    # # plot
    qqplot(residual, line='q', fit=True, ax=axs[1,0])
    axs[1,0].set_title('Q-Q Plot ')

    # plot
    plot_acf(residual,  lags=35, ax=axs[1,1],color="fuchsia", auto_ylims=True)
    axs[1,1].set_title("Autocorrelação");

    st.pyplot(fig)