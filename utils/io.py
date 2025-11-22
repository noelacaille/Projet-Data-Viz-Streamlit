import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    """
    Loads the commune-level dataset.
    """
    # Construct absolute path to ensure it works regardless of where streamlit is run
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv')
    
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

    df = pd.read_csv(file_path, sep=',') # Assuming comma separator based on previous read_file
    return df
