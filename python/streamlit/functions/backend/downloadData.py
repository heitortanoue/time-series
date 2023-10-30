import streamlit as st

import functions.dbFunctions as database
import functions.backend.sessionState as sessionState
from data import download_SQLiteDb

def download_data():
    sessionState.using_state(['downloaded_data'])

    with st.sidebar:
        with st.spinner("Baixando os dados..."):
            download_SQLiteDb()
        with st.spinner("Fazendo cache dos dados..."):
            database.getLvl1Data()
            database.getLvl2Data()

    sessionState.set_state('downloaded_data', True)