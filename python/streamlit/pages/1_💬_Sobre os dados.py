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

#Acessando a coluna 1_1 
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
#placeholder_3 = st.empty()
df_choose = DataFrame()

if st.session_state['downloaded_data']:
    filter_lvl1 = st.sidebar.multiselect(
        "Selecione os países",
        options=lvl_1_filter()
    )

    filter_lvl2 = st.sidebar.multiselect(
        "Selecione os Estados",
        options=lvl_2_filter(filter_lvl1)
    )
    if placeholder_1.button("Dados Nacionais - Nível 01"):
        df_lvl1 = getLvl1Data()
        placeholder_1.empty()
        st.markdown("### Dados a Nivel Nacional") 
        st.write(df_lvl1)
        st.session_state['choose_df'] = '1'
    
    if placeholder_2.button("Dados Nacionais - Nível 02"):
        df_lvl2 = getLvl2Data()
        placeholder_2.empty()
        st.markdown("### Dados a Nivel Sub-Nacional") 
        st.write(df_lvl2) 
        df_choose = df_lvl2
        st.session_state['choose_df'] = '2'

    if st.session_state['choose_df'] in ('1','2') and not st.session_state['chart_mode'] and not st.session_state['plot_mode']:
    # if placeholder_3.button("Dados Nacionais - Nível 01"):
    #     df_lvl3 = getLvl3Data()
    #     placeholder_3.empty()
    #     st.markdown("### Dados a Nivel Regional") 
    #     st.write(df_lvl3)
        
        if st.button("Mostrar grafico de variavel no tempo"):
            st.session_state['chart_mode'] = True
    elif st.session_state['choose_df'] in ('1','2') and not st.session_state['plot_mode']:
        df_choose = getLvl1Data()
        columns_filter = []
        dtypes = df_choose.dtypes.apply(lambda x: x.name).to_dict()
        for column in dtypes:
            if dtypes[column] != 'object':
                columns_filter.append(column)
        dropdown = st.selectbox("Qual variavel você deseja plotar no tempo?",
                                columns_filter)
        st.session_state['column_plot'] = dropdown if dropdown is not None else st.session_state['column_plot']
        if st.button("Gerar gráfico"):
            if filter_lvl1 == []:
                st.markdown("Selecione um país")
            else:
                st.session_state['plot_mode'] = True
            st.write(df_choose)
    elif st.session_state['choose_df'] in ('1','2'):
            if st.session_state['choose_df'] == '1':
                
                #filter_lvl1
                columns_filter = []
                df_choose =  getLvl1Data().query("administrative_area_level_1 == '" + filter_lvl1[0] + "'")
                dtypes = df_choose.dtypes.apply(lambda x: x.name).to_dict()
                for column in dtypes:
                    if dtypes[column] != 'object':
                        columns_filter.append(column)
                dropdown = st.selectbox("Qual variavel você deseja plotar no tempo?",
                                columns_filter)
                st.session_state['column_plot'] = dropdown if dropdown is not None else st.session_state['column_plot']
                
                #df_choose['date'] = pd.to_datetime(df_choose['date'])
                #df_choose = df_choose[["confirmed", "date"]]
                
                #st.dataframe(df_choose)
                column = st.session_state['column_plot']
                bar_chart_top10 = alt.Chart(df_choose).mark_line(point=True).encode(
                    y=alt.Y(column+':Q'),
                    x = alt.X('date:T')
                    #color=alt.Color(
                    #    "Country",
                    #    scale=alt.Scale(
                    #    domain = top_10_countries.Country.tolist(),
                    #    range = ['red']*3+['steelblue']*7),
                    #    legend=None
                    #)
                )
                st.altair_chart(bar_chart_top10, use_container_width=True)
                    #print(df_choose.columns)
                    #df_choose = df_choose[['administrative_area_level_1', 'date', st.session_state['column_plot']]]
                    #random.seed(len(df_choose))
                    #fig, axes = plt.subplots(nrows=len(df_choose['administrative_area_level_1'].unique()), ncols=1, figsize=(8, 6))

                    # Itere pelos países e plote as linhas em subtramas separadas
                    #for i, pais in enumerate(df_choose['administrative_area_level_1'].unique()):
                    #    subset = df_choose[df_choose['administrative_area_level_1'] == pais]
                    #    axes[i].plot(subset['date'], subset[st.session_state['column_plot']], label=pais, color=(random.random(),random.random(),random.random()))
                    #    axes[i].set_xlabel('Dia')
                    #    axes[i].set_ylabel('Valor')
                    #    axes[i].set_title(f'Valor por Dia - {pais}')
                    #    axes[i].legend()
                    #st.pyplot(fig)
                #else:
                    


