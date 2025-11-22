import pandas as pd
import numpy as np

def clean_and_prep_data(df):
    """
    Cleans the raw dataframe and prepares it for analysis.
    Transforms from long to wide format.
    """
    if df.empty:
        return pd.DataFrame()

    # Ensure geocode_commune is string to extract dept
    df['geocode_commune'] = df['geocode_commune'].astype(str).str.zfill(5)
    
    # Extract Department (handle Corsica 2A/2B and DOM)
    def get_dept(code):
        if code.startswith('97'):
            return code[:3]
        return code[:2]
    
    df['dept'] = df['geocode_commune'].apply(get_dept)
    
    # Pivot the table
    # Index: geocode_commune, libelle_commune, dept
    # Columns: mode_transport
    # Values: valeur
    df_pivot = df.pivot_table(
        index=['geocode_commune', 'libelle_commune', 'dept'],
        columns='mode_transport',
        values='valeur',
        aggfunc='sum'
    ).reset_index()
    
    # Fill NaNs with 0
    df_pivot = df_pivot.fillna(0)
    
    # Calculate Total Actifs
    # Identify mode columns (exclude index columns)
    mode_cols = [c for c in df_pivot.columns if c not in ['geocode_commune', 'libelle_commune', 'dept']]
    df_pivot['Total_Actifs'] = df_pivot[mode_cols].sum(axis=1)
    
    # Calculate Percentages
    for mode in mode_cols:
        df_pivot[f'pct_{mode}'] = (df_pivot[mode] / df_pivot['Total_Actifs']) * 100
        
    # Determine Dominant Mode
    # We only look at the raw values or percentages to find the max
    df_pivot['Mode_Dominant'] = df_pivot[mode_cols].idxmax(axis=1)
    
    return df_pivot

def filter_data(df, selected_depts, selected_communes=None):
    """
    Filters the dataframe based on selected departments and communes.
    """
    filtered_df = df.copy()
    
    if selected_depts:
        filtered_df = filtered_df[filtered_df['dept'].isin(selected_depts)]
        
    if selected_communes:
        filtered_df = filtered_df[filtered_df['libelle_commune'].isin(selected_communes)]
        
    return filtered_df
