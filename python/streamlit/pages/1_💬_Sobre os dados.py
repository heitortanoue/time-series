import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *

#Variável de estado 
if 'download_data_button' not in st.session_state:
    st.session_state['download_data_button'] = False 

if 'downloaded_data' not in st.session_state:
    st.session_state['downloaded_data'] = False 

if 'downloaded_lvl1_data' not in st.session_state:
    st.session_state['downloaded_lvl1_data'] = False 

if 'downloaded_lvl2_data' not in st.session_state:
    st.session_state['downloaded_lvl2_data'] = False 


#CREATING TWO COLUMNS 
col_1_1, col_1_2 = st.columns([1,1]) 

#Acessando a coluna 1_1 
with col_1_1:
    st.markdown("# Informações Importantes sobre os dados" ) 
    st.markdown("Aqui escrevemos as coisas") 

     

    if st.session_state['download_data_button'] is False:
        placeholder_1 = st.empty()
        if placeholder_1.button("Faça o download dos arquivos"):
            
            with st.spinner("Fazendo o download do banco de dados..."):
                placeholder_1.empty()
                #DOWNLOAD DOS DADOS
                db = download_SQLiteDb()
            st.session_state['downloaded_data'] = True

            if st.session_state['downloaded_data'] is True:
                #CACHE DOS NÍVEIS 
                df_lvl1 = getLvl1Data()
    
            if st.session_state['downloaded_lvl1_data'] is True:
                df_lvl2 = getLvl2Data()

            ###
            # OS DADOS COMPLETOS DO NIVEL 3 DÁ ERRO DE MEMÓRIA!!!   
            # if st.session_state['downloaded_lvl2_data'] is True:
            #     df_lvl3 = getLvl3Data()

            st.success("Os dados foram baixados")
            
            st.session_state['download_data_button'] = True

    placeholder_1 = st.empty()
    placeholder_2 = st.empty()
    placeholder_3 = st.empty()

    if st.session_state['downloaded_data']:
        if placeholder_1.button("Dados Nacionais - Nível 01"):
            df_lvl1 = getLvl1Data()
            placeholder_1.empty()
            st.markdown("### Dados a Nivel Nacional") 
            st.write(df_lvl1)
        
        if placeholder_2.button("Dados Nacionais - Nível 02"):
            df_lvl2 = getLvl2Data()
            placeholder_2.empty()
            st.markdown("### Dados a Nivel Sub-Nacional") 
            st.write(df_lvl2) 

        # if placeholder_3.button("Dados Nacionais - Nível 01"):
        #     df_lvl3 = getLvl3Data()
        #     placeholder_3.empty()
        #     st.markdown("### Dados a Nivel Regional") 
        #     st.write(df_lvl3)