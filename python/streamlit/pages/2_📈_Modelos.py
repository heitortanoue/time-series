import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *
from functions.filterFunctions import *

# Texto superior na página
st.markdown("# Análises" ) 
st.markdown("Aqui ficarão os modelos que possibilitarão analises pelo Usuario") 
st.markdown("Os modelos disponiveis são os listados pelos botões abaixo") 

#Filtros 
st.sidebar.header("Selecione os filtros")

filter_lvl1 = st.sidebar.multiselect(
    "Selecione os países",
    options=lvl_1_filter()
)

filter_lvl2 = st.sidebar.multiselect(
    "Selecione os Estados",
    options=lvl_2_filter(filter_lvl1)
)

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
