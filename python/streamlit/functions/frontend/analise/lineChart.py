import pandas as pd
import streamlit as st
import altair as alt
from typing import Optional

import functions.backend.sessionState as sessionState
import functions.utils.columns as columns

def draw(df, keys, title:Optional[str|None], legend:Optional[str]):
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

    political_variables = list(set(df.columns) - set(allowedVariables))
    political_variables = [column for column in political_variables if column in keys]

    df_group = df[filtered_variables + political_variables + [columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)]].copy()


    # Trocar variaveis para seu nome traduzido
    df_group = df_group.rename(columns=columns.getVariableTranslationDict())

    numerical_df = df_group[filtered_variables + [columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)]].copy()
    political_df = df_group[political_variables].copy().diff()
    df = pd.concat([numerical_df, df_group[political_variables], political_df.add_suffix('_diff')], axis=1).copy()

    numerical_df = numerical_df.melt(id_vars=[columns.getVariableTranslation('date'), columns.getVariableTranslation(groupVariable)], var_name = "Categoria", value_name = "Valor").copy()
    numerical_df['Categoria'] = numerical_df['Categoria'] +' - ' +  numerical_df[columns.getVariableTranslation(groupVariable)]


    if legend is None:
        barChart = alt.Chart(numerical_df, title=f"{title}").mark_line().encode(
            alt.Color("Categoria").legend(None),
            y=alt.Y('Valor', scale=alt.Scale(domainMin=0)),
            x=alt.X(columns.getVariableTranslation('date'), title=None, axis=alt.Axis(format='%d/%m/%Y', labelPadding=30)),
            yOffset="Categoria",
        )

    else:
        barChart = alt.Chart(numerical_df).mark_line().encode(
            y=alt.Y('Valor', scale=alt.Scale(domainMin=0)),
            x=alt.X(columns.getVariableTranslation('date'), title=None, axis=alt.Axis(format='%d/%m/%Y', labelPadding=30)),
            color=alt.Color("Categoria"),
            yOffset="Categoria"
        )

    # Criar gráficos com rótulos
    rule_charts = []
    for column in political_variables:
        column_diff = column + "_diff"
        serie_diff = df[column_diff]
        serie = df[column]
        up_series = df[(serie_diff != 0) & (serie >= 0)].copy()
        down_series = df[(serie_diff != 0) & (serie < 0)].copy()

        # modulo na down_series
        down_series[column] = down_series[column].abs()

        # Regras aplicadas pelo governo federal
        up_chart = alt.Chart(up_series).mark_rule(color='orange').encode(
            x=columns.getVariableTranslation('date'),
            tooltip=columns.getVariableTranslation(groupVariable)
        )
        rule_charts.append(add_text_labels(up_chart, up_series, 'orange', column))

        # Regras aplicadas pelos governos locais
        down_chart = alt.Chart(down_series).mark_rule(color='green').encode(
            x=columns.getVariableTranslation('date'),
            tooltip=columns.getVariableTranslation(groupVariable)
        )
        rule_charts.append(add_text_labels(down_chart, down_series, 'green', column))

    # Combinar os gráficos
    for rule_chart in rule_charts:
        barChart += rule_chart

    # Exibir o gráfico no Streamlit
    st.altair_chart(barChart, use_container_width=True)

    st.markdown('#### Legenda')
    st.markdown(':orange[Linhas laranjas] representam regras aplicadas pelo governo federal, enquanto as :green[verdes] representam regras aplicadas pelos governos locais.')
    for column in political_variables:
        st.markdown(f"##### {column}")
        enums = columns.getVariableEnumTranslationList(columns.getVariableKey(column))

        # Pega a key e o valor da variável enum e mostra na tela {0: 'alo'}: 0 -> alo
        for key, value in enums.items():
            st.markdown(f"- **{key}**: {value}")

# Função para adicionar rótulos de texto ao gráfico
def add_text_labels(chart, series, color, column):
    text_chart = alt.Chart(series).mark_text(
        align='center',
        baseline='bottom',
        dy=20,
        fontSize=14  # Ajuste o tamanho do texto
    ).encode(
        x=columns.getVariableTranslation('date'),
        y=alt.Y(column, axis=alt.Axis(title='')),
        text=alt.Text(column),  # Exibe o nome da variável e seu valor
        color=alt.value(color)  # Define a cor do texto
    )
    return chart + text_chart