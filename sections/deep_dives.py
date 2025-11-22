import streamlit as st
from utils.viz import plot_top_flop_communes, plot_scatter_size_vs_mode, plot_boxplot_distribution

def show_deep_dives(df_filtered):
    st.header("Analyse des Disparités")
    
    if df_filtered.empty:
        st.warning("Aucune donnée disponible.")
        return

    st.subheader("Top & Flop : Dépendance à la Voiture")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Les plus dépendants de la voiture**")
        fig_top = plot_top_flop_communes(df_filtered, mode="Voiture", top_n=10)
        if fig_top:
            st.plotly_chart(fig_top, use_container_width=True)
            
    with col2:
        st.markdown("**Les moins dépendants (Top Transports en commun)**")
        fig_flop = plot_top_flop_communes(df_filtered, mode="Transports en commun", top_n=10)
        if fig_flop:
            st.plotly_chart(fig_flop, use_container_width=True)

    st.subheader("Corrélation : Taille de la commune vs Usage Voiture")
    fig_scatter = plot_scatter_size_vs_mode(df_filtered, mode="Voiture")
    if fig_scatter:
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.subheader("Distribution par Département")
    fig_box = plot_boxplot_distribution(df_filtered, mode="Voiture")
    if fig_box:
        st.plotly_chart(fig_box, use_container_width=True)
