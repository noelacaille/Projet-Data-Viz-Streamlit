"""
Deep dive section: Interactive maps and regional analysis.
"""

import streamlit as st
import pandas as pd
from utils.prep import compute_car_dependency_index, compute_sustainable_mobility_score
from utils.viz import create_choropleth_map, create_stacked_bar_chart, create_treemap


def render(df: pd.DataFrame):
    """
    Render the deep dive section with maps and regional comparisons.
    
    Args:
        df: Filtered complete dataset
    """
    
    st.markdown("## La carte des dépendances : analyse spatiale")
    
    st.markdown("""
    Cette section révèle la **géographie de la mobilité** en France.
    Chaque point sur la carte représente une commune, colorée selon sa dépendance automobile.
    """)
    
    # Choose analysis type
    analysis_type = st.selectbox(
        "Choisissez l'analyse :",
        options=["Dépendance automobile", "Score de mobilité durable"]
    )
    
    st.markdown("---")
    
    if "Automobile" in analysis_type:
        render_car_dependency_map(df)
    else:
        render_sustainable_mobility_map(df)
    
    st.markdown("---")
    
    # Regional comparison
    st.markdown("## Comparaison régionale")
    
    render_regional_comparison(df)


def render_car_dependency_map(df: pd.DataFrame):
    """Render the car dependency map."""
    
    st.markdown("### Carte de la dépendance automobile")
    
    st.markdown("""
    **Rouge foncé** = Forte dépendance (> 80% de voiture)  
    **Jaune** = Dépendance moyenne (50-80%)  
    **Vert** = Faible dépendance (< 50%)
    """)
    
    # Calculate car dependency
    with st.spinner("Calcul de l'indice de dépendance automobile..."):
        dependency_df = compute_car_dependency_index(df)
    
    if len(dependency_df) == 0:
        st.error("Aucune donnée disponible pour la sélection actuelle.")
        return
    
    # Map
    fig = create_choropleth_map(
        dependency_df,
        metric_col='indice_dependance_voiture',
        title=""
    )
    st.plotly_chart(fig, use_container_width=True, key="car_map")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_dep = dependency_df['indice_dependance_voiture'].mean()
        st.metric("Dépendance moyenne", f"{avg_dep:.1f}%")
    
    with col2:
        high_dep = len(dependency_df[dependency_df['indice_dependance_voiture'] > 80])
        st.metric("Communes > 80%", f"{high_dep:,}".replace(',', ' '))
    
    with col3:
        low_dep = len(dependency_df[dependency_df['indice_dependance_voiture'] < 50])
        st.metric("Communes < 50%", f"{low_dep:,}".replace(',', ' '))
    
    with col4:
        max_dep_commune = dependency_df.loc[dependency_df['indice_dependance_voiture'].idxmax()]
        st.metric(
            "Record", 
            f"{max_dep_commune['indice_dependance_voiture']:.1f}%",
            help=f"{max_dep_commune['nom_commune']} ({max_dep_commune['nom_departement']})"
        )
    
    # Top communes with highest car dependency
    st.markdown("#### Top 15 des communes les plus dépendantes de la voiture")
    
    top_dependent = dependency_df.nlargest(15, 'indice_dependance_voiture')[
        ['nom_commune', 'nom_departement', 'indice_dependance_voiture', 'total_actifs']
    ].reset_index(drop=True)
    
    top_dependent.columns = ['Commune', 'Département', 'Dépendance (%)', 'Actifs']
    top_dependent.index = range(1, len(top_dependent) + 1)
    
    st.dataframe(
        top_dependent,
        use_container_width=True,
        column_config={
            "Dépendance (%)": st.column_config.ProgressColumn(
                "Dépendance (%)",
                format="%.1f%%",
                min_value=0,
                max_value=100
            ),
            "Actifs": st.column_config.NumberColumn("Actifs", format="%d")
        }
    )
    
    st.warning("""
    **Observation** : Les communes les plus dépendantes sont souvent rurales ou périurbaines, 
    sans accès aux transports en commun. Pour ces territoires, la transition est un **défi majeur**.
    """)


