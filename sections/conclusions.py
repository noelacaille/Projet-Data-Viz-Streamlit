import streamlit as st

def show_conclusions(df_filtered):
    st.header("Zoom sur les Mobilités Douces & Simulation")
    
    st.markdown("""
    ### Insights
    L'analyse montre souvent une corrélation inverse entre la densité urbaine et l'usage de la voiture.
    Les zones rurales restent fortement dépendantes de l'automobile, faute d'alternatives.
    """)
    
    st.subheader("Simulation 'What-if'")
    st.markdown("Imaginez un report modal de la voiture vers les transports en commun.")
    
    if df_filtered.empty:
        return

    # Calculate current totals
    total_voiture = df_filtered['Voiture'].sum()
    
    transfer_pct = st.slider("Pourcentage de report modal (Voiture -> TC)", 0, 50, 10, step=1)
    
    transferred_people = total_voiture * (transfer_pct / 100)
    
    st.metric(
        label=f"Personnes transférées vers les TC (avec {transfer_pct}% de report)",
        value=f"{int(transferred_people):,}",
        delta=f"-{int(transferred_people):,} voitures"
    )
    
    st.success(f"Un report de {transfer_pct}% permettrait de retirer {int(transferred_people):,} voitures des routes sur la zone sélectionnée.")
