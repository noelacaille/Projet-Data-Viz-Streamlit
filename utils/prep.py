"""
Data preparation and feature engineering utilities.
Handles cleaning, aggregations, and metric calculations.
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data(show_spinner="Préparation des données...")
def prepare_complete_dataset(commute_df: pd.DataFrame, geo_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge commute data with geographic reference and compute key metrics.
    
    Args:
        commute_df: Raw commute flux data
        geo_df: Geographic reference data
        
    Returns:
        Enriched DataFrame with geographic info and computed metrics
    """
    # Merge datasets
    df = commute_df.merge(
        geo_df,
        left_on='geocode_commune',
        right_on='code_commune_INSEE',
        how='left'
    )
    
    # Calculate total actifs per commune
    commune_totals = df.groupby('geocode_commune')['valeur'].sum().reset_index()
    commune_totals.columns = ['geocode_commune', 'total_actifs']
    
    df = df.merge(commune_totals, on='geocode_commune', how='left')
    
    # Calculate percentage for each mode
    df['pourcentage'] = (df['valeur'] / df['total_actifs'] * 100).round(2)
    
    # Add population categories
    df['categorie_taille'] = pd.cut(
        df['total_actifs'],
        bins=[0, 100, 500, 2000, 10000, np.inf],
        labels=['Très petite (<100)', 'Petite (100-500)', 'Moyenne (500-2k)', 'Grande (2k-10k)', 'Très grande (>10k)']
    )
    
    return df


@st.cache_data
def compute_regional_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data by region and transport mode.
    
    Args:
        df: Complete dataset
        
    Returns:
        DataFrame aggregated by region
    """
    regional = df.groupby(['nom_region', 'mode_transport']).agg({
        'valeur': 'sum',
        'geocode_commune': 'nunique'
    }).reset_index()
    
    regional.columns = ['nom_region', 'mode_transport', 'total_actifs', 'nb_communes']
    
    # Calculate regional percentages
    regional_totals = regional.groupby('nom_region')['total_actifs'].sum().reset_index()
    regional_totals.columns = ['nom_region', 'total_regional']
    
    regional = regional.merge(regional_totals, on='nom_region')
    regional['pourcentage'] = (regional['total_actifs'] / regional['total_regional'] * 100).round(2)
    
    return regional


@st.cache_data
def compute_departmental_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data by department and transport mode.
    
    Args:
        df: Complete dataset
        
    Returns:
        DataFrame aggregated by department
    """
    departmental = df.groupby(['code_departement', 'nom_departement', 'mode_transport']).agg({
        'valeur': 'sum',
        'geocode_commune': 'nunique'
    }).reset_index()
    
    departmental.columns = ['code_departement', 'nom_departement', 'mode_transport', 'total_actifs', 'nb_communes']
    
    # Calculate departmental percentages
    dept_totals = departmental.groupby('code_departement')['total_actifs'].sum().reset_index()
    dept_totals.columns = ['code_departement', 'total_dept']
    
    departmental = departmental.merge(dept_totals, on='code_departement')
    departmental['pourcentage'] = (departmental['total_actifs'] / departmental['total_dept'] * 100).round(2)
    
    return departmental


