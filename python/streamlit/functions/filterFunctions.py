from pandas import read_csv
from typing import List
import numpy as np
import streamlit as st

filter_df = read_csv("../filters.csv")


def lvl_1_filter() -> List[str]:
    filters = filter_df["administrative_area_level_1"].unique()
    filters = np.sort(filters)
    return filters 

def lvl_2_filter(lst:List[str]) -> List[str]:
    condition = filter_df['administrative_area_level_1'].isin(lst)
    lvl_2_filter = filter_df[condition]['administrative_area_level_2']
    return lvl_2_filter


##TO-DO
# def lvl_3_filter(lst)