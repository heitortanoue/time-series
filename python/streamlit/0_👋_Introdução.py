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



# Definir o subtítulo da introdução
st.header("Introdução")

# Escrever o texto da introdução em Markdown
st.markdown("""
A COVID-19 é uma doença causada pelo novo coronavírus SARS-CoV-2, que se espalhou pelo mundo desde o final de 2019, provocando uma pandemia global. Os dados sobre a COVID-19 são fundamentais para monitorar a situação epidemiológica, avaliar o impacto das medidas de prevenção e controle, e orientar as políticas públicas de saúde.

Neste trabalho, utilizamos uma API chamada COVID-19 Data Hub, que fornece dados atualizados e padronizados sobre a COVID-19 de diversas fontes oficiais, como a Organização Mundial da Saúde, o Centro Europeu de Prevenção e Controle de Doenças, e os governos nacionais. A API permite acessar os dados em diferentes formatos, como CSV, JSON, e R. Para obter os dados fizemos o download dos arquivos diretamente do Endpoint e lemos como um objeto Pandas.

O objetivo deste trabalho é realizar uma análise temporal dos dados sobre COVID-19 em todos os nível disponiveis (nível de pais, nível de estado e nível de cidade), utilizando a biblioteca Streamlit para criar um aplicativo web interativo que permite visualizar e explorar os dados. O trabalho é dividido em quatro páginas: Introdução, Análises, Diagnósticos e Previsão. Em cada página, apresentamos os resultados das nossas análises, bem como os códigos e as fontes utilizadas.
""")