import streamlit as st
import pandas as pd

import functions.backend.sessionState as sessionState
import functions.dbFunctions as database
import functions.filterFunctions as filters
from functions.backend.downloadData import download_data


def download_data_button():
    button = st.sidebar.empty()

    buttonPressed = button.button("Faça o download dos arquivos")
    if not buttonPressed:
        return

    with st.sidebar:
        with st.spinner("Fazendo o download do banco de dados..."):
            button.empty()
            download_data()

    st.sidebar.success("Os dados foram baixados")
    get_sidebar()

def date_filter(df):
    df = database.getLvl1Data()

    df['date'] = pd.to_datetime(df['date'])
    d = st.sidebar.date_input(
        "Selecione o intervalo de tempo",
        [df['date'].min(), df['date'].max()],
        format="DD.MM.YYYY"
    )
    return d

def create_filters():
    date_range = date_filter(database.getLvl1Data())

    filter_lvl1 = st.sidebar.multiselect(
        "Selecione os Países",
        options=filters.lvl_1_filter()
    )

    if not filter_lvl1:
        return st.empty()

    filter_lvl2 = st.sidebar.multiselect(
        "Selecione os Estados",
        options=filters.lvl_2_filter(filter_lvl1)
    )

    query_params1 = filters.query_params(filter1=filter_lvl1)

    df = database.getLvl1Data()
    df = df[df['administrative_area_level_1'].isin(filter_lvl1)]
    df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

    if not filter_lvl2:
        sessionState.set_state('filter_lv', 1)
        return df

    filter_lvl3 = st.sidebar.multiselect(
        "Selecione as Cidades",
        options=filters.lvl_3_filter(filter_lvl2)
    )

    query_params1, query_params2 = filters.query_params(filter1=filter_lvl1, filter2=filter_lvl2)

    df = database.getLvl2Data()
    df = df[df['administrative_area_level_2'].isin(query_params2)]
    df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

    if not filter_lvl3:
        sessionState.set_state('filter_lv', 2)
        return df

    query_params1, query_params2, query_params3 = filters.query_params(filter1=filter_lvl1, filter2=filter_lvl2, filter3=filter_lvl3)

    sessionState.set_state('filter_lv', 3)
    df = database.getFilteredData(query_params1, query_params2, query_params3)
    return df

def get_sidebar():
    if sessionState.get_state('downloaded_data'):
        df = create_filters()
        return df

    download_data_button()
    return st.empty()