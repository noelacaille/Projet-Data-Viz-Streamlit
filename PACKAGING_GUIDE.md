# 📦 Instructions de Packaging pour la Remise

## Format du Fichier ZIP

**Nom du fichier** : `StreamlitApp25_[NUMERO_ETUDIANT]_[NOM]_[FILIERE].zip`

**Exemple** : `StreamlitApp25_20000_LACAILLE_BIA.zip`

---

## 📋 Checklist Avant ZIP

### 1. Vérifier les Données
```bash
python check_data.py
```
✅ Tous les fichiers CSV doivent être présents dans `data/`

### 2. Tester l'Application
```bash
streamlit run app.py
```
✅ L'application doit démarrer sans erreur
✅ Tous les onglets doivent s'afficher
✅ Les filtres doivent fonctionner
✅ Les graphiques doivent se charger

### 3. Vérifier les Fichiers Requis

#### Fichiers de Code (Obligatoires)
- [ ] `app.py`
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] `utils/io.py`
- [ ] `utils/prep.py`
- [ ] `utils/viz.py`
- [ ] `sections/intro.py`
- [ ] `sections/overview.py`
- [ ] `sections/deep_dives.py`
- [ ] `sections/comparisons.py`
- [ ] `sections/conclusions.py`

#### Fichiers de Configuration
- [ ] `.streamlit/config.toml`
- [ ] `.gitignore`

#### Fichiers de Documentation
- [ ] `README.md` (principal)
- [ ] `QUICKSTART.md` (optionnel mais recommandé)
- [ ] `DEMO_SCRIPT.md` (pour la vidéo)
- [ ] `PROJECT_SUMMARY.md` (résumé du projet)

#### Données
- [ ] `data/flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv`
- [ ] `data/20230823-communes-departement-region.csv`

#### Fichiers à NE PAS Inclure
- [ ] ❌ `__pycache__/` (dossiers de cache Python)
- [ ] ❌ `venv/` ou `env/` (environnement virtuel)
- [ ] ❌ `.vscode/` ou `.idea/` (config IDE)
- [ ] ❌ Fichiers temporaires (`.pyc`, `.log`, etc.)

---

## 🗂️ Structure Finale à Vérifier

```
StreamlitApp25_20000_LACAILLE_BIA/
│
├── app.py                          ✅ Application principale
├── requirements.txt                ✅ Dépendances
├── README.md                       ✅ Documentation
├── QUICKSTART.md                   ✅ Guide rapide
├── DEMO_SCRIPT.md                  ✅ Script vidéo
├── PROJECT_SUMMARY.md              ✅ Résumé projet
├── check_data.py                   ✅ Script validation
│
├── .streamlit/
│   └── config.toml                 ✅ Config Streamlit
│
├── .gitignore                      ✅ Exclusions Git
│
├── utils/
│   ├── io.py                       ✅ Chargement données
│   ├── prep.py                     ✅ Préparation
│   └── viz.py                      ✅ Visualisations
│
├── sections/
│   ├── intro.py                    ✅ Introduction
│   ├── overview.py                 ✅ Vue d'ensemble
│   ├── deep_dives.py               ✅ Cartes
│   ├── comparisons.py              ✅ Analyses
│   └── conclusions.py              ✅ Conclusions
│
└── data/
    ├── flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv  ✅
    └── 20230823-communes-departement-region.csv                                        ✅
```

---

## 💻 Commandes pour Créer le ZIP

### Option 1 : Windows (PowerShell)
```powershell
# Se placer dans le dossier parent
cd c:\Users\noela\NoeLacaille

# Créer le ZIP
Compress-Archive -Path "Projet-Data-Viz-Streamlit\*" -DestinationPath "StreamlitApp25_20000_LACAILLE_BIA.zip" -Force
```

### Option 2 : Windows (Explorateur de Fichiers)
1. Sélectionnez le dossier `Projet-Data-Viz-Streamlit`
2. Clic droit → "Envoyer vers" → "Dossier compressé"
3. Renommez le fichier selon le format requis

### Option 3 : Ligne de Commande (avec 7-Zip)
```bash
7z a -tzip StreamlitApp25_20000_LACAILLE_BIA.zip Projet-Data-Viz-Streamlit\* -xr!__pycache__ -xr!venv -xr!.vscode
```

---

## 🎥 Préparation de la Vidéo de Démo

### Checklist Avant Enregistrement

#### Technique
- [ ] Fermer tous les onglets inutiles du navigateur
- [ ] Nettoyer le bureau (pas de fichiers persos visibles)
- [ ] Tester le micro et la qualité audio
- [ ] Régler la résolution d'écran (1920x1080 recommandé)
- [ ] Désactiver les notifications Windows

#### Contenu
- [ ] Relire le script (DEMO_SCRIPT.md)
- [ ] Préparer 2-3 phrases de transition
- [ ] Identifier 3-4 insights clés à mettre en avant
- [ ] Tester tous les filtres et interactions
- [ ] Préparer une "chute" percutante

