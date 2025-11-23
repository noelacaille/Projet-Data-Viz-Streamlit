"""
Data loading utilities for the commute dashboard.
Handles data ingestion, caching, and basic validation.
"""

import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data(show_spinner="Chargement des données de mobilité...")
def load_commute_data() -> pd.DataFrame:
    """
    Load the main commute flux dataset.
    
    Returns:
        DataFrame with columns: date_mesure, geocode_commune, libelle_commune, 
                                 mode_transport, valeur
    """
    data_path = Path(__file__).parent.parent / "data" / "flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv"
    
    df = pd.read_csv(data_path)
    
    # Convert date
    df['date_mesure'] = pd.to_datetime(df['date_mesure'])
    
    # Standardize geocode to string with padding
    df['geocode_commune'] = df['geocode_commune'].astype(str)
    
    return df


@st.cache_data(show_spinner="Chargement des données géographiques...")
def load_geographic_data() -> pd.DataFrame:
    """
    Load geographic reference data (communes, departments, regions).
    
    Returns:
        DataFrame with geographic metadata including latitude/longitude
    """
    data_path = Path(__file__).parent.parent / "data" / "20230823-communes-departement-region.csv"
    
    df = pd.read_csv(data_path)
    
    # Keep only relevant columns and deduplicate
    cols_to_keep = [
        'code_commune_INSEE', 'nom_commune', 'latitude', 'longitude',
        'code_departement', 'nom_departement', 'code_region', 'nom_region'
    ]
    
    df = df[cols_to_keep].drop_duplicates(subset=['code_commune_INSEE'])
    
    return df


def get_data_license() -> str:
    """Return the data license and attribution text."""
    return """
    **Source des données :** 
    - Flux domicile-travail : Insee, Recensement de la population 2022
    - Référentiel géographique : Insee & Data.gouv.fr
    
    **Licence :** Licence Ouverte
    
    Les données sont issues de l'enquête annuelle de recensement et représentent 
    les déplacements domicile-travail des actifs de 15 ans ou plus.
    """


def get_transport_mode_mapping() -> dict:
    """
    Return a mapping of transport modes with display names and colors.
    """
    return {
        'Voiture': {
            'display': '🚗 Voiture',
            'color': '#e74c3c',  # Red
            'emoji': '🚗'
        },
        'Transports en commun': {
            'display': '🚌 Transports en commun',
            'color': '#3498db',  # Blue
            'emoji': '🚌'
        },
        'Vélo': {
            'display': '🚴 Vélo',
            'color': '#2ecc71',  # Green
            'emoji': '🚴'
        },
        'Marche': {
            'display': '🚶 Marche',
            'color': '#f39c12',  # Orange
            'emoji': '🚶'
        },
        'Deux-roues motorisé': {
            'display': '🏍️ Deux-roues motorisé',
            'color': '#9b59b6',  # Purple
            'emoji': '🏍️'
        },
        'Pas de transport': {
            'display': '🏠 Pas de transport',
            'color': '#95a5a6',  # Gray
            'emoji': '🏠'
        }
    }


def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Validate data quality and return a summary of issues.
    
    Args:
        df: The commute dataframe
        
    Returns:
        Dictionary with validation metrics
    """
    validation = {
        'total_rows': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'negative_values': (df['valeur'] < 0).sum() if 'valeur' in df.columns else 0,
        'unique_communes': df['geocode_commune'].nunique() if 'geocode_commune' in df.columns else 0,
        'date_range': {
            'min': df['date_mesure'].min() if 'date_mesure' in df.columns else None,
            'max': df['date_mesure'].max() if 'date_mesure' in df.columns else None
        }
    }
    
    return validation
