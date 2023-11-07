import pandas as pd
import streamlit as st
import altair as alt

import functions.backend.sessionState as sessionState
import functions.utils.columns as columns

def draw(df, keys):
    print(df.columns)
    
    filter_lv = sessionState.get_state('filter_lv')
    
    # Agrupar e somar os dados por país
    if filter_lv == 1:
        groupVariable = 'administrative_area_level_1'
    elif filter_lv == 2:
        groupVariable = 'administrative_area_level_2'
    else:
        groupVariable = 'administrative_area_level_3'

    allowedVariables = ['Confirmados', 'Mortes', 'Recuperados', 'Testes Realizados', 'Doses de Vacina', 'Pessoas Vacinadas (Pelo Menos uma Dose)', 'Pessoas Totalmente Vacinadas', 'Hospitalizados', 'Em UTI', 'Com Ventilação Invasiva', 'População']
    filtered_variables = [var for var in allowedVariables if var in keys]
    print(filtered_variables)
    political_variables = list(set(df.columns) - set(allowedVariables))
    political_variables = [column for column in political_variables if column in keys]
    print(political_variables)
    df_group = df[filtered_variables + political_variables + [columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)]].copy()


    # Trocar variaveis para seu nome traduzido
    df_group = df_group.rename(columns=columns.getVariableTranslationDict())

    numerical_df = df_group[filtered_variables + [columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)]].copy()
    political_df = df_group[political_variables].copy().diff()
    df = pd.concat([numerical_df, political_df.add_suffix('_diff')], axis=1).copy()
    
    numerical_df = numerical_df.melt(id_vars=[columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)], var_name = "Categoria", value_name = "Valor").copy()
    numerical_df['Categoria'] = numerical_df['Categoria'] +' - ' +  numerical_df[columns.getVariableTranslation(groupVariable)]

    print(df)

    barChart = alt.Chart(numerical_df).mark_line().encode(
        y=alt.Y('Valor', title=None),
        x=alt.X(columns.getVariableTranslation('date'), title=None),
        color=alt.Color("Categoria", title=None),
        yOffset="Categoria"
    )


    rule_charts = []
    for column in political_variables:
        column += "_diff"
        serie = df[column]
        up_series = df[serie > 0].copy()
        down_series = df[serie < 0].copy()
        rule_charts.append(alt.Chart(up_series).mark_rule(color='red').encode(
            x=columns.getVariableTranslation('date'),
            tooltip=columns.getVariableTranslation(groupVariable)
        ))

        rule_charts.append(alt.Chart(down_series).mark_rule(color='green').encode(
            x=columns.getVariableTranslation('date'),
            tooltip=columns.getVariableTranslation(groupVariable)
        ))

    for chart in rule_charts:
        barChart += chart
        
    st.altair_chart(barChart, use_container_width=True)