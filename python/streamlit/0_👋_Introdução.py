import streamlit as st 


#WIDE LAYOUT
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="🧬") 

#SIDEBAR 
st.sidebar.image("../../www/img/logo.jpeg")
st.sidebar.title("SME-0808 - Dashboard COVID-19") 
st.sidebar.info(
    """

    **Infomações** 

    **Sobre**: Trabalho final da disciplina de Séries Temporais\n
    **Autores**: Grupo J\n
    **Data**: Dezembro de 2023

    """
) 

#SIDEBAR - FILTER 
 

#BODY
st.markdown("# Dashboard - COVID-19 🧬")

st.markdown("## 👋 Olá!")
st.markdown("#### Esse dashboard irá conter todas as informações do nosso trabalho") 
st.markdown("#### Ele ainda está incompleto :grimacing: ")
st.markdown("#### Mas você pode visualizar o trabalho nas páginas ao lado 👈") 