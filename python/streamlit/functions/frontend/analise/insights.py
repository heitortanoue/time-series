import pandas as pd
import streamlit as st
import altair as alt

import functions.backend.sessionState as sessionState
import functions.utils.columns as columns
import functions.dbFunctions as database

def draw(locations, keys):
    filter_lv = sessionState.get_state('filter_lv')

    # Obtém os dados apropriados dependendo do nível de filtro
    if filter_lv == 1:
        data = database.getLvl1Data()
        groupVariable = 'administrative_area_level_1'
    elif filter_lv == 2:
        data = database.getLvl2Data()
        groupVariable = 'administrative_area_level_2'
        filterCountry = locations[0].split(' - ')[0]
        locations = [loc.split(' - ')[1] for loc in locations]
    else:
        return

    allowedVariables = columns.getColumnGroups('variaveis')
    if filter_lv == 1:
        filtered_variables = [groupVariable] + [var for var in allowedVariables if var in keys]
    elif filter_lv == 2:
        filtered_variables = [groupVariable] + ['administrative_area_level_1'] + [var for var in allowedVariables if var in keys]

    df_group = data.copy()[filtered_variables]

    # Renomear a coluna de nível hierárquico
    df_group = df_group.rename(columns={groupVariable: 'location'})

    if filter_lv == 2:
        df_group = df_group[df_group['administrative_area_level_1'] == filterCountry]

    # Retirar a coluna de nível hierárquico se ela existir
    if 'administrative_area_level_1' in df_group.columns:
        df_group = df_group.drop(columns=['administrative_area_level_1'])

    grouped = df_group.groupby('location').sum().reset_index()

    for column in keys:  # ajuste os nomes das colunas conforme necessário
        if column in grouped.columns:
            grouped[f'{column}_rank'] = grouped[column].rank(method='max', ascending=False)

    # Filtrar as linhas baseadas nas localizações fornecidas após o rankeamento
    grouped_filtered = grouped[grouped['location'].isin(locations)]

    st.markdown(f'''
        ## Insights
    ''')

    for i in range(len(grouped_filtered)):
        dado = grouped_filtered.iloc[i]

        # cria uma string com o nome da localização e o rank
        text = f'A região administrativa :green[{dado.location}] é a que ocupa as seguintes posições para cada categoria:'

        # pega as colujnas que terminam em _rank
        rank_columns = [col for col in grouped_filtered.columns if col.endswith('_rank')]

        text_rank = []
        # impime para cada coluna rank o nome da variavel e orank em markdlwm
        for col in rank_columns:
            text_rank.append(f" **{int(dado[col])}º** para *{columns.getVariableTranslation(col.replace('_rank', ''))}*")

        st.markdown(text+','.join(text_rank))
