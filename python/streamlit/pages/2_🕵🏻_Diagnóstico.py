import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *
import altair as alt
from functions.dbFunctions import *
from functions.filterFunctions import *
import pandas as pd

#PAGE STARTS HERE
st.markdown("# Diagnósticos dos dados" ) 
st.markdown("""Texto e mais texto\n
            Essa página deve conter os gráficos e medidas de diagnóstico das séries temporais
            Filtradas em quaisquer um dos níveis e por data.
            O filtro de data ainda não foi implementado""")  

#DATAFRAME PLACEHOLDER 
with st.expander("📈 Tabela com os dados"):
    dataframe_placeholder = st.empty()

#FILTROS 
st.sidebar.header("Selecione os filtros")

# Date filter
date_range = date_filter(getLvl1Data())

filter_lvl1 = st.sidebar.multiselect(
    "Selecione os Países",
    options=lvl_1_filter()
)

if filter_lvl1:

    filter_lvl2 = st.sidebar.multiselect(
        "Selecione os Estados",
        options=lvl_2_filter(filter_lvl1)
    )

    query_params1 = query_params(filter1=filter_lvl1) 

    df = getLvl1Data()
    df = df[df['administrative_area_level_1'].isin(filter_lvl1)]

    #Adiciona dataframe ao placeholder 
    dataframe_placeholder.dataframe(df)

    if filter_lvl2:
                
        filter_lvl3 = st.sidebar.multiselect(
            "Selecione as Cidades",
            options=lvl_3_filter(filter_lvl2)
        ) 

        query_params1, query_params2= query_params(filter1=filter_lvl1, filter2=filter_lvl2) 

        df = getLvl2Data() 
        df = df[df['administrative_area_level_2'].isin(query_params2)]

        #Adiciona dataframe ao placeholder 
        dataframe_placeholder.dataframe(df)

        if filter_lvl3:

            query_params1, query_params2, query_params3 = query_params(filter1=filter_lvl1, filter2=filter_lvl2, filter3=filter_lvl3) 

            df = getFilteredData(query_params1, query_params2, query_params3)

            #Adiciona dataframe ao placeholder 
            dataframe_placeholder.dataframe(df)

