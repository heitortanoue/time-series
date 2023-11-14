import pandas as pd
import streamlit as st
import altair as alt

import functions.backend.sessionState as sessionState
import functions.utils.columns as columns

def draw(df, keys):
    filter_lv = sessionState.get_state('filter_lv')

    # Agrupar e somar os dados por país
    if filter_lv == 1:
        groupVariable = 'administrative_area_level_1'
    elif filter_lv == 2:
        groupVariable = 'administrative_area_level_2'
    else:
        groupVariable = 'administrative_area_level_3'

    allowedVariables = columns.getColumnGroups('variaveis')
    filtered_variables = [groupVariable] + [var for var in allowedVariables if var in keys]

    df_group = df.copy()[filtered_variables]

    # Renomear a coluna de nível administrativo
    df_group = df_group.rename(columns={groupVariable: 'location'})

    # Trocar variaveis para seu nome traduzido
    df_group = df_group.rename(columns=columns.getVariableTranslationDict())

    grouped = df_group.groupby('location').sum().reset_index()

    # Reformatar o DataFrame para criar um gráfico de barras horizontais
    melted = pd.melt(grouped, id_vars='location', var_name='variavel', value_name='valor')

    barChart = alt.Chart(melted).mark_bar().encode(
        y=alt.Y('variavel', title=None),
        x=alt.X('valor', title=None),
        color=alt.Color('location', title=None),
        yOffset='location'
    ).configure_legend(
        orient="bottom",
        symbolLimit=0
    )

    st.altair_chart(barChart, use_container_width=True)