# SkyStats : accidents aériens, bilan historique

Projet ESIEE Paris — Bryan EL BOUSTANI, Louis BUGADA, Ryad MASTOUR et Liam BAH-PAYEN.
Documentation mise à jour le 15 novembre 2026 pour le programme `app.py`.

## Problématique

Comment le nombre d’accidents et leur bilan humain changent-ils selon le constructeur, le modèle d’avion, l’opérateur et la période étudiée ?

[**Ouvrir le dashboard en ligne**](https://accidents-aeriens-esiee-berqbs6auc7f4txjtyjxip.streamlit.app/)

## Utiliser le dashboard

Dans la barre latérale, choisir un constructeur, un type d’appareil, un opérateur et une période. Les menus dépendent des choix précédents. La période initiale est **2014–2023**.

L’application comprend :
- une courbe des décès à bord par année sur **1908–2023**, indépendante des filtres ;
- quatre indicateurs calculés sur la sélection ;
- trois graphiques filtrés : un diagramme circulaire survivants/décès, les dix années comptant le plus d’enregistrements et les cinq modèles les plus représentés ;
- un aperçu des **50 premières lignes** et un bouton pour télécharger **toute la sélection** au format CSV.

Une sélection vide déclenche un message. Les graphiques qui ne peuvent pas être calculés, ou le classement limité au seul modèle choisi, sont remplacés par une explication.

## Fichiers utilisés par cette version

| Fichier | Rôle |
|---|---|
| `app.py` | Programme Streamlit : chargement, nettoyage, indicateurs et affichage |
| `aircrashesFullData.csv` | Données brutes, à la racine du dépôt, à côté de `app.py` |
| `requirements.txt` | Bibliothèques Python nécessaires |
| `.streamlit/config.toml` | Thème sombre par défaut |

Le programme contient trois fonctions : `charger_donnees`, `calculer_indicateurs` et `afficher_application`.

## CSV et période retenue

La lecture utilisée est :

```python
pd.read_csv("aircrashesFullData.csv", sep=",")
```

La virgule sépare les colonnes ; les champs entre guillemets sont respectés. Le fichier fourni comporte **5 052 lignes et 12 colonnes**, avec des années jusqu’en 2026. Le projet conserve **1908–2023**, soit **5 017 lignes** après exclusion des 35 lignes hors période. Le fichier brut n’est pas modifié.

## Nettoyage

- Conversion de `Year`, `Aboard` et `Fatalities (air)` en nombres. Une conversion impossible devient une valeur manquante.
- Les valeurs négatives de `Aboard` et `Fatalities (air)` deviennent manquantes.
- Suppression des doublons exacts : aucun n’a été trouvé dans le fichier fourni.
- Création des colonnes `Constructeur`, `Modele` et `Operateur`, avec uniformisation des espaces.
- Les libellés absents, vides ou commençant par `?` sont classés « Non renseigné », sans supprimer les lignes.
- Regroupement de neuf familles de constructeurs et de dix familles de modèles Boeing selon des préfixes explicites.
- Regroupement des mentions contenant « air france » sous « Air France (mention explicite) ».

Ce dernier regroupement concerne sept lignes sur 1908–2023 : il ne reconstitue pas tout l’historique de la compagnie. Les autres noms d’opérateurs ne sont pas automatiquement rapprochés. Les libellés d’origine restent consultables dans le tableau et l’export.

## Définition des indicateurs

| Indicateur | Calcul |
|---|---|
| Enregistrements | Nombre de lignes sélectionnées |
| Décès à bord déclarés | Somme des bilans connus de `Fatalities (air)`, y compris les lignes dont le nombre d’occupants est incohérent |
| Survie globale | 100 × total des survivants / total des occupants, sur les mêmes lignes avec `Aboard > 0` et `0 ≤ Fatalities (air) ≤ Aboard` |
| Sans décès à bord | 100 × nombre de lignes à zéro décès / nombre de lignes au bilan à bord connu |

Les survivants sont calculés par `Aboard - Fatalities (air)`. La survie globale est un taux pondéré par le nombre d’occupants, et non une moyenne des taux de chaque accident. Un indicateur sans données suffisantes affiche « Non calculable ».

Pour la courbe annuelle, `sum(min_count=1)` évite de transformer une année dont tous les bilans seraient manquants en zéro décès.

### Pourquoi deux totaux de décès ?

Sur 1908–2023, les 5 017 lignes déclarent **111 686 décès à bord**. Le calcul de survie utilise **4 995 lignes cohérentes**, soit **111 613 décès et 44 214 survivants** pour **155 827 occupants**.

Les 22 lignes exclues du taux ont zéro occupant. Parmi elles, neuf déclarent des décès, pour un total de 73. Ces bilans restent dans le total déclaré mais ne permettent pas un calcul de survie cohérent.

Le diagramme circulaire utilise les mêmes lignes valides que le taux de survie. Les décès au sol ne sont inclus dans aucun de ces indicateurs.

## Scénarios de démonstration

| Sélection | Enregistrements | Décès à bord déclarés | Survie globale | Sans décès à bord |
|---|---:|---:|---:|---:|
| Tous, 1908–2023 | 5 017 | 111 686 | 28,4 % | 1,7 % |
| Tous, 2014–2023 — sélection initiale | 136 | 4 625 | 24,8 % | 1,5 % |
| Boeing / Boeing 737 / tous opérateurs, 1980–1999 | 50 | 2 496 | 39,8 % | 2,0 % |
| Boeing / Boeing 737 / tous opérateurs, 2000–2019 | 41 | 2 680 | 36,1 % | 12,2 % |

Comparer les deux périodes Boeing 737 montre que moins d’enregistrements peut coexister avec davantage de décès. Choisir ensuite Boeing 737 sur 1908–1909 permet de montrer le message de sélection vide.

Ces scénarios explorent des données historiques ; ils ne simulent pas un prochain vol. La courbe annuelle globale reste inchangée pendant la démonstration.

## Limites de l’analyse

- **Nombre de vols absent :** aucun risque par vol ni classement de sécurité ne peut être déduit des effectifs.
- **Collecte historique incomplète et hétérogène :** le fichier ne représente pas nécessairement tous les accidents.
- **Standardisation partielle :** certains noms restent incomplets ou dispersés sous plusieurs libellés.
- **Blessures non renseignées :** impossible de distinguer les survivants blessés des personnes indemnes.
- **Causes non renseignées :** le fichier ne contient pas de colonne `Summary` permettant l’analyse textuelle envisagée.
- **Décès au sol :** `Ground` reste visible dans le tableau et l’export, mais n’est pas additionné, car un même bilan peut être répété pour plusieurs appareils.
- **Opérations civiles et militaires mélangées :** un opérateur militaire ne prouve pas une mission de guerre, et un accident commercial ne prouve pas une panne technique.
- **Petites sélections :** les pourcentages deviennent fragiles lorsque peu de lignes sont retenues.

## Exécuter le programme

Le public peut utiliser directement le lien Streamlit. Pour reproduire le programme sur un ordinateur, télécharger le dépôt avec **Code → Download ZIP**, extraire les fichiers, puis exécuter depuis le dossier contenant `app.py` :

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Sur Streamlit Community Cloud, le fichier principal à sélectionner est **`app.py`**. Le CSV doit rester à la racine du dépôt.

## Livrables

- Code : `app.py`, CSV, dépendances et configuration de ce dépôt.
- Rapport harmonisé : **Rapport_SkyStats_Final.docx**.
- Présentation harmonisée : **Presentation_SkyStats_Finale.pptx**, 20 diapositives avec notes pour l’oral : 18 minutes, démonstration comprise. Quatre parties de 4 min 30, dans l’ordre Liam, Ryad, Louis, Bryan.

Le rapport et la présentation sont remis séparément.

## Source

[Kaggle — Air Crashes Full Data 1908–2023](https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023), publié par jogwums.

Les résultats portent sur le fichier CSV fourni pour le projet, et non sur une éventuelle mise à jour ultérieure de la page Kaggle.
