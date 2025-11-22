import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import clean_and_prep_data, filter_data
from sections.intro import show_intro
from sections.overview import show_overview
from sections.deep_dives import show_deep_dives
from sections.conclusions import show_conclusions

# Page Config
st.set_page_config(
    page_title="La Fracture Mobile",
    page_icon="🚗",
    layout="wide"
)

# Load and Prep Data
with st.spinner('Chargement des données...'):
    df_raw = load_data()
    if not df_raw.empty:
        df_processed = clean_and_prep_data(df_raw)
    else:
        st.stop()

# Sidebar
with st.sidebar:
    st.title("Filtres")
    
    # Department Filter
    all_depts = sorted(df_processed['dept'].unique())
    selected_depts = st.multiselect("Sélectionner les Départements", all_depts, default=all_depts[:3] if len(all_depts) > 3 else all_depts)
    
    # Filter dataframe based on dept first to update commune list if needed (optional optimization)
    # For now, let's just filter at the end
    
    # Commune Filter (Optional, might be too long)
    # Let's filter communes based on selected depts
    available_communes = df_processed[df_processed['dept'].isin(selected_depts)]['libelle_commune'].unique()
    # selected_communes = st.multiselect("Sélectionner les Communes (Optionnel)", sorted(available_communes))
    
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio("Aller à", ["Introduction", "Vue d'ensemble", "Analyse détaillée", "Conclusions & Simulation"])

# Apply Filters
df_filtered = filter_data(df_processed, selected_depts)

# Main Content
if page == "Introduction":
    show_intro()
elif page == "Vue d'ensemble":
    show_overview(df_filtered)
elif page == "Analyse détaillée":
    show_deep_dives(df_filtered)
elif page == "Conclusions & Simulation":
    show_conclusions(df_filtered)

# Footer
st.markdown("---")
st.caption("Source: Flux domicile-travail selon le mode de transport principal utilisé - Data.gouv.fr")