@st.cache_data
def compute_car_dependency_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate car dependency index for each commune.
    
    The index represents the percentage of workers using cars for commuting.
    
    Args:
        df: Complete dataset
        
    Returns:
        DataFrame with geocode, commune name, car dependency index, and coordinates
    """
    # Filter for car mode
    car_df = df[df['mode_transport'] == 'Voiture'].copy()
    
    # Get unique communes with their info
    dependency = car_df.groupby('geocode_commune').agg({
        'nom_commune': 'first',
        'pourcentage': 'first',
        'total_actifs': 'first',
        'valeur': 'first',
        'latitude': 'first',
        'longitude': 'first',
        'nom_departement': 'first',
        'nom_region': 'first'
    }).reset_index()
    
    dependency.columns = [
        'geocode_commune', 'nom_commune', 'indice_dependance_voiture',
        'total_actifs', 'nb_voitures', 'latitude', 'longitude',
        'nom_departement', 'nom_region'
    ]
    
    # Remove communes with missing coordinates
    dependency = dependency.dropna(subset=['latitude', 'longitude'])
    
    return dependency


@st.cache_data
def get_top_communes_by_mode(df: pd.DataFrame, mode: str, n: int = 20) -> pd.DataFrame:
    """
    Get top N communes for a specific transport mode.
    
    Args:
        df: Complete dataset
        mode: Transport mode to filter
        n: Number of top communes to return
        
    Returns:
        DataFrame with top communes sorted by percentage
    """
    mode_df = df[df['mode_transport'] == mode].copy()
    
    # Filter out very small communes (< 50 actifs) to avoid statistical noise
    mode_df = mode_df[mode_df['total_actifs'] >= 50]
    
    # Sort by percentage and get top N
    top = mode_df.nlargest(n, 'pourcentage')[
        ['nom_commune', 'nom_departement', 'pourcentage', 'valeur', 'total_actifs']
    ]
    
    return top.reset_index(drop=True)


@st.cache_data
def compute_modal_shift_potential(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute potential for modal shift (from car to sustainable modes).
    
    Identifies communes with high car dependency but sufficient size for alternatives.
    
    Args:
        df: Complete dataset
        
    Returns:
        DataFrame with modal shift potential metrics
    """
    # Get car dependency by commune
    car_dep = df[df['mode_transport'] == 'Voiture'].groupby('geocode_commune').agg({
        'nom_commune': 'first',
        'pourcentage': 'first',
        'total_actifs': 'first',
        'nom_departement': 'first',
        'nom_region': 'first',
        'latitude': 'first',
        'longitude': 'first'
    }).reset_index()
    
    # Filter for communes with > 1000 actifs and > 70% car usage
    potential = car_dep[
        (car_dep['total_actifs'] > 1000) & 
        (car_dep['pourcentage'] > 70)
    ].copy()
    
    # Calculate potential reduction (assuming 20% could shift to alternatives)
    potential['actifs_transferables'] = (potential['total_actifs'] * potential['pourcentage'] / 100 * 0.2).round(0)
    
    potential = potential.sort_values('actifs_transferables', ascending=False)
    
    return potential


@st.cache_data
def compute_sustainable_mobility_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a sustainable mobility score for each commune.
    
    Score is based on: bike + walk + public transit + no transport (telework)
    
    Args:
        df: Complete dataset
        
    Returns:
        DataFrame with sustainability scores
    """
    sustainable_modes = ['Vélo', 'Marche', 'Transports en commun', 'Pas de transport']
    
    # Filter for sustainable modes
    sustainable = df[df['mode_transport'].isin(sustainable_modes)].copy()
    
    # Sum percentages for each commune
    scores = sustainable.groupby('geocode_commune').agg({
        'nom_commune': 'first',
        'pourcentage': 'sum',
        'total_actifs': 'first',
        'nom_departement': 'first',
        'nom_region': 'first',
        'latitude': 'first',
        'longitude': 'first'
    }).reset_index()
    
    scores.columns = [
        'geocode_commune', 'nom_commune', 'score_mobilite_durable',
        'total_actifs', 'nom_departement', 'nom_region', 'latitude', 'longitude'
    ]
    
    scores = scores.dropna(subset=['latitude', 'longitude'])
    scores = scores.sort_values('score_mobilite_durable', ascending=False)
    
    return scores


def filter_data(df: pd.DataFrame, 
                regions: list = None, 
                departments: list = None,
                size_categories: list = None,
                min_actifs: int = 0) -> pd.DataFrame:
    """
    Apply filters to the dataset based on user selections.
    
    Args:
        df: Complete dataset
        regions: List of regions to include
        departments: List of departments to include
        size_categories: List of commune size categories
        min_actifs: Minimum number of actifs
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if regions:
        filtered = filtered[filtered['nom_region'].isin(regions)]
    
    if departments:
        filtered = filtered[filtered['nom_departement'].isin(departments)]
    
    if size_categories:
        filtered = filtered[filtered['categorie_taille'].isin(size_categories)]
    
    if min_actifs > 0:
        filtered = filtered[filtered['total_actifs'] >= min_actifs]
    
    return filtered
