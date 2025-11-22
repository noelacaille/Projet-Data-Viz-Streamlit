# 🎬 Script de Démonstration - Dashboard Mobilité

## Durée : 3-4 minutes

---

## 🎯 Introduction (30 secondes)

**[Écran : Page d'accueil du dashboard]**

> "Bonjour ! Je vous présente mon dashboard Streamlit sur la mobilité en France. 
> Le titre : **'La Fracture de la Mobilité - La France est-elle vraiment prête à lâcher la voiture ?'**
> 
> Ce projet analyse 25 millions de trajets domicile-travail pour révéler une vérité dérangeante 
> sur notre dépendance automobile."

**[Montrer rapidement les 5 onglets]**

---

## 📊 Section 1 : Vue d'Ensemble (45 secondes)

**[Naviguer vers l'onglet "Vue d'Ensemble"]**

> "Premier constat : regardez ces chiffres clés."

**[Pointer les KPIs]**

> "La voiture représente **70% des trajets** ! C'est près de **15 fois plus** que le vélo. 
> Regardez ce donut chart : le rouge (voiture) écrase littéralement tout le reste."

**[Scroller vers les jauges de dépendance]**

> "Et voici la fracture : les grandes communes sont à 55% de dépendance automobile, 
> mais les petites communes ? **90%** ! C'est ça, la fracture territoriale de la mobilité."

---

## 🗺️ Section 2 : Cartographie (60 secondes)

**[Naviguer vers l'onglet "Cartographie"]**

> "Maintenant, visualisons cette fracture sur une carte."

**[Montrer la carte de dépendance automobile]**

> "Chaque point est une commune, colorée selon sa dépendance à la voiture. 
> Rouge foncé = plus de 80% de dépendance. 
> Regardez : les centres urbains (Paris, Lyon, Bordeaux) sont en jaune-vert, 
> mais toute la campagne est rouge sang."

**[Zoomer sur une région rurale]**

> "Ici, en zone rurale, certaines communes sont à **95%** de dépendance. 
> Ces gens n'ont **aucune alternative**. La voiture n'est pas un choix, c'est une obligation."

**[Scroller vers le tableau des top communes]**

> "Et voici le classement : les 15 communes les plus dépendantes. 
> Toutes rurales, toutes sans transports en commun."

---

## 🔬 Section 3 : Analyses Comparatives (45 secondes)

**[Naviguer vers l'onglet "Analyses Comparatives"]**

**[Sélectionner "Vélo" dans le menu déroulant]**

> "Parlons du vélo. Les médias en parlent beaucoup, mais regardez la réalité : 
> les champions du vélo sont Strasbourg, Grenoble, Bordeaux... 
> Des villes avec **infrastructure cyclable développée**."

**[Scroller vers le scatter plot]**

> "Ce graphique révèle l'effet de seuil : en dessous de 1000 actifs, 
> il n'y a quasiment **aucune mobilité durable**. 
> La corrélation est claire : **la densité permet la diversité des modes**."

**[Montrer le potentiel de report modal]**

> "Et voici les communes avec le plus grand potentiel de changement : 
> taille suffisante, forte dépendance automobile. 
> Si on investissait ici, on pourrait transférer **des dizaines de milliers d'actifs** 
> vers des modes plus durables."

---

## 🎓 Section 4 : Conclusions (30 secondes)

**[Naviguer vers l'onglet "Conclusions"]**

> "En conclusion, 5 insights majeurs :"

**[Pointer les 5 encarts colorés]**

1. > "La voiture est reine absolue - 70% des trajets"
2. > "La fracture territoriale est béante - zone blanche vs métropoles"
3. > "Le vélo : succès localisé, pas généralisé - <5% national"
4. > "Le télétravail : une solution partielle pour cadres urbains"
5. > "Effet de seuil : la densité est clé pour la mobilité durable"

**[Scroller vers les implications]**

> "Que faire ? Pour les décideurs publics : arrêter le dogmatisme. 
> La solution vélo+TC ne marche pas partout. 
> Il faut des **politiques différenciées** selon les territoires."

---

## 🎨 Section 5 : Fonctionnalités Techniques (30 secondes)

**[Retour à la vue d'ensemble, montrer la sidebar]**

> "Côté technique, j'ai mis l'accent sur l'UX. 
> Regardez cette sidebar avec filtres : vous pouvez sélectionner des régions, 
> des départements, filtrer par taille de commune."

**[Appliquer un filtre : Île-de-France]**

> "Par exemple, si je filtre sur l'Île-de-France... 
> Tous les graphiques se mettent à jour instantanément ! 
> C'est possible grâce au **caching Streamlit** et aux **pré-agrégations**."

**[Montrer un graphique interactif]**

> "Les graphiques sont interactifs : vous pouvez zoomer, survoler pour voir les détails, 
> cliquer sur les légendes... Tout est fait avec **Plotly**."

---

## 🎯 Conclusion (15 secondes)

**[Retour sur la page d'accueil]**

> "Voilà ! Un dashboard complet avec :
> - ✅ Storytelling clair (problème → analyse → insights → implications)
> - ✅ 20+ visualisations interactives
> - ✅ Cartes choroplèthes avec géolocalisation
> - ✅ UI/UX soignée avec CSS personnalisé
> - ✅ Performance optimisée avec caching
> - ✅ Documentation complète et transparence sur les limites
> 
> Merci d'avoir regardé cette démo !"

---

## 📝 Points à Souligner Oralement

### Forces du Projet
1. **Storytelling fort** : Arc narratif clair du début à la fin
2. **Visualisations pertinentes** : Chaque graphique répond à une question
3. **Transparence** : Section entière sur les limites des données
4. **Performance** : Chargement rapide malgré 125k lignes
5. **UI/UX professionnelle** : CSS custom, couleurs cohérentes, responsive

### Choix Techniques Justifiés
1. **Plotly** plutôt qu'Altair → Meilleur pour les cartes interactives
2. **Caching agressif** → Performance critique pour gros datasets
3. **Pré-agrégations** → Éviter de recalculer à chaque interaction
4. **Structure modulaire** → Sections séparées = code maintenable

### Insights Data Science
1. **Effet de seuil** : Découverte de la barrière des ~1000 actifs
2. **Fracture territoriale** : Quantifiée précisément (55% vs 90%)
3. **Mythe du vélo** : Démystifié avec données réelles (<5% national)
4. **Potentiel de report modal** : Méthode pour prioriser investissements

---

## 🎥 Conseils pour la Vidéo

### Préparation
- [ ] Tester tous les filtres avant l'enregistrement
- [ ] Nettoyer l'historique du navigateur
- [ ] Fermer les onglets inutiles
- [ ] Préparer quelques phrases de transition

### Tournage
- [ ] Parler clairement et pas trop vite
- [ ] Montrer, ne pas juste décrire
- [ ] Utiliser le curseur pour guider l'œil du spectateur
- [ ] Varier les rythmes : rapide pour l'intro, lent pour les insights

### Montage (optionnel)
- [ ] Ajouter des flèches/cercles pour highlights
- [ ] Zoom sur les KPIs importants
- [ ] Transition smooth entre sections
- [ ] Musique de fond légère (optionnel)

---

**Bonne chance pour votre démonstration ! 🎬✨**
