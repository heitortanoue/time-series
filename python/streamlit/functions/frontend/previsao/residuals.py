import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot 
from statsmodels.graphics.tsaplots import plot_acf

def residual_analysis(residual:pd.DataFrame):

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,10))

    # plot[1,1]
    residual.plot(ax=axs[0,0])
    axs[0,0].set_title("Residuals");

    # plot
    sns.distplot(residual, ax=axs[0,1]);
    axs[0,1].set_title("Density plot - Residual");

    # # plot
    qqplot(residual['residuals'], line='q', fit=True, ax=axs[1,0])
    axs[1,0].set_title('Plot Q-Q')

    # plot
    plot_acf(residual,  lags=35, ax=axs[1,1],color="fuchsia", auto_ylims=True)
    axs[1,1].set_title("Autocorrelation");

    plt.show()