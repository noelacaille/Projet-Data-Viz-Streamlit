# 🚀 Guide de Démarrage Rapide

## Installation en 3 minutes

### Étape 1 : Prérequis
```bash
# Vérifier la version Python (doit être >= 3.9)
python --version
```

### Étape 2 : Installation
```bash
# Se placer dans le dossier du projet
cd Projet-Data-Viz-Streamlit

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 3 : Lancement
```bash
# Démarrer l'application
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## 🎮 Utilisation

### Navigation
- **Onglets en haut** : Naviguez entre les 5 sections principales
- **Barre latérale** : Utilisez les filtres pour explorer les données
- **Graphiques interactifs** : Survolez, zoomez, cliquez

### Filtres Disponibles
1. **Région(s)** : Sélectionnez une ou plusieurs régions
2. **Département(s)** : Affinez par département
3. **Taille des communes** : Filtrez par catégorie de taille
4. **Minimum d'actifs** : Excluez les petites communes

### Sections du Dashboard
1. **🏠 Introduction** : Contexte et questions clés
2. **📊 Vue d'Ensemble** : KPIs et répartition globale
3. **🗺️ Cartographie** : Cartes interactives de la France
4. **🔬 Analyses Comparatives** : Rankings et corrélations
5. **🎓 Conclusions** : Insights et implications

---

## 🐛 Résolution de Problèmes

### Erreur : "ModuleNotFoundError"
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur : "FileNotFoundError" pour les CSV
Vérifiez que les fichiers sont bien dans le dossier `data/` :
- `flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv`
- `20230823-communes-departement-region.csv`

### L'application est lente
- Réduisez les filtres (sélectionnez moins de régions)
- Utilisez le filtre "Minimum d'actifs" pour exclure les petites communes
- Le premier chargement est plus lent (cache en construction)

### Port déjà utilisé
```bash
# Utiliser un port différent
streamlit run app.py --server.port 8502
```

---

## 💡 Astuces

### Performance
- Le cache Streamlit accélère les chargements suivants
- Les filtres se combinent (AND logique)
- Cliquez sur "Clear cache" dans le menu (⋮) si besoin

### Visualisations
- **Cartes** : Cliquez sur les points pour voir les détails
- **Graphiques** : Double-cliquez pour réinitialiser le zoom
- **Tableaux** : Cliquez sur les colonnes pour trier

### Export
- **Screenshots** : Utilisez l'outil de capture de votre navigateur
- **Données** : Les tableaux peuvent être copiés-collés dans Excel

---

## 📧 Besoin d'Aide ?

- 📖 Consultez le [README.md](README.md) complet
- 🐛 Signalez un bug via GitHub Issues
- 💬 Posez vos questions sur GitHub Discussions

---

**Bon voyage dans les données de la mobilité française ! 🚗🚴🚌**
