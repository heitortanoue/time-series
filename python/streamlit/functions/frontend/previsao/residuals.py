import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot 
from statsmodels.graphics.tsaplots import plot_acf
from scipy.stats import jarque_bera 
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import breakvar_heteroskedasticity_test

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

def residuals_tests(model_selected, model_fit, resids):
    st.markdown("## Testes 🧪")
    if 'Autoregressivo' not in model_selected:
        # Aplicar o Teste de Jarque-Bera
        if(callable(model_fit.resid)):
            residuos = model_fit.resid()
        else:
            residuos = model_fit.resid
    else:
        residuos = resids
    estatistica, p_valor = jarque_bera(residuos)
    st.markdown("### Teste de Jarque-Bera - Normalidade dos Resíduos")
    # Exibir os resultados
    st.markdown(f"**Estatística do teste de Jarque-Bera:** {str(estatistica)}")
    st.markdown(f"**Valor p:** {str(p_valor)}")
    # Testar a hipótese nula de que os resíduos têm uma distribuição normal
    if p_valor > 0.05:
        st.success("Os resíduos parecem seguir uma distribuição normal (não podemos rejeitar a hipótese nula)", icon="✅")
    else:
        st.warning("Os resíduos não seguem uma distribuição normal (rejeitamos a hipótese nula)", icon="⚠️")

    # Aplicar o teste de LjungBox para independência dos resíduos
    df = acorr_ljungbox(residuos, lags=10).rename(columns={'lb_stat':'Estatisticas','lb_pvalue':'P-Valores'})
    # Exibir os resultados
    st.markdown("### Teste de Ljung-Box - Autocorrelação Serial")
    st.markdown('#### Estatísticas e P-Valores associados ao teste de Ljung-Box')
    st.dataframe(df.transpose())
    # Testar a hipótese nula de independência dos resíduos
    if any(df['P-Valores'] < 0.05):
        st.warning("Os resíduos não são independentes (rejeitamos a hipótese nula)", icon="⚠️")
    else:
        st.success("Os resíduos são independentes (não podemos rejeitar a hipótese nula)", icon="✅") 

    # Aplicar o teste de homocedaticidade dos resíduos 
    st.markdown("### Teste de Homocedasticidade dos Resíduos")
    estatistica, p_valor = breakvar_heteroskedasticity_test(residuos)
    # Exibir os resultados
    st.markdown(f"**Estatística do teste de homocedasticidade:** {str(estatistica)}")
    st.markdown(f"**Valor p:** {str(p_valor)}")
    # Testar a hipótese nula de que os resíduos têm uma distribuição normal
    if p_valor > 0.05:
        st.success("Os resíduos parecem ser homocedásticos (não podemos rejeitar a hipótese nula)", icon="✅")
    else:
        st.warning("Os resíduos são heterocedásticos (rejeitamos a hipótese nula)", icon="⚠️")