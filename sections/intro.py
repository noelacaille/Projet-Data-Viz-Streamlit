import streamlit as st

def show_intro():
    st.title("La Fracture Mobile : Comment la France se déplace-t-elle au travail ?")
    
    st.markdown("""
    ### Contexte
    La voiture reste reine en France, mais son hégémonie masque de profondes disparités territoriales.
    Existe-t-il une France à deux vitesses entre les pôles urbains (transports en commun) et les territoires ruraux (dépendance automobile) ? 
    Où se situent les nouvelles mobilités ?
    
    ### Objectifs
    Ce tableau de bord vise à :
    *   Identifier les zones de "dépendance critique" à la voiture.
    *   Mettre en lumière les "champions de la mobilité douce".
    *   Explorer les corrélations entre la taille des communes et les modes de transport.
    
    ### Données
    Les données proviennent du jeu de données public : **Flux domicile-travail selon le mode de transport principal utilisé**.
    Elles recensent le mode de transport principal déclaré par les actifs de 15 ans ou plus se déplaçant pour travailler.
    
    **Limitations :**
    *   Les chiffres sont des estimations.
    *   La catégorie "Pas de transport" inclut généralement la marche à pied ou le télétravail (si non spécifié autrement).
    """)
    
    st.info("Utilisez le menu latéral pour filtrer les données par région ou département.")
