"""
Introduction section: Context, objectives, and data overview.
"""

import streamlit as st
from utils.io import get_data_license


def render():
    """Render the introduction section."""
    
    # Hero section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem; border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>
            🚗 La Fracture de la Mobilité
        </h1>
        <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; margin-top: 1rem; margin-bottom: 0;'>
            La France est-elle vraiment prête à lâcher la voiture ?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # The Hook
    st.markdown("### 🎯 Pourquoi cette question ?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Alors que les **zones à faibles émissions** (ZFE) se multiplient dans les centres-villes, 
        que les **prix du carburant** explosent, et que le **changement climatique** impose 
        une transformation radicale de nos modes de vie, une question se pose avec urgence :
        
        **Peut-on vraiment se passer de la voiture en France ?**
        
        Ce dashboard explore les **données réelles** des déplacements domicile-travail de 
        **25 millions d'actifs français** pour révéler les fractures invisibles de la mobilité.
        """)
    
    with col2:
        st.info("""
        **📊 Les Données**
        
        - 🗓️ **Année** : 2022
        - 👥 **Actifs** : 25M+
        - 🏘️ **Communes** : 36 000
        - 🚌 **Modes** : 6 catégories
        """)
    
    st.markdown("---")
    
    # The Context
    st.markdown("### 📖 Le Contexte")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🌍 Crise Climatique
        Le secteur des **transports** représente 
        **31% des émissions de CO₂** en France.
        La voiture individuelle en est le 
        principal responsable.
        """)
    
    with col2:
        st.markdown("""
        #### 🏙️ Centres vs Périphérie
        Les grandes métropoles investissent 
        massivement dans les **transports en commun**,
        mais qu'en est-il des **zones rurales** 
        et **périurbaines** ?
        """)
    
    with col3:
        st.markdown("""
        #### 💼 Post-Covid
        Le **télétravail** a explosé depuis 2020.
        Est-ce une vraie solution ou un 
        privilège de **cadres urbains** ?
        """)
    
    st.markdown("---")
    
    # The Questions
    st.markdown("### 🔍 Les Questions Clés")
    
    questions = [
        "**La Voiture est-elle vraiment reine ?** À quel point la France dépend-elle de la voiture pour les trajets domicile-travail ?",
        "**La Révolution Vélo : mythe ou réalité ?** En dehors des centres-villes, le vélo est-il une alternative crédible ?",
        "**Le Télétravail : qui en profite ?** Quelles communes ont le plus fort taux de 'Pas de transport' ?",
        "**Les Zones Blanches : où sont-elles ?** Où n'existe-t-il aucune alternative à la voiture ?",
        "**Le Potentiel de Changement : qui peut basculer ?** Quelles villes ont la taille critique pour développer des alternatives ?"
    ]
    
    for i, q in enumerate(questions, 1):
        st.markdown(f"{i}. {q}")
    
    st.markdown("---")
    
    # Data Overview
    st.markdown("### 📊 À Propos des Données")
    
    with st.expander("🔎 Voir les détails techniques et les limitations"):
        st.markdown(get_data_license())
        
        st.markdown("#### ⚠️ Limitations et Précautions")
        st.warning("""
        **Interprétation de "Pas de transport"** : Cette catégorie peut inclure :
        - Le télétravail (travail à domicile)
        - Les personnes travaillant sur leur lieu de résidence (agriculteurs, commerçants)
        - Les trajets à pied très courts (< 5 min)
        
        Il est donc difficile d'isoler le vrai télétravail des autres cas.
        """)
        
        st.info("""
        **Données arrondies** : Pour respecter le secret statistique, l'Insee arrondit 
        les petits effectifs. Les valeurs décimales que vous voyez sont des estimations 
        statistiques, pas des comptages exacts.
        """)
        
        st.markdown("""
        **Périmètre** : 
        - Actifs de **15 ans ou plus**
        - Uniquement les trajets **domicile-travail** (pas les autres déplacements)
        - Mode de transport **principal** (si quelqu'un fait vélo + train, seul le principal est compté)
        """)
    
    st.markdown("---")
    
    # Navigation hint
    st.success("""
    👉 **Explorez le dashboard** en utilisant les filtres dans la barre latérale et 
    naviguez entre les différentes sections pour découvrir les insights.
    """)
