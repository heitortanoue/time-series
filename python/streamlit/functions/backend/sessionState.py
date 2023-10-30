import streamlit as st

def using_state(variables):
    state = st.session_state
    result = {}

    for var_name in variables:
        if var_name not in state:
            state[var_name] = None
        result[var_name] = state[var_name]
    return result

def get_state(var_name):
    state = st.session_state
    return state[var_name]

def set_state(var_name, var_value):
    st.session_state[var_name] = var_value