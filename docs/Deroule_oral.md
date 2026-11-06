# Oral de 18 minutes avec le dashboard en ligne

Application : https://accidents-aeriens-esiee-berqbs6auc7f4txjtyjxip.streamlit.app/

| Diapositive | Durée | Objectif |
|---|---:|---|
| 1. Sujet et mission | 0:30 | Client simulé et question |
| 2. Données et périmètre | 1:00 | Source, ligne, colonnes, année partielle |
| 3. Diagnostic qualité | 1:30 | Anomalies et intersections |
| 4. Décisions de nettoyage | 1:30 | Justifier les traitements |
| 5. Évolution temporelle | 1:30 | Courbes sans confusion entre effectif et risque |
| 6. Gravité | 1:00 | Distribution, moyenne et médiane |
| 7. Survie pondérée | 1:00 | Numérateur et dénominateur |
| 8. Géographie | 0:45 | Couverture et pays non résolus |
| 9. Constructeurs | 0:45 | Effectifs et limites |
| 10. Associations | 1:00 | Corrélations et absence de causalité démontrée |
| 11. Deux périodes | 1:00 | Comparer des indicateurs différents |
| 12. Effet du nettoyage | 1:00 | Changement de population |
| 13. Sensibilité | 1:00 | Hypothèse relative de gravité |
| 14. Monte-Carlo | 1:30 | Tirages, graine, quantiles et limites |
| 15. Démonstration en ligne | 2:00 | Montrer les quatre scénarios |
| 16. Conclusion | 1:00 | Résultats, limites et suite |

Total : **18 minutes**, hors questions. Répartir les diapositives entre les membres
et faire une répétition chronométrée.

## Démonstration en deux minutes

Avant de commencer : période 1908–2025, aucun pays ni constructeur sélectionné.
Ouvrir la page Scénarios et préparer le menu « Scénario à démontrer ».

| Temps | Scénario | Action et phrase clé |
|---|---|---|
| 0:00–0:30 | Comparer deux périodes | « Les deux fenêtres durent vingt ans. Les indicateurs ne décrivent pas la même chose. » |
| 0:30–1:00 | Traitement des données manquantes | « Les seuls pays résolus donnent une autre population et 30,15 % de survie pondérée. » |
| 1:00–1:30 | Hypothèse sur la gravité | Passer de 10 à 20 %. « La baisse relative est imposée, aucun effet réel n'est estimé. » |
| 1:30–2:00 | Monte-Carlo : collections fictives | Passer de 50 à 100 lignes puis revenir à 50. « Ce sont des collections fictives, pas une fréquence d'accidents par vol. » |

Les explications longues sont faites sur les diapositives précédentes.

## Répétition des filtres

Choisir France dans Vue d'ensemble : 109 lignes, 2 019 décès déclarés, médiane 7
et survie affichée à 21,8 %. Retirer France pour retrouver le périmètre global.

## Questions à préparer

- Pourquoi ne pas imputer les occupations nulles ? Le nombre réel ne peut pas être reconstitué.
- Pourquoi conserver les grandes valeurs ? Elles peuvent correspondre à des événements réels.
- Pourquoi ne pas classer les constructeurs par danger ? Le nombre de vols manque.
- Pourquoi le taux change après un filtre de qualité ? La population change.
- Q05–Q95 est-il un intervalle de confiance ? Non, il décrit les répétitions simulées.
- La simulation prédit-elle des accidents futurs ? Non.
- Quelles méthodes viennent du cours ? Voir Correspondance_cours.md, avec les adaptations signalées.

Vérifier le lien avant l'oral et garder les figures exportées comme secours.
Pendant le partage d'écran, afficher les diapositives ou le dashboard et garder
les notes dans une fenêtre non partagée.
