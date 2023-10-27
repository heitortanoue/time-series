from pandas import read_csv
import pandas as pd
from typing import List
import numpy as np
import streamlit as st
from functions.dbFunctions import getLvl1Data

filter_df = read_csv("./filters.csv")

def date_filter(df):
    df = getLvl1Data()
    df['date'] = pd.to_datetime(df['date'])
    d = st.sidebar.date_input(
    "Selecione o intervalo de tempo",
    [df['date'].min(), df['date'].max()],
    format="YYYY-MM-DD",
)
    return d


def lvl_1_filter() -> List[str]:
    filters = filter_df["administrative_area_level_1"].dropna().unique()
    filters = np.sort(filters)
    return filters

def lvl_2_filter(lst:List[str]) -> List[str]:
    countries = [item.split("-")[0].strip() for item in lst]
    lvl_2 = filter_df.query('administrative_area_level_1 in @countries').dropna()
    filter = (lvl_2['administrative_area_level_1'] + " - " + lvl_2['administrative_area_level_2']).drop_duplicates().sort_values() 
    return filter

def lvl_3_filter(lst) -> List[str]:
    countries = [item.split("-")[0].strip() for item in lst] 
    states = [item.split("-")[1].strip() for item in lst] 
    lvl_3 = filter_df.query('administrative_area_level_2 in @states').dropna()
    filter = (lvl_3['administrative_area_level_2'] + " - " + lvl_3['administrative_area_level_3']).sort_values()
    return filter 

def query_params(filter1=[], filter2=None, filter3=None):
    
    def extract_value(item):
        parts = item.split(" - ")
        return parts[1] if len(parts) > 1 else item

    # Process each list and extract values
    query_params1 = [extract_value(item) for item in filter1]
    
    if filter2 is None and filter3 is None:
        return query_params1 
    
    elif filter3 is None:
        query_params2 = [extract_value(item) for item in filter2]
        return query_params1, query_params2

    else:
        query_params2 = [extract_value(item) for item in filter2] 
        query_params3 = [extract_value(item) for item in filter3]
        return query_params1, query_params2, query_params3