# La Fracture Mobile : Dashboard Streamlit

Ce projet est une application de data storytelling construite avec Streamlit, analysant les flux domicile-travail en France.

## Objectifs
L'application vise à explorer les disparités d'usage de la voiture versus les transports en commun et les mobilités douces à travers le territoire français.

## Données
Le jeu de données utilisé est "Flux domicile-travail selon le mode de transport principal utilisé".
Il contient des estimations du nombre d'actifs utilisant différents modes de transport pour se rendre au travail, par commune.

## Structure du Projet
*   `app.py` : Point d'entrée de l'application.
*   `sections/` : Modules contenant le code pour chaque page de l'application.
*   `utils/` : Fonctions utilitaires pour le chargement, la préparation et la visualisation des données.
*   `data/` : Dossier contenant les fichiers CSV.

## Installation et Exécution

1.  Cloner le dépôt ou extraire l'archive.
2.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3.  Lancer l'application :
    ```bash
    streamlit run app.py
    ```

## Auteur
Projet réalisé dans le cadre du cours de Data Visualization.