def render_sustainable_mobility_map(df: pd.DataFrame):
    """Render the sustainable mobility score map."""
    
    st.markdown("### Carte du score de mobilité durable")
    
    st.markdown("""
    Ce score agrège les modes durables : **Vélo + Marche + TC + Télétravail**.  
    **Vert foncé** = Score élevé (champions de la mobilité durable)  
    **Jaune/Rouge** = Score faible (tout-voiture)
    """)
    
    # Calculate sustainability score
    with st.spinner("Calcul des scores de mobilité durable..."):
        scores_df = compute_sustainable_mobility_score(df)
    
    if len(scores_df) == 0:
        st.error("Aucune donnée disponible pour la sélection actuelle.")
        return
    
    # Map
    fig = create_choropleth_map(
        scores_df,
        metric_col='score_mobilite_durable',
        title=""
    )
    
    # Update color scale (reversed, green is good)
    fig.update_traces(
        marker=dict(colorscale='RdYlGn')  # Normal scale (green = high)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="sustainable_map")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = scores_df['score_mobilite_durable'].mean()
        st.metric("Score moyen", f"{avg_score:.1f}%")
    
    with col2:
        high_score = len(scores_df[scores_df['score_mobilite_durable'] > 40])
        st.metric("Communes > 40%", f"{high_score:,}".replace(',', ' '))
    
    with col3:
        low_score = len(scores_df[scores_df['score_mobilite_durable'] < 20])
        st.metric("Communes < 20%", f"{low_score:,}".replace(',', ' '))
    
    with col4:
        max_score_commune = scores_df.loc[scores_df['score_mobilite_durable'].idxmax()]
        st.metric(
            "Champion", 
            f"{max_score_commune['score_mobilite_durable']:.1f}%",
            help=f"{max_score_commune['nom_commune']} ({max_score_commune['nom_departement']})"
        )
    
    # Top sustainable communes
    st.markdown("#### Top 15 des champions de la mobilité durable")
    
    top_sustainable = scores_df.nlargest(15, 'score_mobilite_durable')[
        ['nom_commune', 'nom_departement', 'score_mobilite_durable', 'total_actifs']
    ].reset_index(drop=True)
    
    top_sustainable.columns = ['Commune', 'Département', 'Score Durable (%)', 'Actifs']
    top_sustainable.index = range(1, len(top_sustainable) + 1)
    
    st.dataframe(
        top_sustainable,
        use_container_width=True,
        column_config={
            "Score durable (%)": st.column_config.ProgressColumn(
                "Score durable (%)",
                format="%.1f%%",
                min_value=0,
                max_value=100
            ),
            "Actifs": st.column_config.NumberColumn("Actifs", format="%d")
        }
    )
    
    st.success("""
    **Observation** : Les communes avec les meilleurs scores sont souvent des **centres urbains** 
    (Paris, Lyon, Strasbourg) ou des **petites villes denses** avec une culture vélo forte.
    """)


def render_regional_comparison(df: pd.DataFrame):
    """Render regional comparison charts."""
    
    st.markdown("""
    Comment les **régions** se comparent-elles en termes de mobilité ? 
    Cette vue permet d'identifier les leaders et les retardataires.
    """)
    
    # Aggregate by region
    regional = df.groupby(['nom_region', 'mode_transport']).agg({
        'valeur': 'sum'
    }).reset_index()
    
    # Calculate percentages
    regional_totals = regional.groupby('nom_region')['valeur'].sum().reset_index()
    regional_totals.columns = ['nom_region', 'total']
    
    regional = regional.merge(regional_totals, on='nom_region')
    regional['pourcentage'] = (regional['valeur'] / regional['total'] * 100).round(1)
    
    # Sort by car percentage (descending)
    car_by_region = regional[regional['mode_transport'] == 'Voiture'].sort_values('pourcentage', ascending=False)
    region_order = car_by_region['nom_region'].tolist()
    
    regional['nom_region'] = pd.Categorical(regional['nom_region'], categories=region_order, ordered=True)
    regional = regional.sort_values('nom_region')
    
    # Stacked bar chart
    fig = create_stacked_bar_chart(
        regional,
        x_col='nom_region',
        y_col='pourcentage',
        color_col='mode_transport',
        title=""
    )
    
    # Update specific properties without conflicting with template
    fig.update_xaxes(tickangle=-45)
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(height=600)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Régions les **moins** dépendantes de la voiture")
        
        best_regions = car_by_region.tail(5)[['nom_region', 'pourcentage']].reset_index(drop=True)
        best_regions.columns = ['Région', 'Voiture (%)']
        best_regions.index = range(1, len(best_regions) + 1)
        
        st.dataframe(best_regions, use_container_width=True)
        
        st.info("""
        Ces régions ont souvent des **métropoles denses** avec des réseaux de 
        transport développés (Île-de-France, Grand Est avec Strasbourg...).
        """)
    
    with col2:
        st.markdown("#### Régions les **plus** dépendantes de la voiture")
        
        worst_regions = car_by_region.head(5)[['nom_region', 'pourcentage']].reset_index(drop=True)
        worst_regions.columns = ['Région', 'Voiture (%)']
        worst_regions.index = range(1, len(worst_regions) + 1)
        
        st.dataframe(worst_regions, use_container_width=True)
        
        st.warning("""
        Ces régions, souvent rurales ou montagneuses, ont **peu d'alternatives**. 
        La politique de mobilité ne peut pas être uniforme sur le territoire.
        """)
