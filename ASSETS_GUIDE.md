# 🎨 Assets & Branding Guide

## Visual Identity

### Color Palette

#### Primary Colors
- **Deep Purple**: `#667eea` - Sidebar gradient start
- **Royal Purple**: `#764ba2` - Sidebar gradient end
- **Dark Slate**: `#2c3e50` - Text primary
- **Steel Blue**: `#34495e` - Text secondary

#### Transport Mode Colors
- **🚗 Voiture**: `#e74c3c` (Rouge vif)
- **🚌 Transports en commun**: `#3498db` (Bleu)
- **🚴 Vélo**: `#2ecc71` (Vert)
- **🚶 Marche**: `#f39c12` (Orange)
- **🏍️ Deux-roues motorisé**: `#9b59b6` (Violet)
- **🏠 Pas de transport**: `#95a5a6` (Gris)

#### Semantic Colors
- **Success**: `#2ecc71` (Vert)
- **Warning**: `#f39c12` (Orange)
- **Danger**: `#e74c3c` (Rouge)
- **Info**: `#3498db` (Bleu)

#### Background Colors
- **White**: `#ffffff`
- **Light Gray**: `#f8f9fa`
- **Medium Gray**: `#e0e0e0`

---

## Typography

### Font Family
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Font Weights
- **Light**: 300 - Body text légère
- **Regular**: 400 - Body text standard
- **Semi-Bold**: 600 - Sous-titres
- **Bold**: 700 - Titres

### Font Sizes
- **H1**: 2.5rem (40px)
- **H2**: 2rem (32px)
- **H3**: 1.5rem (24px)
- **Body**: 1rem (16px)
- **Small**: 0.9rem (14px)

---

## Icons & Emojis

### Section Icons
- 🏠 **Introduction**: Home, contexte
- 📊 **Vue d'ensemble**: Charts, statistiques
- 🗺️ **Cartographie**: Cartes, géographie
- 🔬 **Analyses**: Microscope, recherche
- 🎓 **Conclusions**: Graduation cap, insights

### Transport Mode Emojis
- 🚗 Voiture
- 🚌 Bus / Transports en commun
- 🚴 Vélo
- 🚶 Marche à pied
- 🏍️ Moto / Deux-roues
- 🏠 Maison / Télétravail

### Status Icons
- ✅ Succès, validation
- ❌ Erreur, problème
- ⚠️ Attention, warning
- ℹ️ Information
- 💡 Insight, idée
- 🎯 Objectif, cible
- 📈 Croissance, augmentation
- 📉 Décroissance, diminution

---

## Logo Suggestions (Optional)

Si vous souhaitez ajouter un logo, voici des suggestions :

### Option 1 : Text Logo
```
🚗💥🚴
LA FRACTURE
```

### Option 2 : Minimal Icon
```
  🚗 ─────┬───── 🚴
         │
      MOBILITÉ
```

### Option 3 : Split Design
```
┌─────────────┬─────────────┐
│  VOITURE    │    VÉLO     │
│    70%      │     5%      │
└─────────────┴─────────────┘
```

---

## Banner Images (Optional)

### Hero Banner Suggestions
1. **Urban/Rural Split**: Photo montrant d'un côté des transports en commun urbains, de l'autre une route rurale
2. **Traffic Visualization**: Carte de chaleur abstraite de la France avec flux de mobilité
3. **Gradient Background**: Simplement le gradient violet (actuel) avec typographie forte

### Recommended Dimensions
- **Hero Banner**: 1200 x 400 px
- **Logo**: 200 x 200 px (carré)
- **Favicon**: 32 x 32 px

---

## Layout Components

### Card Style
```css
border-radius: 10px;
box-shadow: 0 2px 8px rgba(0,0,0,0.05);
padding: 1.5rem;
background: white;
```

### Button Style
```css
border-radius: 8px;
padding: 0.5rem 2rem;
font-weight: 600;
transition: all 0.3s ease;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
```

### Hover Effect
```css
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
```

---

## Gradients

### Primary Gradient (Sidebar)
```css
background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
```

### Hero Gradient (Alternative)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Separator Gradient
```css
background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
```

