# 🚗 La Fracture de la Mobilité - Dashboard Streamlit

## La France est-elle vraiment prête à lâcher la voiture ?

Un dashboard interactif de data-storytelling explorant les **25 millions de trajets domicile-travail** des actifs français, révélant la fracture territoriale de la mobilité.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.33+-red.svg)
![License](https://img.shields.io/badge/license-Open%20Licence-green.svg)

---

## 🎯 Le Pitch

Alors que les **zones à faibles émissions** se multiplient et que la **transition écologique** s'impose, cette application révèle une vérité dérangeante : **la France reste massivement dépendante de la voiture** pour les trajets domicile-travail.

### L'Arc Narratif

1. **Le Constat** : La voiture représente 65-75% des trajets
2. **La Fracture** : Un fossé béant entre centres urbains et périphérie
3. **Les Signaux Faibles** : Où le vélo et le télétravail émergent-ils ?
4. **Les Insights** : Effet de seuil, zones blanches, potentiel de changement
5. **Les Implications** : Que faire pour une transition équitable ?

---

## 📊 Les Données

### Sources
- **Flux domicile-travail** : [Insee - Recensement 2022](https://www.insee.fr/)
  - 25+ millions d'actifs
  - 36 000+ communes
  - 6 modes de transport
  
- **Référentiel géographique** : [Data.gouv.fr](https://www.data.gouv.fr/)
  - Coordonnées GPS
  - Départements et régions

### Licence
**Licence Ouverte / Open Licence** (Etalab)
- ✅ Réutilisation libre
- ✅ Modification autorisée
- ✅ Usage commercial possible
- ⚠️ Attribution obligatoire

---

## 🚀 Installation & Démarrage

### Prérequis
- Python 3.9 ou supérieur
- pip

### Installation

```bash
# Cloner le repository
git clone <votre-repo>
cd Projet-Data-Viz-Streamlit

# Créer un environnement virtuel (recommandé)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

---

## 📁 Structure du Projet

```
Projet-Data-Viz-Streamlit/
│
├── app.py                          # 🎯 Application principale
│
├── sections/                       # 📄 Sections du dashboard
│   ├── intro.py                   # Introduction & contexte
│   ├── overview.py                # Vue d'ensemble & KPIs
│   ├── deep_dives.py              # Cartes interactives
│   ├── comparisons.py             # Analyses comparatives
│   └── conclusions.py             # Insights & conclusions
│
├── utils/                          # 🛠️ Utilitaires
│   ├── io.py                      # Chargement des données
│   ├── prep.py                    # Préparation & feature engineering
│   └── viz.py                     # Fonctions de visualisation
│
├── data/                           # 📊 Données
│   ├── flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv
│   └── 20230823-communes-departement-region.csv
│
├── requirements.txt                # 📦 Dépendances Python
└── README.md                       # 📖 Ce fichier
```

---

## 🎨 Fonctionnalités Principales

### 1. 🏠 Introduction
- **Contexte** : Crise climatique, fracture territoriale, post-Covid
- **Questions clés** : 5 questions guidant l'exploration
- **Limitations** : Transparence sur les biais des données

### 2. 📊 Vue d'Ensemble
- **KPIs dynamiques** : Actifs totaux, part de la voiture, mobilité durable
- **Visualisations** : Donut chart, Sunburst, Gauges de dépendance
- **Insights** : Comparaison grandes vs petites communes

### 3. 🗺️ Cartographie Interactive
- **Carte de dépendance automobile** : Choropleth avec gradient de couleur
- **Score de mobilité durable** : Carte des champions
- **Comparaison régionale** : Stacked bar charts par région
- **Top rankings** : Communes les plus/moins dépendantes

### 4. 🔬 Analyses Comparatives
- **Champions par mode** : Top 20 pour vélo, TC, marche, etc.
- **Corrélation taille/mobilité** : Scatter plot avec trendline
- **Potentiel de report modal** : Identification des zones prioritaires
- **Impact CO₂** : Estimation des économies potentielles

### 5. 🎓 Conclusions
- **5 insights majeurs** : Synthèse des découvertes clés
- **Implications** : Pistes d'action pour décideurs et entreprises
- **Qualité des données** : Validation et limitations détaillées
- **Prochaines étapes** : Pistes d'amélioration

---

## 🎯 Fonctionnalités Techniques

### Performance
- ✅ **Caching agressif** avec `@st.cache_data`
- ✅ **Pré-agrégations** pour les calculs lourds
- ✅ **Filtrage efficace** : Calculs uniquement sur données filtrées
- ✅ **Lazy loading** : Chargement à la demande

### UX/UI
- ✅ **Design moderne** : CSS personnalisé, gradients, animations
- ✅ **Responsive** : Adaptation mobile/desktop
- ✅ **Navigation intuitive** : Tabs, sidebar, boutons
- ✅ **Feedback visuel** : Spinners, métriques, progress bars
- ✅ **Accessibilité** : Contrastes élevés, labels clairs

### Visualisations
- ✅ **Plotly interactive** : Zoom, pan, hover tooltips
- ✅ **Cartes choroplèthes** : Mapbox avec géolocalisation
- ✅ **Charts variés** : Bar, scatter, donut, sunburst, gauge, treemap
- ✅ **Couleurs cohérentes** : Palette centralisée

### Data Quality
- ✅ **Validation automatique** : Détection valeurs manquantes, doublons
- ✅ **Nettoyage robuste** : Gestion des cas limites
- ✅ **Documentation** : Métadonnées et sources citées
- ✅ **Transparence** : Section dédiée aux limitations

---

## 💡 Insights Clés Découverts

### 1. 🚗 La Voiture est Reine Absolue
**65-75%** des trajets domicile-travail → La voiture écrase tous les autres modes

### 2. 🗺️ Fracture Territoriale Béante
**Grandes villes** : ~50% voiture | **Zones rurales** : >85% voiture

### 3. 🚴 Le Vélo : Succès Localisé
**<5%** au niveau national mais **15-20%** à Strasbourg, Bordeaux

### 4. 🏠 Télétravail : Privilège Urbain
**5-10%** de "Pas de transport" (mélange télétravail + agriculteurs)

### 5. 📊 Effet de Seuil
**< 1000 actifs** → Presque aucune alternative viable

---

## 🛠️ Technologies Utilisées

- **[Streamlit](https://streamlit.io/)** : Framework d'application web
- **[Pandas](https://pandas.pydata.org/)** : Manipulation de données
- **[Plotly](https://plotly.com/python/)** : Visualisations interactives
- **[NumPy](https://numpy.org/)** : Calculs numériques

---

## 📈 Améliorations Possibles

### Court terme
- [ ] Export PDF des insights
- [ ] Téléchargement des données filtrées (CSV)
- [ ] Mode sombre (dark mode)
- [ ] Comparaison temporelle (2015 vs 2022)

### Moyen terme
- [ ] Machine Learning : Clustering de communes similaires
- [ ] Simulation what-if (nouvelle ligne de bus → impact)
- [ ] API REST pour intégration externe
- [ ] Dashboard admin pour collectivités

### Long terme
- [ ] Données temps réel (API transport)
- [ ] Croisement avec données socio-économiques
- [ ] Module de recommandation IA
- [ ] Plateforme collaborative (partage d'analyses)

---

## 🤝 Contribution

Ce projet est **open source** et les contributions sont bienvenues !

### Comment contribuer ?
1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📝 Citation & Licence

### Pour citer ce travail
```
Dashboard "La Fracture de la Mobilité" (2024)
Données : Insee, Recensement de la Population 2022
Licence : Licence Ouverte / Open Licence (Etalab)
```

### Licence du Code
Ce code est distribué sous **Licence Ouverte / Open Licence**
- ✅ Modification autorisée
- ✅ Réutilisation libre
- ✅ Attribution obligatoire

---

## 📧 Contact & Support

Pour toute question, suggestion ou signalement de bug :
- 📧 Email : [votre-email]
- 🐛 Issues : [GitHub Issues](lien-vers-issues)
- 💬 Discussions : [GitHub Discussions](lien-vers-discussions)

---

## 🙏 Remerciements

- **Insee** : Pour la mise à disposition des données de recensement
- **Data.gouv.fr** : Pour les référentiels géographiques
- **Streamlit** : Pour le framework incroyable
- **Plotly** : Pour les visualisations magnifiques

---

## 📚 Ressources Complémentaires

### Datasets
- [Insee - Flux domicile-travail](https://www.insee.fr/fr/statistiques/fichier/7631989/flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.zip)
- [Data.gouv.fr - Référentiel communes](https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/)

### Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)

### Storytelling
- [Data Viz Society](https://www.datavisualizationsociety.org/)
- [FT Visual Vocabulary](https://ft-interactive.github.io/visual-vocabulary/)
- [Evergreen Data](https://stephanieevergreen.com/)

---

<div align="center">

**Fait avec ❤️ et beaucoup de ☕ pour la transition écologique**

[⬆ Retour en haut](#-la-fracture-de-la-mobilité---dashboard-streamlit)

</div>
