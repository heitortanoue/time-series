import streamlit as st
import pandas as pd

import functions.backend.sessionState as sessionState
import functions.frontend.sidebar as sidebar
import functions.utils.columns as columns

# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar()

# PAGE STARTS HERE
st.markdown("# Análises" )

if sessionState.get_state('downloaded_data') is not True:
    st.warning("Faça o download dos dados antes de continuar")
elif filtered_df.empty:
    st.warning("Selecione os filtros antes de continuar")
else:
    variablesSelected = st.multiselect(
        "Selecione as variáveis que deseja analisar",
        options = columns.getAllVariablesTranslation()
    )

    variablesKeys = columns.getVariableKeyList(variablesSelected)

    pieChartColumn, insightsColumn = st.columns(2)

    with pieChartColumn:
        st.markdown("### Gráfico de Pizza")
        st.write("Aqui vai o gráfico de pizza")

    with insightsColumn:
        st.markdown("### Insights")
        st.write("Aqui vão os insights")

    st.markdown("### Gráfico de Linha")
    st.line_chart(filtered_df, x='date', y=variablesKeys)