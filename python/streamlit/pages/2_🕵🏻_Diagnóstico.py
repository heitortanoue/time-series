import streamlit as st 
import pandas as pd
import functions.backend.sessionState as sessionState
import functions.frontend.sidebar as sidebar
import functions.utils.columns as columns 
import functions.frontend.analise.lineChart as lineChart
import functions.frontend.diagnostico.windowing as windowSeries
import functions.frontend.diagnostico.decomposition as decomposition
import functions.frontend.diagnostico.autocorrelation as autocorrelation

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar(diagnostico=True)

#PAGE STARTS HERE
st.markdown("# Diagnósticos dos dados" ) 

#DATAFRAME PLACEHOLDER 
with st.expander("📈 Tabela com os dados"):
    dataframe_placeholder = st.empty()
    # dataframe_placeholder.dataframe(filtered_df)


textWarning = """Nesta seção, é possível realizar um estudo de diagnóstico da série selecionada. Desse modo, é possível realizar a decomposição da série em suas componentes de Tendência, Sazonalidade e Ruído.\n
Além disso também é disponibilizado o correlograma da série para estudos de possíveis modelos preditivos. """

if sessionState.get_state('downloaded_data') is not True:
    st.markdown(textWarning)
    st.warning("Faça o download dos dados antes de continuar")
elif sessionState.get_state('filter_lv') is None:
    st.markdown(textWarning)
    st.warning("Selecione os filtros antes de continuar")

else:
    locations = sidebar.get_locations()
    locations_str = ', '.join([location.split('-')[1] if '-' in location else location for location in locations])
    st.markdown(f"### {locations_str}")

    st.warning("Selecione apenas **uma variável** por vez")

    defaultVariables = ['deaths']
    variablesSelected = st.multiselect(
        "Selecione as variáveis que deseja analisar",
        options = columns.getVariableTranslationList(columns.getColumnGroups('serie_temporal')),
        default = columns.getVariableTranslationList(defaultVariables)
    )

    # Espaçador
    st.text("")

    variablesKeys = columns.getVariableKeyList(variablesSelected)

    st.markdown("### Gráfico de Linha")
    lineChartDf = filtered_df.copy()

    print(lineChartDf.dtypes)

    lineChartDf = lineChartDf.rename(columns=columns.getVariableTranslationDict())

    lineChart.draw(lineChartDf, variablesSelected)

    #Definindo janela de tempo
    window = sidebar.get_window_time()
    decomposition_model = sidebar.get_decomposition_model()
    windowedDf = windowSeries.resample_time_series(lineChartDf, value_column=variablesSelected, time_window=window, time_column='Data') 
   
   #Plotando a série decomposta
    st.markdown("## Decompondo a Série Temporal")
    lag = sidebar.get_differentiation_lag() 
    decomposition.filter_and_plot_decomposition(windowedDf, lags=lag, model=decomposition_model) 

    #Plotando a Autocorrelacao 
    st.markdown("## Autocorrelação") 
    autocorrelation.plot_autocorrelation(windowedDf)
    
