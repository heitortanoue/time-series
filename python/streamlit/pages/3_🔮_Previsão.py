import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *
from functions.filterFunctions import *

# Texto superior na página
st.markdown("# Modelos e Previsões" ) 
st.markdown("""Texto e mais texto\n
            Essa página deve conter os modelos de previsão das séries temporais.
            **O usuário deve ter controle sobre os parâmetros do modelo escolhido**
            Filtradas em quaisquer um dos níveis e por data.
            O filtro de data ainda não foi implementado""")  
st.markdown("Os modelos disponiveis são os listados pelos botões abaixo") 

#FILTROS 
st.sidebar.header("Selecione os filtros")

filter_lvl1 = st.sidebar.multiselect(
    "Selecione os países",
    options=lvl_1_filter()
)

if filter_lvl1:

    filter_lvl2 = st.sidebar.multiselect(
        "Selecione os Estados",
        options=lvl_2_filter(filter_lvl1)
    )

    if filter_lvl2:
                
        filter_lvl3 = st.sidebar.multiselect(
            "Selecione as Cidades",
            options=lvl_3_filter(filter_lvl2)
        )

        st.write(filter_lvl1)
        st.write(filter_lvl2)
        st.write(filter_lvl3)

#Esses modelos estão somente para exemplo
modelo_id = 0
modelo_names = ["ARIMA", "SARIMA"]

buttons = []

# Adiciona um botão para cada modelo
for i in range(2):
    buttons.append(st.empty().button(modelo_names[i]))

#Adiciona os trigers
if buttons[0]:
    print(modelo_names[0])

if buttons[1]:
    print(modelo_names[1])    
