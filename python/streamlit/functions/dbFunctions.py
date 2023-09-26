#Connect to the SQLite Db 
import sqlite3
from typing import Union, Optional, Any, List
from pandas import DataFrame
from pathlib import Path
import streamlit as st

#Variável de estado 
if 'download_data_button' not in st.session_state:
    st.session_state['download_data_button'] = False 

if 'downloaded_data' not in st.session_state:
    st.session_state['downloaded_data'] = False 

if 'downloaded_lvl1_data' not in st.session_state:
    st.session_state['downloaded_lvl1_data'] = False 

if 'downloaded_lvl2_data' not in st.session_state:
    st.session_state['downloaded_lvl2_data'] = False

class DbConnSQLite:

    def __init__(self) -> None:
        
        #Abrindo conexao 
        self.conn = sqlite3.connect(database="./data/latest.db") 
        
    def execute_sql(self, query:str, return_df: bool = False, verbose: bool = False, return_dict: bool = False, **kwargs) -> Union[DataFrame, List[Any]]:

        #Abrindo cursor 
        cur = self.conn.cursor()
        try:
            #Executando Query 
            cur.execute(query, kwargs) 
            #Printando query executada 
            if verbose:
                print(f"\nQuery Executada:\n\n{query}\n")
            #Retornando um Df 
            if return_df:
                column_names = [col[0] for col in cur.description] 
                query_data = cur.fetchall() 
                # Parse as df 
                query_df = DataFrame.from_records(query_data, columns=column_names) 
                res = query_df 

            return res
        finally:
            #Fechando cursor 
            cur.close() 

    def commit(self):
        #Fechando conexao 
        self.conn.commit() 
        self.conn.close() 

@st.cache_data
def getLvl1Data():
    
    conn = DbConnSQLite()

    query = f"""
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population,
                l.iso_alpha_3,
                l.iso_alpha_2,
                l.iso_numeric,
                l.iso_currency,
                l.key_local,
                l.key_google_mobility,
                l.key_apple_mobility,
                l.key_jhu_csse,
                l.key_nuts,
                l.key_gadm
            FROM timeseries t 
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level = 1;
            """ 
    
    df = conn.execute_sql(query=query, return_df=True)  

    st.session_state['downloaded_lvl1_data'] = True

    return df

@st.cache_data
def getLvl2Data():
    
    conn = DbConnSQLite()

    query = f"""
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population,
                l.iso_alpha_3,
                l.iso_alpha_2,
                l.iso_numeric,
                l.iso_currency,
                l.key_local,
                l.key_google_mobility,
                l.key_apple_mobility,
                l.key_jhu_csse,
                l.key_nuts,
                l.key_gadm
            FROM timeseries t 
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level = 2;
            """ 
    
    df = conn.execute_sql(query=query, return_df=True)  

    st.session_state['downloaded_lvl2_data'] = True

    return df

@st.cache_data
def getLvl3Data():
    
    conn = DbConnSQLite()

    query = f"""
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population,
                l.iso_alpha_3,
                l.iso_alpha_2,
                l.iso_numeric,
                l.iso_currency,
                l.key_local,
                l.key_google_mobility,
                l.key_apple_mobility,
                l.key_jhu_csse,
                l.key_nuts,
                l.key_gadm
            FROM timeseries t 
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level = 3;
            """ 
    
    df = conn.execute_sql(query=query, return_df=True)  

    st.session_state['downloaded_lvl3_data'] = True

    return df