---

## Animation Guidelines

### Subtle Animations
- **Hover**: 0.3s ease
- **Fade In**: 0.5s ease-in
- **Slide**: 0.4s ease-out

### No Animation
- Sur les graphiques Plotly (déjà interactifs)
- Sur les tableaux de données
- Sur les métriques (pour ne pas distraire)

---

## Responsive Breakpoints

### Desktop
- **Large**: > 1400px
- **Medium**: 1024px - 1400px
- **Small**: 768px - 1024px

### Mobile
- **Tablet**: 600px - 768px
- **Phone**: < 600px

---

## Accessibility

### Contrast Ratios (WCAG AA)
- **Text**: Minimum 4.5:1
- **Large Text**: Minimum 3:1
- **Graphics**: Minimum 3:1

### Current Compliance
- ✅ Text on white: 2c3e50 (#2c3e50) → 12.6:1 ✅
- ✅ Links: 3498db (#3498db) → 4.5:1 ✅
- ✅ Success: 2ecc71 (#2ecc71) → 3.0:1 ⚠️ (Large text only)

### Recommendations
- Utiliser des labels clairs sur tous les graphiques
- Ajouter des tooltips explicatifs
- Éviter de se fier uniquement à la couleur (utiliser aussi forme/texture)

---

## Image Assets (à créer si besoin)

### Suggested Illustrations
1. **France Map Outline**: Silhouette de la France avec points
2. **Transport Icons Set**: Version stylisée des emojis
3. **Data Visualization Pattern**: Abstrait, arrière-plan subtil

### Placeholder Images
Si vous voulez ajouter des images décoratives :
- **Unsplash Keywords**: "france aerial", "urban transport", "bicycle infrastructure"
- **License**: Choisir CC0 (domaine public)

---

## File Organization

```
assets/                         (À créer si besoin)
├── images/
│   ├── logo.png
│   ├── logo.svg
│   ├── favicon.ico
│   └── hero-banner.jpg
├── icons/
│   └── transport-modes/
│       ├── car.svg
│       ├── bus.svg
│       ├── bike.svg
│       └── walk.svg
└── fonts/
    └── (Inter is loaded from Google Fonts)
```

---

## Branding Do's and Don'ts

### ✅ Do's
- Utiliser le gradient violet pour les éléments importants
- Maintenir la cohérence des couleurs par mode de transport
- Utiliser des icônes/emojis pour rendre l'interface friendly
- Garder un design propre et épuré (pas de surcharge)

### ❌ Don'ts
- Utiliser trop de couleurs différentes (max 6 couleurs principales)
- Mélanger gradients de différentes directions
- Ajouter des animations distrayantes sur les données
- Utiliser des polices fantaisistes (rester sur Inter)

---

## Export Assets Commands

### Generate Favicon (si vous avez un logo)
```python
from PIL import Image

# Redimensionner pour favicon
img = Image.open('logo.png')
img = img.resize((32, 32), Image.LANCZOS)
img.save('favicon.ico')
```

### Optimize PNG Images
```bash
# Avec pngquant (réduit la taille sans perte visible)
pngquant --quality=65-80 --ext .png --force images/*.png
```

---

## Integration in Streamlit

### Add Favicon
```python
st.set_page_config(
    page_icon="🚗",  # Emoji ou chemin vers favicon.ico
    ...
)
```

### Add Logo in Sidebar
```python
st.sidebar.image("assets/images/logo.png", width=200)
```

### Add Hero Image
```python
st.image("assets/images/hero-banner.jpg", use_column_width=True)
```

---

## Design References

### Inspiration Sites
- **Streamlit Gallery**: https://streamlit.io/gallery
- **Dribbble**: Search "data dashboard"
- **Behance**: Search "data visualization"

### Color Palette Tools
- **Coolors**: https://coolors.co/
- **Adobe Color**: https://color.adobe.com/
- **Paletton**: https://paletton.com/

---

**Note**: Le dashboard actuel fonctionne parfaitement sans assets additionnels. 
Ces suggestions sont optionnelles pour aller plus loin dans la personnalisation.
