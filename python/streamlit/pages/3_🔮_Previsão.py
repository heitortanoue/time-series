import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *
from functions.filterFunctions import *
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


import functions.backend.sessionState as sessionState
import functions.utils.columns as columns
import functions.frontend.sidebar as sidebar

# Texto superior na página
st.markdown("# Modelos e Previsões" ) 
st.markdown("""Texto e mais texto\n
            Essa página deve conter os modelos de previsão das séries temporais.
            **O usuário deve ter controle sobre os parâmetros do modelo escolhido**
            Filtradas em quaisquer um dos níveis e por data.
            O filtro de data ainda não foi implementado""")  

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])
# Mostra a sidebar
filtered_df = sidebar.get_sidebar()
textWarning = 'Colocar textinho'
if sessionState.get_state('downloaded_data') is not True:
    st.markdown(textWarning)
    st.warning("Faça o download dos dados antes de continuar")
elif sessionState.get_state('filter_lv') is None:
    st.markdown(textWarning)
    st.warning("Selecione os filtros antes de continuar")

else:
    # Nomes dos Modelos
    model_names = ["AR", "ARIMA", "SARIMA"]
    # Parametros que os modelos utilizam
    dict_params = {"AR":["p"], "ARIMA":["p", "d", "q"], "SARIMA":["p", "d", "q", "s"]}

    # Funcoes para os modelos
    dict_functions = {"AR":AutoReg, "ARIMA":ARIMA, "SARIMA":SARIMAX}

    # Adiciona a dropdown dos modelos
    model_name = st.selectbox("Qual modelo você deseja utilizar?", model_names)

    # Coloca os parametros do modelo para o usuario selecionar
    params_name = dict_params[model_name]

    actual_params = {}
    for param in params_name:
        actual_params[param] = st.number_input(f"Parametro {param}", format = "%d", min_value = 1)

    # Coloca as variaveis que serão usadas para treinar o modelo
    defaultVariables = ['confirmed', 'deaths', 'recovered']
    variablesSelected = st.multiselect(
        "Selecione as variáveis que deseja usar no modelo",
        options = columns.getVariableTranslationList(columns.getColumnGroups('serie_temporal')),
        default = columns.getVariableTranslationList(defaultVariables)
    )
    variablesKeys = columns.getVariableKeyList(variablesSelected)
    df_to_use = filtered_df[variablesKeys]

    proportion = st.number_input("Defina a proporção entre Treino e Teste", format="%d", min_value = 1, max_value = 99, value  = 50)
    train_size = int((proportion/100)*len(df_to_use))
    train, test = df_to_use[:train_size], df_to_use[train_size:]

    model = None
    # Treina os modelos
    if model_name == "AR":
        model = AutoReg(train['deaths'], lags=(actual_params["p"]))
    #Falta acabar de implementar
    #elif model_name in ("ARIMA", "SARIMA"):
    #    model = dict_functions[model_name](train, order=list(actual_params.values()))
    result = model.fit()

    # Faz as predições
    predict = result.predict(start=test.index[0], end=test.index[-1], dynamic=False)
        