"""
Conclusions section: Key insights, data quality, and next steps.
"""

import streamlit as st
import pandas as pd
from utils.io import validate_data_quality


def render(df_raw: pd.DataFrame, df_filtered: pd.DataFrame):
    """
    Render the conclusions and data quality section.
    
    Args:
        df_raw: Original unfiltered dataset
        df_filtered: Current filtered dataset
    """
    
    st.markdown("## Conclusions et insights")
    
    st.markdown("""
    Après avoir exploré les données de mobilité de **25 millions d'actifs français**, 
    voici les conclusions principales et ce qu'elles signifient pour l'avenir.
    """)
    
    # Key Insights
    st.markdown("### Les 5 insights majeurs")
    
    insights = [
        {
            "title": "1. La voiture est reine absolue",
            "icon": "",
            "content": """
            Avec **65-75% des trajets domicile-travail**, la voiture écrase tous les autres modes. 
            Ce n'est pas un choix, c'est souvent une **contrainte** pour des millions de Français 
            sans alternative viable.
            """,
            "type": "error"
        },
        {
            "title": "2. La fracture territoriale est béante",
            "icon": "",
            "content": """
            Les grandes métropoles peuvent se permettre la mobilité durable. 
            Le reste du territoire est **prisonnier de la voiture**. C'est une question 
            d'**équité territoriale** avant d'être une question environnementale.
            """,
            "type": "warning"
        },
        {
            "title": "3. Le vélo : succès localisé, pas généralisé",
            "icon": "",
            "content": """
            Malgré le battage médiatique, le vélo reste < 5% des trajets au niveau national. 
            Mais dans certaines villes (Strasbourg, Bordeaux), il atteint **15-20%**. 
            La preuve que **l'infrastructure change les comportements**.
            """,
            "type": "info"
        },
        {
            "title": "4. Le télétravail : une solution partielle",
            "icon": "",
            "content": """
            Le "Pas de transport" a explosé post-Covid (5-10% selon les zones). 
            Mais c'est un **privilège de cadres urbains**. Les métiers manuels, 
            les services, la santé ne peuvent pas télétravailler.
            """,
            "type": "info"
        },
        {
            "title": "5. Effet de seuil : la densité est la clé",
            "icon": "",
            "content": """
            En dessous de **~1000 actifs**, il n'y a quasiment aucune alternative à la voiture. 
            La mobilité durable n'est **économiquement viable** qu'avec une densité minimale. 
            C'est le paradoxe : ceux qui en ont le plus besoin ne peuvent pas en bénéficier.
            """,
            "type": "success"
        }
    ]
    
    for insight in insights:
        icon_text = f"{insight['icon']} " if insight['icon'] else ""
        if insight["type"] == "error":
            with st.container():
                st.markdown(f"#### {icon_text}{insight['title']}")
                st.error(insight["content"])
        elif insight["type"] == "warning":
            with st.container():
                st.markdown(f"#### {icon_text}{insight['title']}")
                st.warning(insight["content"])
        elif insight["type"] == "info":
            with st.container():
                st.markdown(f"#### {icon_text}{insight['title']}")
                st.info(insight["content"])
        else:
            with st.container():
                st.markdown(f"#### {icon_text}{insight['title']}")
                st.success(insight["content"])
    
    st.markdown("---")
    
    # Implications
    st.markdown("### Implications et pistes d'action")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Pour les décideurs publics")
        st.markdown("""
        - **Arrêter le dogmatisme** : La solution vélo+TC ne fonctionne pas partout. 
          Il faut des solutions **différenciées** selon les territoires.
        
        - **Investir intelligemment** : Cibler les communes de 1k-10k actifs avec 
          forte dépendance automobile → ROI maximal.
        
        - **Covoiturage & autopartage** : Dans les zones rurales, optimiser la voiture 
          plutôt que la bannir.
        
        - **Aménagement du territoire** : Rapprocher habitat et emploi pour réduire 
          les distances (mixité fonctionnelle).
        """)
    
    with col2:
        st.markdown("#### Pour les entreprises")
        st.markdown("""
        - **Télétravail flexible** : Continuer à généraliser pour les postes compatibles.
        
        - **Mobilité douce** : Inciter vélo/TC via des primes, infrastructures 
          (parkings vélos sécurisés).
        
        - **Horaires décalés** : Réduire la congestion en étalant les arrivées.
        
        - **Localisation des bureaux** : Privilégier les zones bien desservies en TC.
        """)
    
    st.markdown("---")
    
    # Data Quality
    st.markdown("### Qualité des données et limitations")
    
    st.markdown("""
    Comme tout travail de Data Science, cette analyse a des **limites** qu'il faut connaître.
    """)
    
    with st.expander("Voir l'évaluation détaillée de la qualité des données"):
        # Validate data
        validation = validate_data_quality(df_raw)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Lignes Totales", f"{validation['total_rows']:,}".replace(',', ' '))
            st.metric("Lignes Dupliquées", validation['duplicate_rows'])
        
        with col2:
            st.metric("Communes Uniques", f"{validation['unique_communes']:,}".replace(',', ' '))
            st.metric("Valeurs Négatives", validation['negative_values'])
        
        with col3:
            date_min = validation['date_range']['min']
            date_max = validation['date_range']['max']
            st.metric("Période", f"{date_min.year}" if date_min else "N/A")
        
        st.markdown("#### Valeurs manquantes par colonne")
        
        missing_df = pd.DataFrame.from_dict(
            validation['missing_values'], 
            orient='index', 
            columns=['Valeurs Manquantes']
        )
        missing_df = missing_df[missing_df['Valeurs Manquantes'] > 0]
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("Aucune valeur manquante détectée !")
    
    st.markdown("#### Les biais et limites connus")
    
    limitations = [
        {
            "title": "Mode de transport principal uniquement",
            "desc": "Si quelqu'un fait vélo → train → vélo, seul le mode principal (train) est compté. On sous-estime donc l'intermodalité."
        },
        {
            "title": "Ambiguïté du 'Pas de transport'",
            "desc": "Mélange télétravail, travail à domicile (agriculteurs), et marche très courte. Impossible de distinguer."
        },
        {
            "title": "Données arrondies",
            "desc": "Pour le secret statistique, les petits effectifs sont arrondis/estimés. Les décimales sont des artefacts statistiques."
        },
        {
            "title": "Périmètre limité",
            "desc": "Uniquement les trajets domicile-travail. Exclut les courses, loisirs, sorties scolaires, etc."
        },
        {
            "title": "Snapshot temporel",
            "desc": "Données de 2022. Ne capture pas les évolutions récentes (inflation, ZFE, nouveaux RER métropolitains...)."
        }
    ]
    
    for lim in limitations:
        st.markdown(f"**• {lim['title']}** : {lim['desc']}")
    
    st.markdown("---")
    
    # Next Steps
    st.markdown("### Prochaines étapes & pistes d'amélioration")
    
    st.markdown("""
    Ce dashboard est un **point de départ**. Voici comment aller plus loin :
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Analyses complémentaires")
        st.markdown("""
        - **Évolution temporelle** : Comparer 2015 → 2022 pour voir les tendances.
        - **Croisement avec revenus** : Mobilité = question de pouvoir d'achat.
        - **Impact des infrastructures** : Corrélation avec km de pistes cyclables, lignes TC.
        - **Modélisation prédictive** : Prédire l'impact de nouvelles lignes TC.
        """)
    
    with col2:
        st.markdown("#### Améliorations techniques")
        st.markdown("""
        - **Données temps réel** : Intégrer des APIs de trafic pour dashboard dynamique.
        - **Clustering ML** : Identifier des "profils de communes" similaires.
        - **Simulation what-if** : "Si on ajoute une ligne de bus, quel impact ?"
        - **Export personnalisé** : Permettre aux collectivités de télécharger leurs données.
        """)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("### Contribuer et partager")
    
    st.info("""
    **Ce projet a été réalisé en Novembre 2025**
    
    - **Auteur** : Noé LACAILLE pour l'EFREI Paris
    - **Données** : Insee 2022 repris par Ecolab (Licence Ouverte)
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
        <p style='margin: 0;'>Dashboard créé avec Streamlit</p>
        <p style='margin: 0; font-size: 0.9rem;'>Données : Insee 2022 • Licence Ouverte</p>
    </div>
    """, unsafe_allow_html=True)
