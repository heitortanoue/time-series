import streamlit as st
import functions.backend.sessionState as sessionState
import functions.frontend.sidebar as sidebar
import functions.utils.columns as columns
import functions.frontend.analise.barChart as barChart
import functions.frontend.analise.insights as insights
import functions.frontend.analise.lineChart as lineChart


# Variável de estado que vamos usar nessa página
sessionState.using_state(['downloaded_data'])

# Mostra a sidebar
filtered_df = sidebar.get_sidebar()

# PAGE STARTS HERE
st.markdown("# Análises")

textWarning = 'Nesta seção, convidamos você a realizar uma análise exploratória dos dados de COVID-19. A análise exploratória é uma etapa fundamental para compreender as tendências e padrões nos dados, proporcionando insights valiosos sobre o impacto da pandemia. Para começar, selecione as regiões geográficas de interesse e as variáveis que deseja analisar. Explore os gráficos interativos, personalize a visualização conforme suas preferências e interprete os dados em busca de conclusões relevantes. Compartilhe suas descobertas e insights para contribuir para uma compreensão mais aprofundada da situação da COVID-19'

#Overview Dataframe placeholder 
with st.expander("📈 Tabela com os dados completos por nível"):
    st.info("Utilize essa tabela para comparações entre todos os países", icon="ℹ️")
    dataframe_placeholder = st.empty()

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

    defaultVariables = ['confirmed', 'deaths', 'recovered']
    variablesSelected = st.multiselect(
        "Selecione as variáveis que deseja analisar",
        options = columns.getVariableTranslationList(columns.getColumnGroups('serie_temporal')),
        default = columns.getVariableTranslationList(defaultVariables)
    )

    # Espaçador
    st.text("")

    # Overview Dataframe
    filter_lv = sessionState.get_state('filter_lv')
    overview_df = insights.get_overviewDf(filter_lv, variablesSelected)
    dataframe_placeholder.dataframe(overview_df)

    variablesKeys = columns.getVariableKeyList(variablesSelected)

    barChartColumn, insightsColumn = st.columns(2, gap="large")

    with barChartColumn:
        barChart.draw(filtered_df, variablesKeys)

    with insightsColumn:
        insights.draw(locations, variablesKeys)

    st.markdown("### Gráfico de Linha")
    lineChartDf = filtered_df.copy()
    lineChartDf = lineChartDf.rename(columns=columns.getVariableTranslationDict())

    lineChart.draw(lineChartDf, variablesSelected, title="", legend=None)