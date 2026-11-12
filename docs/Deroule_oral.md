# Déroulé de la présentation

## Problématique

Comment le nombre d’accidents et leur bilan humain changent-ils selon le constructeur, le modèle d’avion, l’opérateur et la période étudiée ?

Le support comporte 21 diapositives avec notes. Durée prévue : environ 19 min 30, dont trois minutes d’introduction et deux minutes de démonstration. Répartir les diapositives entre les membres et répéter avec un chronomètre.

| Diapositive | Sujet | Durée prévue |
|---|---|---|
| 1 | Accidents aériens et présentation du groupe | 0:25 |
| 2 | Pourquoi avoir choisi ce sujet ? | 1:15 |
| 3 | La question qui guide notre travail | 1:20 |
| 4 | Aviation militaire et aviation commerciale | 0:45 |
| 5 | Une ligne du CSV devient plusieurs colonnes | 0:55 |
| 6 | Le nettoyage change les libellés, pas les faits | 1:05 |
| 7 | La survie demande des données cohérentes | 1:00 |
| 8 | 11 occupants, 8 décès : comment lire la survie ? | 0:55 |
| 9 | Le choix à gauche pilote les résultats à droite | 1:00 |
| 10 | Les indicateurs répondent à des questions différentes | 0:55 |
| 11 | Les effectifs du fichier varient selon l’époque | 0:45 |
| 12 | La barre entière représente 155 827 occupants | 0:55 |
| 13 | Les faibles bilans sont les plus nombreux | 0:45 |
| 14 | Notre cas d’étude : le Boeing 737 | 0:40 |
| 15 | Le nombre d’enregistrements baisse | 0:55 |
| 16 | Le bilan humain augmente pourtant | 1:15 |
| 17 | Le parcours que nous allons tester | 2:00 |
| 18 | Les compléments au cours ont un rôle précis | 0:40 |
| 19 | Nos chiffres décrivent ce fichier | 0:35 |
| 20 | Streamlit permet de vérifier la comparaison | 0:45 |
| 21 | La gravité ne se lit pas dans un seul chiffre | 0:40 |

## Démonstration, diapositive 17

Avant le passage, ouvrir le dashboard et revenir aux valeurs par défaut.

- Retrouver 5 017 lignes sur Tous / Tous / Tous / 1908–2023.
- Choisir Boeing puis Boeing 737, avec Tous pour l’opérateur : 102 lignes.
- Comparer 1980–1999 et 2000–2019 : 50 puis 41 lignes, 2 496 puis 2 680 décès à bord déclarés.
- Consulter le tableau et le téléchargement CSV, puis montrer la sélection vide sur 1908–1909.
- Revenir à 1908–2023.

Pour montrer le filtre opérateur après la démonstration principale, revenir à Tous pour le constructeur et le modèle puis sélectionner Air France (mention explicite). Le résultat porte sur sept mentions et ne constitue pas l’historique complet de la compagnie. Voir Guide_client.md.

## Préparation aux questions

Expliquer DataFrame, sep=",", masque, groupby, sum et moyenne sans lire le code.
Savoir refaire les deux formules de taux avec un exemple numérique.
Expliquer les 22 lignes exclues de la survie et conservées dans les autres calculs.
Pourquoi la baisse des effectifs ne prouve-t-elle pas une amélioration de sécurité ?
Pourquoi la recherche des compagnies reste-t-elle incomplète ?

Afficher les slides ou le dashboard pendant le partage d'écran. Garder les notes
dans une fenêtre non partagée. Garder le rapport comme secours de démonstration.
