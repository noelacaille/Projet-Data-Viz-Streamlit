"""
Main Streamlit application for the Mobility Dashboard.

La fracture de la mobilité : La France est-elle vraiment prête à lâcher la voiture ?

This dashboard explores commuting patterns in France using 2022 census data,
revealing the deep territorial divide in mobility options.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import utility functions
from utils.io import load_commute_data, load_geographic_data
from utils.prep import prepare_complete_dataset, filter_data

# Import section renderers
from sections import intro, overview, deep_dives, comparisons, conclusions


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="La fracture de la mobilité | Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Dashboard de visualisation des flux domicile-travail en France. Données Insee 2022."
    }
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

def load_custom_css():
    """Load custom CSS for beautiful UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700;
        color: #1e3a8a;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        color: #1e40af;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0a1a46;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3b82f6 0%, #1e40af 100%);
        padding-top: 0.5rem;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
        margin-bottom: 0.3rem;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }
    
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: white;
    }
    
    .st-emotion-cache-ja5xo9{
        padding-bottom: 0 !important;
    }
    
    [data-testid="stSidebar"] h4 {
        color: white !important;
        font-size: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    
    /* Compact multiselect in sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        margin-bottom: 0.3rem;
    }
    
    /* Compact slider in sidebar */
    [data-testid="stSidebar"] .stSlider {
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        font-weight: 600;
        border-radius: 8px;
        background-color: transparent;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Separator */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Selectbox */
    .stSelectbox > label {
        font-weight: 600;
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data(show_spinner="Chargement des données...")
def load_all_data():
    """
    Load and prepare all data with caching.
    
    Returns:
        tuple: (raw_commute_df, raw_geo_df, complete_df)
    """
    # Load raw data
    commute_df = load_commute_data()
    geo_df = load_geographic_data()
    
    # Prepare complete dataset
    complete_df = prepare_complete_dataset(commute_df, geo_df)
    
    return commute_df, geo_df, complete_df


# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

def render_sidebar(df: pd.DataFrame):
    """
    Render the sidebar with filters and controls.
    
    Args:
        df: Complete dataset
        
    Returns:
        dict: Filter selections
    """
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 0.3rem 0;'>
            <h1 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>Analyse de la mobilité en France</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Region filter
        st.markdown("#### Géographie")
        
        all_regions = sorted(df['nom_region'].dropna().unique())
        selected_regions = st.multiselect(
            "Région(s)",
            options=all_regions,
            default=None,
            help="Sélectionnez une ou plusieurs régions"
        )
        
        # Department filter (conditional on region)
        if selected_regions:
            available_depts = sorted(
                df[df['nom_region'].isin(selected_regions)]['nom_departement'].dropna().unique()
            )
        else:
            available_depts = sorted(df['nom_departement'].dropna().unique())
        
        selected_departments = st.multiselect(
            "Département(s)",
            options=available_depts,
            default=None,
            help="Affinez par département"
        )
        
        # Size filters
        st.markdown("#### Taille")
        
        size_categories = st.multiselect(
            "Catégories de taille",
            options=['Très petite (<100)', 'Petite (100-500)', 
                    'Moyenne (500-2k)', 'Grande (2k-10k)', 'Très grande (>10k)'],
            default=None,
            help="Filtrer par taille de commune"
        )
        
        # Dynamic slider bounds based on size categories
        slider_min = 0
        slider_max = 10000
        default_value = 0  # Changed from 1000 to 0 to include all communes by default
        
        if size_categories:
            if 'Très petite (<100)' in size_categories:
                slider_min = 0
                slider_max = 100
            elif 'Petite (100-500)' in size_categories:
                slider_min = 100
                slider_max = 500
            elif 'Moyenne (500-2k)' in size_categories:
                slider_min = 500
                slider_max = 2000
            elif 'Grande (2k-10k)' in size_categories:
                slider_min = 2000
                slider_max = 10000
            elif 'Très grande (>10k)' in size_categories:
                slider_min = 10000
                slider_max = 100000
            default_value = slider_min
        
        min_actifs = st.slider(
            "Min. actifs",
            min_value=slider_min,
            max_value=slider_max,
            value=default_value,
            step=100,
            help="Exclure les très petites communes"
        )
        
        filters = {
            'regions': selected_regions if selected_regions else None,
            'departments': selected_departments if selected_departments else None,
            'size_categories': size_categories if size_categories else None,
            'min_actifs': min_actifs
        }
        
        return filters


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    
    # Load custom CSS
    load_custom_css()
    
    # Load data
    try:
        commute_raw, geo_raw, complete_df = load_all_data()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        st.stop()
    
    # Render sidebar and get filter selections
    filters = render_sidebar(complete_df)
    
    # Apply filters to get filtered dataset
    filtered_df = filter_data(
        complete_df,
        regions=filters['regions'],
        departments=filters['departments'],
        size_categories=filters['size_categories'],
        min_actifs=filters['min_actifs']
    )
    
    # Calculate and display stats in sidebar after filters
    with st.sidebar:
        # Compact metrics display
        st.markdown("""
        <style>
        [data-testid="stMetric"] {
            text-align: center;
        }
        [data-testid="stMetricLabel"] {
            justify-content: center;
            text-align: center;
            display: flex;
            align-items: center;
            font-size: 0.8rem !important;
        }
        [data-testid="stMetricLabel"] > div {
            width: 100%;
            text-align: center;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.7rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        total_actifs = filtered_df['valeur'].sum()
        nb_communes = filtered_df['geocode_commune'].nunique()
        
        st.markdown("#### Sélection")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Actifs", f"{total_actifs/1_000_000:.1f}M")
        with col2:
            st.metric("Communes", f"{nb_communes:,}".replace(',', ' '))
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Introduction",
        "Vue d'ensemble",
        "Cartographie",
        "Analyses comparatives",
        "Conclusions"
    ])
    
    with tab1:
        intro.render()
    
    with tab2:
        if len(filtered_df) == 0:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            overview.render(filtered_df)
    
    with tab3:
        if len(filtered_df) == 0:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            deep_dives.render(filtered_df)
    
    with tab4:
        if len(filtered_df) == 0:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            comparisons.render(filtered_df)
    
    with tab5:
        conclusions.render(commute_raw, filtered_df)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
