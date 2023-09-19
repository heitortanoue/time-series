import streamlit as st 
from data import download_SQLiteDb 
from functions.dbFunctions import *

# Texto superior na página
st.markdown("# Analizes" ) 
st.markdown("Aqui ficarão os modelos que possibilitarão analises pelo Usuario") 
st.markdown("Os modelos disponiveis são os listados pelos botões abaixo") 

#Esses modelos estão somente para exemplo
modelo_id = 0
modelo_names = ["ARIMA", "ARMA"]

buttons = []

# Adiciona um botão para cada modelo
for i in range(2):
    buttons.append(st.empty().button(modelo_names[i]))

#Adiciona os trigers
if buttons[0]:
    print(modelo_names[0])

if buttons[1]:
    print(modelo_names[1])    
