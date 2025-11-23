"""
Comparative analysis section: Rankings, correlations, and insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.prep import get_top_communes_by_mode, compute_modal_shift_potential
from utils.viz import create_horizontal_bar_chart, create_scatter_plot, TRANSPORT_COLORS


def render(df: pd.DataFrame):
    """
    Render the comparative analysis section.
    
    Args:
        df: Filtered complete dataset
    """
    
    st.markdown("## Analyse comparative : disparités et champions")
    
    st.markdown("""
    Au-delà des moyennes, explorons les **extrêmes** et les **corrélations** pour 
    identifier ce qui fonctionne et ce qui ne fonctionne pas.
    """)
    
    # Mode selector
    st.markdown("### Les champions par mode de transport")
    
    mode_choice = st.selectbox(
        "Sélectionnez un mode de transport :",
        options=['Vélo', 'Transports en commun', 'Marche', 'Pas de transport', 'Deux-roues motorisé'],
        index=0
    )
    
    render_top_communes(df, mode_choice)
    
    st.markdown("---")
    
    # Correlation analysis
    st.markdown("### Taille de commune vs Mobilité durable")
    
    render_size_correlation(df)
    
    st.markdown("---")
    
    # Modal shift potential
    st.markdown("### Potentiel de report modal")
    
    render_modal_shift_analysis(df)


def render_top_communes(df: pd.DataFrame, mode: str):
    """Render top communes for a specific transport mode."""
    
    st.markdown(f"#### Top 20 des communes pour : **{mode}**")
    
    st.caption("Communes avec au moins 100 actifs")
    
    # Get top communes
    with st.spinner("Calcul des classements..."):
        top = get_top_communes_by_mode(df, mode, n=20)
    
    if len(top) == 0:
        st.warning(f"Aucune commune avec suffisamment de données pour le mode '{mode}'.")
        return
    
    # Create a combined label for better display
    top['label'] = top['nom_commune'] + ' (' + top['nom_departement'] + ')'
    
    # Horizontal bar chart
    fig = create_horizontal_bar_chart(
        top,
        x_col='pourcentage',
        y_col='label',
        title=""
    )
    
    fig.update_traces(marker_color=TRANSPORT_COLORS.get(mode, '#95a5a6'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    with st.expander("Voir le tableau détaillé"):
        display_df = top[['nom_commune', 'nom_departement', 'pourcentage', 'valeur', 'total_actifs']].copy()
        display_df.columns = ['Commune', 'Département', 'Part (%)', 'Utilisateurs', 'Total Actifs']
        display_df.index = range(1, len(display_df) + 1)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Part (%)": st.column_config.NumberColumn("Part (%)", format="%.1f%%"),
                "Utilisateurs": st.column_config.NumberColumn("Utilisateurs", format="%.0f"),
                "Total Actifs": st.column_config.NumberColumn("Total Actifs", format="%d")
            }
        )
    
    # Mode-specific insights
    if mode == 'Vélo':
        st.info("""
        **Insight Vélo** : Les champions du vélo sont souvent des **villes moyennes** 
        (Strasbourg, Bordeaux, Grenoble) avec une **infrastructure cyclable** développée 
        et une **culture vélo** forte. La topographie compte aussi : les villes plates dominent.
        """)
    
    elif mode == 'Transports en commun':
        st.info("""
        **Insight TC** : Sans surprise, les grandes métropoles dominent. Mais notez que 
        même dans ces villes, les TC restent souvent **minoritaires** face à la voiture. 
        Seules Paris et quelques centres atteignent > 30%.
        """)
    
    elif mode == 'Pas de transport':
        st.info("""
        **Insight Télétravail** : Cette catégorie mélange télétravail et résidence sur lieu 
        de travail. Les scores élevés peuvent indiquer soit des **zones résidentielles aisées** 
        (cadres en télétravail) soit des **zones agricoles** (agriculteurs).
        """)
    
    elif mode == 'Marche':
        st.info("""
        **Insight Marche** : La marche domine dans les **centres-villes denses** où 
        logement et emploi sont proches. C'est aussi un indicateur de **mixité fonctionnelle**.
        """)


def render_size_correlation(df: pd.DataFrame):
    """Render correlation between commune size and sustainable mobility."""
    
    st.markdown("""
    **Question** : Y a-t-il un **seuil de taille** à partir duquel les alternatives 
    à la voiture deviennent viables ?
    """)
    
    # Calculate sustainable modes percentage per commune
    sustainable_modes = ['Vélo', 'Marche', 'Transports en commun']
    
    # Pivot to get modes as columns
    pivot = df.pivot_table(
        index=['geocode_commune', 'nom_commune', 'total_actifs', 'nom_departement'],
        columns='mode_transport',
        values='pourcentage',
        fill_value=0
    ).reset_index()
    
    # Calculate sustainable mobility score
    for mode in sustainable_modes:
        if mode not in pivot.columns:
            pivot[mode] = 0
    
    pivot['score_durable'] = pivot[sustainable_modes].sum(axis=1)
    
    # Filter outliers and small communes
    pivot = pivot[(pivot['total_actifs'] >= 100) & (pivot['total_actifs'] <= 50000)]
    
    if len(pivot) == 0:
        st.warning("Pas assez de données pour cette analyse.")
        return
    
    # Add size category for coloring
    pivot['categorie'] = pd.cut(
        pivot['total_actifs'],
        bins=[0, 500, 2000, 10000, 50000],
        labels=['Petite', 'Moyenne', 'Grande', 'Très grande']
    )
    
    # Scatter plot
    fig = create_scatter_plot(
        pivot,
        x_col='total_actifs',
        y_col='score_durable',
        color_col='categorie',
        size_col='total_actifs',
        title="",
        x_label="Nombre d'actifs (log scale)",
        y_label="Score de mobilité durable (%)"
    )
    
    # Use log scale for x-axis
    fig.update_xaxes(type='log')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate correlation
    correlation = pivot[['total_actifs', 'score_durable']].corr().iloc[0, 1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Corrélation", f"{correlation:.3f}")
    
    with col2:
        threshold = pivot[pivot['score_durable'] > 30]['total_actifs'].min()
        st.metric("Seuil > 30% durable", f"{threshold:,.0f} actifs".replace(',', ' '))
    
    with col3:
        high_score_pct = len(pivot[pivot['score_durable'] > 30]) / len(pivot) * 100
        st.metric("Communes > 30%", f"{high_score_pct:.1f}%")
    
    st.success(f"""
    ✅ **Conclusion** : La corrélation est **{correlation:.2f}**, confirmant qu'il existe un 
    **effet de seuil**. En dessous de ~{threshold:,.0f} actifs, les alternatives à la voiture 
    sont quasi inexistantes. C'est le **paradoxe de la mobilité durable** : elle nécessite 
    une densité minimale pour être viable économiquement.
    """)


def render_modal_shift_analysis(df: pd.DataFrame):
    """Render analysis of modal shift potential."""
    
    st.markdown("""
    **Question** : Quelles communes ont le plus grand **potentiel de report modal** 
    (passer de la voiture à des alternatives) ?
    
    On identifie les communes qui cumulent :
    - Taille suffisante (> 1000 actifs)
    - Forte dépendance automobile (> 80%)
    - Potentiel d'action pour les politiques publiques
    """)
    
    # Calculate modal shift potential
    with st.spinner("Analyse du potentiel de report modal..."):
        potential_df = compute_modal_shift_potential(df)
    
    if len(potential_df) == 0:
        st.info("Aucune commune ne correspond aux critères dans la sélection actuelle.")
        return
    
    st.markdown(f"""
    **{len(potential_df)} communes** identifiées avec un fort potentiel de transformation.
    """)
    
    # Top 20 communes by transferable workers
    top_potential = potential_df.head(20).copy()
    top_potential['label'] = (top_potential['nom_commune'] + 
                              ' (' + top_potential['nom_departement'] + ')')
    
    # Horizontal bar chart
    fig = create_horizontal_bar_chart(
        top_potential,
        x_col='actifs_transferables',
        y_col='label',
        title=""
    )
    
    # Update specific properties without conflicting with template
    fig.update_xaxes(title='Actifs transférables (estimation -20%)')
    fig.update_layout(height=600)
    
    fig.update_traces(marker_color=COLORS['warning'])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_potential = potential_df['actifs_transferables'].sum()
        st.metric(
            "Potentiel total",
            f"{total_potential/1000:.0f}k actifs",
            help="Si 20% des automobilistes passaient à d'autres modes"
        )
    
    with col2:
        avg_dep = potential_df['pourcentage'].mean()
        st.metric(
            "Dépendance moyenne",
            f"{avg_dep:.1f}%",
            help="Moyenne pour ces communes"
        )
    
    with col3:
        co2_savings = total_potential * 2.5 * 220 / 1000  # 2.5 kg CO2/trajet, 220 jours
        st.metric(
            "Économie CO₂ potentielle",
            f"{co2_savings/1000:.0f}k tonnes/an",
            help="Estimation basée sur 2.5kg CO2 / trajet"
        )
    
    # Detailed table
    with st.expander("Voir le tableau détaillé"):
        display_df = potential_df[['nom_commune', 'nom_departement', 'pourcentage', 
                                    'total_actifs', 'actifs_transferables']].head(30).copy()
        display_df.columns = ['Commune', 'Département', 'Dépendance (%)', 
                              'Total Actifs', 'Potentiel Transfert']
        display_df.index = range(1, len(display_df) + 1)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Dépendance (%)": st.column_config.NumberColumn("Dépendance (%)", format="%.1f%%"),
                "Total Actifs": st.column_config.NumberColumn("Total Actifs", format="%d"),
                "Potentiel Transfert": st.column_config.NumberColumn("Potentiel Transfert", format="%.0f")
            }
        )
    
    st.warning("""
    **Note méthodo** : Le "potentiel de transfert" est une **estimation théorique** 
    basée sur l'hypothèse qu'avec des infrastructures adaptées, 20% des automobilistes 
    pourraient changer de mode. C'est un indicateur de **priorisation** pour les investissements, 
    pas une prédiction précise.
    """)


# Import colors
from utils.viz import COLORS
