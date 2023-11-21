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

def create_filters(diagnostico:bool=False):
    sessionState.using_state(['locations'])
    date_range = date_filter(database.getLvl1Data())

    if diagnostico:
        
        sessionState.using_state(['lag'])
        sessionState.using_state(['window'])
        sessionState.using_state(['decomposition_model'])

        window_filter = st.sidebar.multiselect(
            "Selecione a janela de tempo",
            options=['Diária','Semanal', 'Mensal']
        )

        if window_filter[0] == 'Diária':
            sessionState.set_state('window', 'D')
        elif window_filter[0] == 'Semanal':
            sessionState.set_state('window', 'W') 
        elif window_filter[0] == 'Mensal':
            sessionState.set_state('window','M')

    filter_lvl1 = st.sidebar.multiselect(
        "Selecione os Países",
        options=filters.lvl_1_filter()
    )

    if not filter_lvl1:
        sessionState.set_state('locations', None)
        sessionState.set_state('filter_lv', None)
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
        sessionState.set_state('locations', filter_lvl1)
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
        sessionState.set_state('locations', filter_lvl2)
        sessionState.set_state('filter_lv', 2)
        return df

    query_params1, query_params2, query_params3 = filters.query_params(filter1=filter_lvl1, filter2=filter_lvl2, filter3=filter_lvl3)

    sessionState.set_state('filter_lv', 3)
    sessionState.set_state('locations', filter_lvl3)
    df = database.getFilteredData(query_params1, query_params2, query_params3)
    return df

def get_sidebar(diagnostico:bool=False):
    if sessionState.get_state('downloaded_data'):
        df = create_filters(diagnostico)
        return df

    download_data_button()
    return st.empty()

def get_locations():
    return sessionState.get_state('locations') 

def get_window_time():
    return sessionState.get_state('window')

def get_differentiation_lag():
    return sessionState.get_state('lag') 

def get_decomposition_model():
    return sessionState.get_state('decomposition_model')