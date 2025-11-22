"""
Main Streamlit application for the Mobility Dashboard.

🚗 La Fracture de la Mobilité : La France est-elle vraiment prête à lâcher la voiture ?

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
    page_title="La Fracture de la Mobilité | Dashboard",
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
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700;
        color: #2c3e50;
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
        border-bottom: 3px solid #3498db;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        color: #34495e;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: white;
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
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

@st.cache_data(show_spinner="📊 Chargement des données...")
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
        <div style='text-align: center; padding: 1rem 0 2rem 0;'>
            <h1 style='color: white; margin: 0; font-size: 1.8rem;'>🚗 Mobilité France</h1>
            <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem;'>Filtres & Navigation</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Region filter
        st.markdown("### 🗺️ Filtres Géographiques")
        
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
        
        st.markdown("---")
        
        # Size filters
        st.markdown("### 👥 Taille des Communes")
        
        size_categories = st.multiselect(
            "Catégories de taille",
            options=['Très petite (<100)', 'Petite (100-500)', 
                    'Moyenne (500-2k)', 'Grande (2k-10k)', 'Très grande (>10k)'],
            default=None,
            help="Filtrer par taille de commune"
        )
        
        min_actifs = st.slider(
            "Minimum d'actifs",
            min_value=0,
            max_value=10000,
            value=0,
            step=100,
            help="Exclure les très petites communes"
        )
        
        st.markdown("---")
        
        # Info section
        st.markdown("### ℹ️ À Propos")
        st.markdown("""
        <p style='color: rgba(255,255,255,0.9); font-size: 0.9rem;'>
        Ce dashboard analyse les trajets domicile-travail de 25M+ d'actifs français.
        </p>
        """, unsafe_allow_html=True)
        
        # Stats about current selection
        st.markdown("---")
        st.markdown("### 📊 Sélection Actuelle")
        
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
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        st.stop()
    
    # Sidebar filters
    filters = render_sidebar(complete_df)
    
    # Apply filters
    filtered_df = filter_data(
        complete_df,
        regions=filters['regions'],
        departments=filters['departments'],
        size_categories=filters['size_categories'],
        min_actifs=filters['min_actifs']
    )
    
    # Show filter stats in sidebar
    with st.sidebar:
        total_actifs = filtered_df['valeur'].sum()
        nb_communes = filtered_df['geocode_commune'].nunique()
        
        st.metric("Actifs", f"{total_actifs/1_000_000:.1f}M")
        st.metric("Communes", f"{nb_communes:,}".replace(',', ' '))
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Introduction",
        "📊 Vue d'Ensemble",
        "🗺️ Cartographie",
        "🔬 Analyses Comparatives",
        "🎓 Conclusions"
    ])
    
    with tab1:
        intro.render()
    
    with tab2:
        if len(filtered_df) == 0:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            overview.render(filtered_df)
    
    with tab3:
        if len(filtered_df) == 0:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            deep_dives.render(filtered_df)
    
    with tab4:
        if len(filtered_df) == 0:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Ajustez vos filtres.")
        else:
            comparisons.render(filtered_df)
    
    with tab5:
        conclusions.render(commute_raw, filtered_df)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
