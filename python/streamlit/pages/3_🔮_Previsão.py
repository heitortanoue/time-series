import streamlit as st
import functions.backend.sessionState as sessionState
import functions.utils.columns as columns
import functions.frontend.sidebar as sidebar
import functions.frontend.diagnostico.differentiation as differentiation
import functions.frontend.analise.lineChart as lineChart
import functions.frontend.previsao.models as models
import functions.frontend.previsao.residuals as residuals
from scipy.stats import jarque_bera
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import breakvar_heteroskedasticity_test

# Texto superior na página
st.markdown("# Modelos e Previsões" )

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar(diagnostico=True, cumulative=False) #nao usar dados cumulativos para previsao

textWarning = """
Aqui, exploramos análises preditivas dos dados da COVID-19. Combinando técnicas avançadas de séries temporais, o trabalho permite que os usuários interajam com o modelo, escolhendo variáveis específicas para entender a evolução da pandemia.
Esta abordagem dinâmica realça a flexibilidade e precisão dos modelos preditivos em antecipar tendências de saúde pública, enfatizando a importância da análise de dados e tecnologia no contexto de uma crise de saúde global.
"""
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

    filtered_df = filtered_df.rename(columns=columns.getVariableTranslationDict())
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

    with col_2_1:
        #Filtro de divisao de dados em treino e teste
        proportion = st.number_input("Defina a proporção entre Treino e Teste", format="%d", min_value = 1, max_value = 99, value  = 80)
        train_size = int((proportion/100)*len(filtered_df))
        train, test = filtered_df[:train_size], filtered_df[train_size:]

    with col_2_2:
        # Filtro de selecao de modelos
        model_names = ["Autoregressivo", "Autoregressivo - Busca Automática", "Médias Móveis","ARMA", "ARIMA", "ARIMA - Busca Automática (AutoARIMA)", "SARIMA"]
        automatic_models = ["Autoregressivo - Busca Automática", "ARIMA - Busca Automática (AutoARIMA)"]
        params_models = ["Autoregressivo", "Médias Móveis", "ARIMA", "SARIMA"]

        model_selected = st.selectbox("Qual modelo você deseja utilizar?", model_names)

    st.markdown(f"### Modelo {model_selected.title()}")

    # Parametros que os modelos utilizam
    dict_params = {"Autoregressivo":["lags"],
                   "Médias Móveis":["q"],
                   "ARMA":["p", "q"],
                   "ARIMA":["p", "d", "q"],
                   "SARIMA":["p", "d", "q", "s"]}

    #Modelos
    models_functions = {
        "Autoregressivo": (models.AutoRegressiveModel),
        "Autoregressivo - Busca Automática": (models.AutoRegressiveModel, {"lags":None, "max_lags":20}),
        "Médias Móveis": models.MovingAverageModel,
        "ARMA": models.ARMAModel,
        "ARIMA": (models.ARIMAModel, {"auto":False}),
        "ARIMA - Busca Automática (AutoARIMA)": (models.ARIMAModel, {"auto":True}),
        "SARIMA": models.SARIMAModel
    }


    #Seleciona parametros do modelos nao-automaticos
    if model_selected in dict_params:
        params_name = dict_params[model_selected]

        actual_params = {}
        for param in params_name:
            actual_params[param] = st.number_input(f"Parametro {param}", format = "%f")

    try:
        #Modelos Automaticos
        if model_selected in automatic_models:
            #Seleciona Seleciona parametros do modelos automaticos
            selected_function, automatic_args = models_functions[model_selected]
            #Caso especial AutoARIMA
            if model_selected == "ARIMA - Busca Automática (AutoARIMA)":
                model_fit, forecast_values, conf_int, resids, model_order = selected_function(train = train[variablesSelected].fillna(0), steps=len(test), **automatic_args)
            else:
                model_fit, forecast_values, conf_int, resids = selected_function(train = train[variablesSelected].fillna(0), steps=len(test), **automatic_args)

            #Plotando os Resultados
            models.plot_test_data_forecast(test[variablesSelected], forecasts = forecast_values, conf_int = conf_int)

        else:
            selected_function = models_functions[model_selected]
            model_fit, forecast_values, conf_int, resids = selected_function(train=train[variablesSelected].fillna(0),
                                                                        steps=len(test), **actual_params)

            #Plotando os Resultados
            models.plot_test_data_forecast(test[variablesSelected], forecasts = forecast_values, conf_int = conf_int)

        #Diagnóstico dos Resíduos
        st.markdown("## Análise dos Resíduos 🔎")

        #Gráfico de Diagnóstico dos Resíduos
        residuals.residual_analysis(resids)

        # #Testes dos residuos
        residuals.residuals_tests(model_selected, model_fit, resids)
    except Exception as e:
        st.error(f"Erro na modelagem: {e}")