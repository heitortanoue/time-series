import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *
import altair as alt
from functions.dbFunctions import *
from functions.filterFunctions import *
import pandas as pd

#Variável de estado 
if 'download_data_button' not in st.session_state:
    st.session_state['download_data_button'] = False 
if 'choose_df' not in st.session_state:
    st.session_state['choose_df'] = 0 
if 'chart_mode' not in st.session_state:
    st.session_state['chart_mode'] = False

if 'downloaded_data' not in st.session_state:
    st.session_state['downloaded_data'] = False 

if 'downloaded_lvl1_data' not in st.session_state:
    st.session_state['downloaded_lvl1_data'] = False 

if 'downloaded_lvl2_data' not in st.session_state:
    st.session_state['downloaded_lvl2_data'] = False 

if 'plot_mode' not in st.session_state:
    st.session_state['plot_mode'] = False

if 'country_mode' not in st.session_state:
    st.session_state['country_mode'] = False

if 'column_plot' not in st.session_state:
    st.session_state['column_plot'] = False

#PAGE STARTS HERE
st.markdown("# Análises" ) 
st.markdown("""Texto e mais texto\n
            Essa página deve conter os gráficos exploratórios para as variávies epidemiológicas
            Filtradas em quaisquer um dos níveis e por data.
            O filtro de data ainda não foi implementado""") 

#DATAFRAME PLACEHOLDER 
with st.expander("📈 Tabela com os dados"):
    dataframe_placeholder = st.empty()

if st.session_state['download_data_button'] is False:
    placeholder_1 = st.empty()
    if placeholder_1.button("Faça o download dos arquivos"):
        with st.spinner("Fazendo o download do banco de dados..."):
            placeholder_1.empty()
            #DOWNLOAD DOS DADOS
            db = download_SQLiteDb()
            st.session_state['downloaded_data'] = True
            st.session_state['download_data_button'] = True
        
            if st.session_state['downloaded_data']:
                #CACHE DOS NÍVEIS 
                df_lvl1 = getLvl1Data()
                st.session_state['downloaded_lvl1_data'] = True

            if st.session_state['downloaded_lvl1_data']:
                df_lvl2 = getLvl2Data()

        st.success("Os dados foram baixados")

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
    #filtra as datas 
    df  = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

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
        df  = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

        #Adiciona dataframe ao placeholder 
        dataframe_placeholder.dataframe(df)

        if filter_lvl3:

            query_params1, query_params2, query_params3 = query_params(filter1=filter_lvl1, filter2=filter_lvl2, filter3=filter_lvl3) 

            df = getFilteredData(query_params1, query_params2, query_params3)
            df  = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

            #Adiciona dataframe ao placeholder 
            dataframe_placeholder.dataframe(df)

# # Filter data based on date range
# filtered_data = data[(data['date'] >= date_range[0]) & (data['date'] <= date_range[1])

# # Dropdown to select a column for plotting
# selected_column = st.selectbox("Select a column for plotting", data.columns[1:])

# # Create Altair plot
# st.write("Altair Plot:")
# alt_chart = alt.Chart(filtered_data).mark_line().encode(
#     x='date:T',
#     y=alt.Y(selected_column, type='quantitative', aggregate='sum'),
# ).properties(
#     width=300,
#     height=200
# )
# st.altair_chart(alt_chart)

# # You can repeat the above code for each of the four columns.
# # You may also create additional plots and columns as needed.

# # Example to create multiple columns:
# # with st.beta_container():
# #     # Add your Altair plot and filters here