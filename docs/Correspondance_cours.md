# Correspondance avec les supports fournis

Les pages ci-dessous sont les numéros de pages PDF, couverture comprise.
Le barème indicatif du TD supplémentaire concerne ce TD. Il ne remplace pas
les critères d'évaluation de l'énoncé du projet final.

| Travail dans le projet | Notions utilisées | Support et pages |
|---|---|---|
| Fonctions, boucles, conditions, dictionnaires | `def`, `for`, `if`, `dict`, listes, ensembles | Chap1_Cours1_2, parties Python ; TP01 et TP02 |
| Chargement et exploration | `read_csv`, `head`, `shape`, `dtypes`, `describe` | Chap1_Cours4, p. 4–7 ; TP03 NumPy/Pandas |
| Valeurs manquantes | `isna`, remplacement explicite, conservation de l'information | Chap1_Cours4, p. 5 et 9–10 |
| Sélection de périodes et catégories | masques booléens, `loc`, sélection de colonnes | Chap1_Cours4, p. 8 |
| Regroupements | `groupby`, `agg`, `value_counts`, sommes, médianes | Chap1_Cours4, p. 11–17 |
| Dates, anomalies et dictionnaire de correction | conversion de dates, indicateurs de cohérence, rapport qualité | TD supplémentaire, projet 3, p. 3 |
| Calculs NumPy | tableaux, indexation, calculs vectorisés, sommes, moyennes, écarts-types | Chap1_Cours3, p. 3–12 ; TP03 |
| Courbes | chronologie des enregistrements et décès | Chap2_Cours1, p. 10 |
| Barres | pays identifiés, constructeurs et survie agrégée | Chap2_Cours1, p. 11 |
| Histogrammes | distribution des décès et des résultats fictifs | Chap2_Cours1, p. 8 ; TP04 |
| Nuage de points | occupants et décès à bord | Chap2_Cours1, p. 9 ; TP04 |
| Boîtes à moustaches | gravité sur deux périodes | Chap2_Cours1, p. 12 ; TP04 |
| Heatmap | matrice de corrélation | Chap2_Cours1, p. 14 ; TP04, p. 1 et 3 |
| Dashboard | `title`, `write`, `sidebar`, `slider`, `selectbox`, `multiselect`, `checkbox`, `pyplot` | Streamlit_Cours_TD, p. 1–6 |
| Export, cache et graine aléatoire | `cache_data`, `download_button`, `RandomState(seed)` | test.py fourni |
| Répétitions de simulation et sensibilité | 1 000 répétitions, statistiques, quantiles et invariants | TD supplémentaire, projet 6, p. 5–6 |
| Contrôles | assertions et fonctions documentées avec bloc principal | TD supplémentaire, p. 1 et 6 |

## Adaptations à expliquer, sans prétendre qu'elles figurent mot pour mot dans le cours

- **Rééchantillonnage avec remise.** Le projet 6 enseigne une simulation Monte-Carlo
  logistique. Ici, on tire des lignes historiques entières. Cette technique de
  rééchantillonnage est ajoutée pour préserver le lien entre occupants et décès.
  Il faut expliquer la différence entre simuler des lignes et prévoir des accidents.
  À valider avec l'enseignant si son exigence porte sur les méthodes exactes du cours.
- **Taux pondéré de survie.** Les sommes et divisions sont vues. L'application à ce
  problème demande d'utiliser les mêmes lignes dans le numérateur et le dénominateur.
- **Référentiel de pays.** Le mécanisme est un dictionnaire de correspondance, comme
  le nettoyage des villes du projet 3. Le référentiel ISO est une donnée de référence ajoutée.
- **Syntaxes de nettoyage.** `to_datetime`, `to_numeric`, `duplicated`, `isin`,
  `between`, `reindex` et `map` sont des méthodes pratiques. Toutes ne sont pas
  montrées explicitement dans les diapositives de base. Leur usage est expliqué
  dans le guide du code plutôt que présenté comme déjà maîtrisé.
- **Ergonomie.** `radio`, `metric`, `columns` et `caption` organisent l'interface.
  Ce sont de petits compléments aux widgets du TD, pas de nouvelles analyses statistiques.
- **Vérification technique.** SHA-256 et unittest servent à conserver l'origine du
  fichier et à vérifier les calculs. La classe des tests ne fait pas partie du code
  d'analyse à présenter. Pas besoin d'introduire la programmation objet dans l'oral.

## Niveau de complexité retenu

Pas de modèle prédictif, de machine learning, de scraping, d'API payante ou de base
de données externe. Les résultats reposent sur les tableaux, filtres, agrégations
et graphiques demandés dans l'énoncé. La simulation avancée reste distincte du cœur du projet.
