# La fracture de la mobilite : La France est-elle vraiment prete a lacher la voiture ?

Ce projet est un tableau de bord interactif realise avec Streamlit, explorant les habitudes de deplacement domicile-travail en France. Il s'appuie sur les donnees du recensement de l'INSEE (2022) pour mettre en lumiere les disparites territoriales en matiere de mobilite.

## Description

L'application vise a visualiser et analyser la dependance a la voiture et l'adoption des modes de transport durables a travers le territoire francais. Elle permet d'identifier les zones de forte dependance automobile, de comparer les regions et les communes, et d'evaluer le potentiel de report modal.

## Fonctionnalites

Le tableau de bord est structure en plusieurs sections cles :

1.  **Introduction** : Presentation du contexte, des objectifs et vue d'ensemble des donnees (nombre d'actifs, communes couvertes, modes de transport).
2.  **Vue d'ensemble** : Indicateurs cles de performance (KPI) et visualisations des flux (diagrammes solaires, graphiques en anneau, jauges) pour comprendre la repartition globale des modes de transport.
3.  **Analyse spatiale (Cartographie)** : Cartes interactives et analyses regionales. Cette section presente des indices de dependance a la voiture et des scores de mobilite durable pour visualiser les fractures territoriales.
4.  **Analyse comparative** : Classements des communes et regions, correlations entre variables et identification des "champions" de la mobilite durable. Elle explore egalement le potentiel de report modal.
5.  **Conclusions** : Synthese des insights cles tires de l'analyse et evaluation de la qualite des donnees.

## Installation et Utilisation

### Pre-requis

*   Python 3.8+
*   Les bibliotheques dans `requirements.txt`

### Lancement de l'application

Pour lancer le tableau de bord en local, executez la commande suivante :

```bash
python -m streamlit run app.py
```

L'application sera accessible dans votre navigateur a l'adresse indiquee (`http://localhost:8501`).

## Structure du Projet

*   `app.py` : Point d'entree principal de l'application Streamlit. Gere la navigation et la configuration de la page.
*   `data/` : Contient les fichiers de donnees CSV utilises pour l'analyse.
    *   `flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv` : Donnees de flux domicile-travail.
    *   `20230823-communes-departement-region.csv` : Referentiel geographique.
*   `sections/` : Modules Python contenant le code specifique a chaque page/section du dashboard.
    *   `intro.py` : Page d'introduction.
    *   `overview.py` : Vue d'ensemble et KPIs.
    *   `deep_dives.py` : Cartographie et analyses approfondies.
    *   `comparisons.py` : Comparaisons et classements.
    *   `conclusions.py` : Conclusions et qualite des donnees.
*   `utils/` : Fonctions utilitaires pour le chargement des donnees, la preparation et la visualisation.
    *   `io.py` : Gestion des entrees/sorties (chargement des CSV).
    *   `prep.py` : Nettoyage et transformation des donnees.
    *   `viz.py` : Creation des graphiques (Plotly).
*   `requirements.txt` : Liste des dependances Python.

## Donnees

Les donnees utilisees proviennent de l'INSEE et concernent les deplacements domicile-travail (recensement de la population). Elles sont croisees avec un referentiel geographique des communes, departements et regions francaises.

## Auteur

Projet realise par Noe Lacaille.