#### Durée
- [ ] ⏱️ **Objectif : 2-4 minutes** (ni trop court, ni trop long)
- [ ] ⏱️ Chronomètre chaque section pendant les répétitions
- [ ] ⏱️ Prévoir 30s de marge pour l'édition

### Structure Vidéo Recommandée (3 min 30s)

| Section | Durée | Contenu Clé |
|---------|-------|-------------|
| Intro | 30s | Titre, contexte, pitch |
| Vue d'ensemble | 45s | KPIs, fracture révélée |
| Carte | 60s | Choroplèthe, zoom, insights |
| Analyses | 45s | Champions, corrélations |
| Conclusion | 30s | 5 insights + implications |

---

## ✅ Checklist Finale Avant Soumission

### Technique
- [ ] Le ZIP fait moins de 100 MB (limite usuelle)
- [ ] Le ZIP contient TOUS les fichiers nécessaires
- [ ] Le ZIP ne contient PAS de dossiers cachés (__pycache__, .vscode)
- [ ] Le nom du ZIP suit le format exact

### Fonctionnel
- [ ] L'application démarre avec `streamlit run app.py`
- [ ] Tous les onglets s'affichent sans erreur
- [ ] Les cartes se chargent correctement
- [ ] Les filtres fonctionnent
- [ ] Les graphiques sont interactifs

### Documentation
- [ ] Le README.md est complet (installation, usage, sources)
- [ ] Les sources des données sont citées
- [ ] Les limitations sont documentées
- [ ] Le code est commenté aux endroits clés

### Vidéo
- [ ] Durée : 2-4 minutes ✅
- [ ] Qualité audio claire ✅
- [ ] Démonstration complète (5 sections) ✅
- [ ] Insights clés énoncés ✅
- [ ] Format : MP4 ou lien YouTube/Vimeo ✅

---

## 📤 Plateforme de Remise

### Si Soumission par Email
- **Sujet** : `[Streamlit Dashboard] NOM Prénom - Filière`
- **Corps** : 
  ```
  Bonjour,
  
  Veuillez trouver ci-joint mon projet Streamlit Dashboard :
  - Fichier ZIP : StreamlitApp25_XXXXX_NOM_BIA.zip
  - Vidéo de démo : [lien YouTube/fichier joint]
  
  Dataset utilisé : Flux domicile-travail INSEE 2022
  Titre : "La Fracture de la Mobilité"
  
  Cordialement,
  [Votre Nom]
  ```

### Si Soumission par Plateforme (Moodle, etc.)
- [ ] Téléverser le ZIP
- [ ] Téléverser la vidéo (ou coller le lien)
- [ ] Vérifier que les fichiers sont bien uploadés
- [ ] Confirmer la soumission

---

## 🆘 Troubleshooting Dernière Minute

### "Le ZIP est trop gros"
Les fichiers CSV sont volumineux. Options :
1. Vérifier qu'il n'y a pas de doublons de données
2. Compresser avec un niveau de compression max
3. Si vraiment trop gros, mettre les CSV dans un drive et inclure le lien dans README

### "L'application ne démarre pas"
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt

# Vérifier les données
python check_data.py
```

### "Les cartes ne s'affichent pas"
Vérifier que le fichier géographique contient bien les colonnes `latitude` et `longitude`

### "Erreur de cache"
```bash
# Lancer avec cache désactivé
streamlit run app.py --server.headless true
```

---

## 🎯 Rappel des Critères d'Évaluation

| Critère | Poids | Ce que le Prof Attend |
|---------|-------|----------------------|
| **Narrative & Problem Framing** | 25 pts | Histoire claire, audience définie, questions précises |
| **Data Work** | 25 pts | Nettoyage, feature engineering, validation |
| **Visualization & UX** | 25 pts | Graphiques pertinents, interactions, design soigné |
| **Engineering Quality** | 15 pts | Code propre, performant, reproductible |
| **Communication** | 10 pts | Documentation, vidéo claire, transparence |

### Points Bonus Potentiels
- ✨ UI exceptionnellement belle
- ✨ Insights non-évidents découverts
- ✨ Performance optimale sur gros dataset
- ✨ Documentation exhaustive

---

## ✅ Dernière Vérification (Le Jour J)

**1 heure avant soumission** :

```bash
# 1. Cloner le projet dans un dossier temporaire
xcopy Projet-Data-Viz-Streamlit\ Test-Final\ /E /I

# 2. Se placer dedans
cd Test-Final

# 3. Créer un nouvel environnement
python -m venv venv
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Vérifier les données
python check_data.py

# 6. Lancer l'app
streamlit run app.py

# 7. Tester TOUS les onglets et filtres

# 8. Si tout fonctionne → Créer le ZIP final
```

---

**Bonne chance pour votre remise ! 🍀✨**

*"Un grand pouvoir implique de grandes données bien visualisées"* 📊
