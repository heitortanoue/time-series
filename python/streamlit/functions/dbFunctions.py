#Connect to the SQLite Db
import sqlite3
from typing import Union, Optional, Any, List
from pandas import DataFrame
from pathlib import Path
import streamlit as st
import pandas as pd

class DbConnSQLite:

    def __init__(self) -> None:

        #Abrindo conexao
        self.conn = sqlite3.connect(database="./data/latest.db")

    def execute_sql(self, query:str, params: dict = None, return_df: bool = False, verbose: bool = False, return_dict: bool = False, **kwargs) -> Union[DataFrame, List[Any]]:

        #Abrindo cursor
        cur = self.conn.cursor()
        try:
            #Executando Query
            if params is not None:
                cur.execute(query, params)
            else:
                cur.execute(query)
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
                l.population
            FROM timeseries t
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level = 1;
            """

    df = conn.execute_sql(query=query, return_df=True)

    # Convert date column to datetime and get the date
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df['date'].apply(lambda x: pd.Timestamp(x).date())


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
                l.population
            FROM timeseries t
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level = 2;
            """

    df = conn.execute_sql(query=query, return_df=True)
    # Convert date column to datetime and get the date
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df['date'].apply(lambda x: pd.Timestamp(x).date())

    return df

@st.cache_data
def getFilteredData(query_params1=None, query_params2=None, query_params3=None):
    conn = DbConnSQLite()

    if query_params1 is not None and query_params2 is None and query_params3 is None:
        query_params1 = ','.join(query_params1)

        query = """
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population
            FROM timeseries t
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level_1 IN (?);
            """

        params = [query_params1]

    elif query_params1 is not None and query_params2 is not None and query_params3 is None:
        query_params1 = ','.join(query_params1)
        query_params2 = ','.join(query_params2)

        query = """
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population
            FROM timeseries t
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level_1 IN (?)
                AND l.administrative_area_level_2 IN (?);
            """

        params = [query_params1, query_params2]

    elif query_params1 is not None and query_params2 is not None and query_params3 is not None:
        query_params1 = ','.join(query_params1)
        query_params2 = ','.join(query_params2)
        query_params3 = ','.join(query_params3)

        query = """
            SELECT t.*,
                l.administrative_area_level,
                l.administrative_area_level_1,
                l.administrative_area_level_2,
                l.administrative_area_level_3,
                l.latitude,
                l.longitude,
                l.population
            FROM timeseries t
            LEFT JOIN location l on l.id = t.id
            WHERE l.administrative_area_level_1 IN (?)
                AND l.administrative_area_level_2 IN (?)
                AND l.administrative_area_level_3 IN (?);
            """

        params = [query_params1, query_params2, query_params3]

    else:
        # Handle the case when no valid filter parameters are provided
        return None

    df = conn.execute_sql(query, params=params, return_df=True)
    # Convert date column to datetime and get the date
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df['date'].apply(lambda x: pd.Timestamp(x).date())

    return df
