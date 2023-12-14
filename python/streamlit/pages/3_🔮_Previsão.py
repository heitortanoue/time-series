import streamlit as st 
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import functions.backend.sessionState as sessionState
import functions.utils.columns as columns
import functions.frontend.sidebar as sidebar
import functions.frontend.diagnostico.differentiation as differentiation
import functions.frontend.analise.lineChart as lineChart

# Texto superior na página
st.markdown("# Modelos e Previsões" ) 

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar(diagnostico=True, cumulative=False) #nao usar dados cumulativos para previsao
filtered_df = filtered_df.rename(columns=columns.getVariableTranslationDict()) 

textWarning = 'Colocar textinho'
if sessionState.get_state('downloaded_data') is not True:
    st.markdown(textWarning)
    st.warning("Faça o download dos dados antes de continuar")
elif sessionState.get_state('filter_lv') is None:
    st.markdown(textWarning)
    st.warning("Selecione os filtros antes de continuar")
elif sessionState.get_state('window') is None:
    st.markdown(textWarning)
    st.warning('Selecione uma janela de tempo adequada')
elif filtered_df is None or filtered_df.empty:
    st.markdown(textWarning)
    st.warning("Não há dados para serem analisados")
else:

    col_1_1, col_1_2 = st.columns(2)

    with col_1_1:
        # Define as variaveis que serão usadas para treinar o modelo
        variablesSelected = st.selectbox(
        "Selecione a variável que deseja modelar",
        options = columns.getVariableTranslationList(columns.getColumnGroups('variaveis'))
                )
        variablesKeys = columns.getVariableKeyList(variablesSelected)  

        lineChart.draw(filtered_df, [variablesSelected], legend=None, title=f"Série Original - {variablesSelected}")

    with col_1_2:
        #Filtro de transformação
        filtered_df_stationary = filtered_df.copy()
        stationarity_time_series = differentiation.transformation_picker(filtered_df[variablesSelected]).to_frame()
        filtered_df_stationary[variablesSelected] = stationarity_time_series[variablesSelected]
        lineChart.draw(filtered_df_stationary, [variablesSelected], legend=None, title=f"Série Transformada - {variablesSelected}")

    st.markdown("## Modelagem")

    col_2_1, col_2_2 = st.columns(2) 

    # with col_2_1:
    #     # Define as variaveis que serão usadas para treinar o modelo
    #     variablesSelected = st.selectbox(
    #     "Selecione a variável que deseja modelar",
    #     options = columns.getVariableTranslationList(columns.getColumnGroups('variaveis'))
    #             )
    #     variablesKeys = columns.getVariableKeyList(variablesSelected)

    # df_to_use = filtered_df[variablesKeys] 

    with col_2_1:
        #Filtro de divisao de dados em treino e teste 
        proportion = st.number_input("Defina a proporção entre Treino e Teste", format="%d", min_value = 1, max_value = 99, value  = 80)
        train_size = int((proportion/100)*len(stationarity_time_series))
        train, test = stationarity_time_series[:train_size], stationarity_time_series[train_size:]

    with col_2_2:
        # Filtro de selecao de modelos
        model_names = ["Autoregressivo", "Médias Móveis", "ARIMA", "SARIMA"]
        model_name = st.selectbox("Qual modelo você deseja utilizar?", model_names)
        

    # Parametros que os modelos utilizam
    dict_params = {"Autoregressivo":["p"], "Médias Móveis":["q"], "ARIMA":["p", "d", "q"], "SARIMA":["p", "d", "q", "s"]}

    # Funcoes para os modelos
    dict_functions = {"Autoregressivo":AutoReg, "Médias Móveis":ARIMA,  "ARIMA":ARIMA, "SARIMA":SARIMAX}

    # Coloca os parametros do modelo para o usuario selecionar
    params_name = dict_params[model_name]

    st.markdown(f"### Modelo {model_name.title()}")

    actual_params = {}
    for param in params_name:
        actual_params[param] = st.number_input(f"Parametro {param}", format = "%d", min_value = 1)

    # model = None
    # # Treina os modelos
    # if model_name == "AR":
    #     model = AutoReg(train['deaths'], lags=(actual_params["p"]))
    # #Falta acabar de implementar
    # #elif model_name in ("ARIMA", "SARIMA"):
    # #    model = dict_functions[model_name](train, order=list(actual_params.values()))
    # result = model.fit()

    # # Faz as predições
    # predict = result.predict(start=test.index[0], end=test.index[-1], dynamic=False)
        