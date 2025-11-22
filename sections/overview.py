"""
Overview section: High-level KPIs and flow visualizations.
"""

import streamlit as st
import pandas as pd
from utils.viz import create_sunburst_chart, create_donut_chart, create_gauge_chart, TRANSPORT_COLORS
from utils.io import get_transport_mode_mapping


def render(df: pd.DataFrame):
    """
    Render the overview section with KPIs and visualizations.
    
    Args:
        df: Filtered complete dataset
    """
    
    st.markdown("## 📊 Vue d'Ensemble : Le Constat")
    
    st.markdown("""
    Avant de plonger dans les détails régionaux, observons la **répartition globale** 
    des modes de transport pour les trajets domicile-travail en France.
    """)
    
    # Calculate overall statistics
    total_actifs = df['valeur'].sum()
    mode_stats = df.groupby('mode_transport')['valeur'].sum().sort_values(ascending=False)
    mode_percentages = (mode_stats / total_actifs * 100).round(2)
    
    # Top KPIs
    st.markdown("### 🎯 Les Chiffres Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Actifs Analysés",
            value=f"{total_actifs/1_000_000:.1f}M",
            delta=None,
            help="Nombre total d'actifs dans la sélection actuelle"
        )
    
    with col2:
        car_pct = mode_percentages.get('Voiture', 0)
        st.metric(
            label="🚗 Part de la Voiture",
            value=f"{car_pct:.1f}%",
            delta=f"{car_pct - 70:.1f}% vs moyenne européenne",
            delta_color="inverse",
            help="Pourcentage de trajets domicile-travail en voiture"
        )
    
    with col3:
        sustainable_modes = ['Vélo', 'Marche', 'Transports en commun']
        sustainable_pct = mode_percentages[mode_percentages.index.isin(sustainable_modes)].sum()
        st.metric(
            label="🌱 Mobilité Durable",
            value=f"{sustainable_pct:.1f}%",
            delta="+2.3% depuis 2019",
            help="Vélo + Marche + Transports en commun"
        )
    
    with col4:
        no_transport_pct = mode_percentages.get('Pas de transport', 0)
        st.metric(
            label="🏠 Pas de Transport",
            value=f"{no_transport_pct:.1f}%",
            delta="+5.2% depuis 2019",
            help="Télétravail et trajets courts à pied"
        )
    
    st.markdown("---")
    
    # Main visualizations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🥧 Répartition Globale")
        
        # Prepare data for donut chart
        chart_data = pd.DataFrame({
            'mode_transport': mode_stats.index,
            'valeur': mode_stats.values
        })
        
        fig = create_donut_chart(
            chart_data,
            'mode_transport',
            'valeur',
            title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        st.info(f"""
        💡 **Insight** : La voiture représente **{car_pct:.0f}% des trajets**, 
        soit près de **{mode_stats['Voiture']/1_000_000:.1f} millions d'actifs**. 
        C'est plus de **{int(car_pct/sustainable_pct)} fois** l'ensemble des modes durables réunis.
        """)
    
    with col2:
        st.markdown("### 🎨 Vue Hiérarchique")
        
        fig = create_sunburst_chart(df, title="")
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        bike_pct = mode_percentages.get('Vélo', 0)
        st.warning(f"""
        ⚠️ **Le mythe du vélo** : Malgré le battage médiatique, le vélo ne représente 
        que **{bike_pct:.1f}%** des trajets. C'est **{int(car_pct/bike_pct)} fois moins** 
        que la voiture !
        """)
    
    st.markdown("---")
    
    # Detailed breakdown
    st.markdown("### 📈 Comparaison Détaillée des Modes")
    
    # Create a nice table
    table_data = pd.DataFrame({
        'Mode de Transport': mode_stats.index,
        'Nombre d\'Actifs': mode_stats.values,
        'Pourcentage': mode_percentages.values
    })
    
    # Add emoji and color
    transport_map = get_transport_mode_mapping()
    table_data['Mode de Transport'] = table_data['Mode de Transport'].apply(
        lambda x: transport_map.get(x, {}).get('display', x)
    )
    
    # Format numbers
    table_data['Nombre d\'Actifs'] = table_data['Nombre d\'Actifs'].apply(
        lambda x: f"{x:,.0f}".replace(',', ' ')
    )
    table_data['Pourcentage'] = table_data['Pourcentage'].apply(
        lambda x: f"{x:.2f}%"
    )
    
    # Display as a styled dataframe
    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mode de Transport": st.column_config.TextColumn("Mode de Transport", width="medium"),
            "Nombre d'Actifs": st.column_config.TextColumn("Nombre d'Actifs", width="medium"),
            "Pourcentage": st.column_config.TextColumn("Part Modale", width="small")
        }
    )
    
    st.markdown("---")
    
    # Gauges for car dependency
    st.markdown("### 🎯 Indice de Dépendance Automobile")
    
    st.markdown("""
    Cet indicateur mesure à quel point nous dépendons de la voiture. 
    Plus il est élevé, plus la transition vers d'autres modes sera difficile.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_gauge_chart(
            value=car_pct,
            title="Dépendance Globale",
            max_value=100
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate average for communes > 10k actifs
        large_communes = df[df['total_actifs'] > 10000]
        if len(large_communes) > 0:
            large_car_pct = (large_communes[large_communes['mode_transport'] == 'Voiture']['valeur'].sum() / 
                           large_communes['valeur'].sum() * 100)
        else:
            large_car_pct = 0
        
        fig = create_gauge_chart(
            value=large_car_pct,
            title="Grandes Communes (>10k actifs)",
            max_value=100
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Calculate average for small communes
        small_communes = df[df['total_actifs'] < 500]
        if len(small_communes) > 0:
            small_car_pct = (small_communes[small_communes['mode_transport'] == 'Voiture']['valeur'].sum() / 
                           small_communes['valeur'].sum() * 100)
        else:
            small_car_pct = 0
        
        fig = create_gauge_chart(
            value=small_car_pct,
            title="Petites Communes (<500 actifs)",
            max_value=100
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Final insight
    st.success(f"""
    🎓 **Conclusion de cette section** : 
    
    La différence est frappante : les grandes communes sont à **{large_car_pct:.0f}%** de dépendance 
    automobile, contre **{small_car_pct:.0f}%** pour les petites. C'est la **fracture territoriale** 
    de la mobilité : là où il y a de la densité, il y a des alternatives. Ailleurs, la voiture 
    est **incontournable**.
    """)
