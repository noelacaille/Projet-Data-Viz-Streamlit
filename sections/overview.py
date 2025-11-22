import streamlit as st
from utils.viz import plot_mode_distribution

def show_overview(df_filtered):
    st.header("Vue d'ensemble")
    
    if df_filtered.empty:
        st.warning("Aucune donnée disponible pour la sélection actuelle.")
        return

    # KPIs
    total_actifs = df_filtered['Total_Actifs'].sum()
    
    # Calculate global percentages for KPIs
    # Sum of values for each mode
    mode_cols = [c for c in df_filtered.columns if c.startswith('pct_')]
    # We need raw sums to calculate global percentage, not average of percentages
    # Re-identify raw columns based on pct columns
    raw_cols = [c.replace('pct_', '') for c in mode_cols]
    
    sums = df_filtered[raw_cols].sum()
    global_pcts = (sums / total_actifs) * 100
    
    pct_voiture = global_pcts.get('Voiture', 0)
    pct_tc = global_pcts.get('Transports en commun', 0)
    
    # Find the commune with lowest car usage (Champion Ecologie)
    # Filter out very small communes to avoid outliers with 1 person
    df_significant = df_filtered[df_filtered['Total_Actifs'] > 100]
    if not df_significant.empty:
        champion = df_significant.loc[df_significant['pct_Voiture'].idxmin()]
        champion_name = champion['libelle_commune']
        champion_val = champion['pct_Voiture']
    else:
        champion_name = "N/A"
        champion_val = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Volume Total Actifs", f"{int(total_actifs):,}")
    col2.metric("Part Modale Voiture", f"{pct_voiture:.1f}%")
    col3.metric("Champion Écologie (Min Voiture)", f"{champion_name} ({champion_val:.1f}%)")
    
    st.subheader("Répartition des modes de transport")
    fig_pie = plot_mode_distribution(df_filtered)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Map placeholder (Implementing a full map might be heavy, let's see if we can do a simple scatter mapbox or similar if we had lat/lon)
    # The dataset has 'geocode_commune' but not lat/lon directly. 
    # Usually we need to join with a geojson or a lat/lon dataset.
    # For now, I will skip the map or put a placeholder message as I don't have the geojson in the file list.
    # The user prompt mentioned "Carte Choroplèthe: Carte de la zone sélectionnée...".
    # Without a geojson file in the workspace, I cannot easily render a choropleth map of French communes.
    # I will add a note about this.
    
    st.info("Note: La carte interactive nécessite des données géographiques (GeoJSON) non incluses dans le dataset principal.")
