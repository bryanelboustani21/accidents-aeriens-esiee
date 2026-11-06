# Accidents aériens : analyse et visualisation des données

Projet de groupe ESIEE Paris. Version alignée sur l'application en ligne du 6 novembre 2026.

## Application à présenter

**[Ouvrir le dashboard Streamlit](https://accidents-aeriens-esiee-berqbs6auc7f4txjtyjxip.streamlit.app/)**

Le dashboard est accessible depuis un navigateur sans installer Python.
Ce dépôt constitue le rendu du code. Le rapport et le support de présentation
sont remis séparément.

## Question étudiée

Comment les enregistrements d'accidents aériens et leur gravité varient-ils selon
les périodes, les lieux et les caractéristiques déclarées des appareils ?

Une ligne est un enregistrement, pas nécessairement un événement unique. Le nombre
de vols est inconnu : aucun risque d'accident par vol ni classement de danger n'est calculé.

## Les sept pages

| Page | Contenu |
|---|---|
| Vue d'ensemble | Indicateurs, courbes annuelles, tableau filtré et export |
| Qualité des données | Audit global, décisions, correspondances et anomalies |
| Évolution | Courbes annuelles et survie pondérée par décennie |
| Répartition | Pays identifiés et constructeurs regroupés |
| Gravité et survie | Histogramme, nuage de points, heatmap et boxplot |
| Scénarios | Périodes, nettoyage, sensibilité et Monte-Carlo |
| Méthode et sources | Définitions, hypothèses, limites et références |

## Repères de démonstration

| Sélection | Enregistrements | Décès à bord déclarés | Survie affichée |
|---|---:|---:|---:|
| 1908–2025, tous pays et constructeurs | 5 043 | 112 481 | 28,6 % |
| Même période, France | 109 | 2 019 | 21,8 % |

Les taux utilisent uniquement les lignes compatibles avec le calcul de survie.
L'année 2026 est partielle et exclue par défaut. Une case permet de l'inclure.

## Code et documentation

- `app.py` : interface et scénarios.
- `analyse.py` : lecture, nettoyage, drapeaux, filtres et indicateurs.
- `graphiques.py` : figures et justification des choix.
- `simulations.py` : sensibilité et collections fictives.
- `preparer.py` : reproduction des résultats hors interface.
- `tests/test_metier.py` : huit contrôles des calculs et des cas limites.
- `docs/Guide_du_code.md` : explications et questions probables.
- `docs/Correspondance_cours.md` : lien avec les cours et TD fournis.
- `docs/Deroule_oral.md` : présentation de 18 minutes.
- `docs/Guide_client.md` : mission et démonstration.
- `docs/Checklist_rendu.md` : correspondance avec les consignes.
- `docs/Source_version.json` : origine du fichier et version de référence.

**Conserver les dossiers.** Le CSV brut doit rester dans
`data/raw/aircrashesFullData.csv` et le référentiel dans
`data/reference/iso_countries.csv`. La configuration se trouve dans `.streamlit/config.toml`.

## Reproduire l'analyse

La démonstration utilise le lien en ligne. Pour reproduire les résultats et vérifier
le code sous Python 3.12, dans le dossier du projet, sous Windows :

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python preparer.py
.venv\Scripts\python -m unittest discover -s tests -v
```

Sous macOS / Linux, créer l'environnement avec `python3` puis utiliser `.venv/bin/python`.
`preparer.py` crée `outputs` et `data/processed` sans modifier le CSV brut.
Pour le développement : `python -m streamlit run app.py`.

## Décisions de nettoyage

Le fichier brut contient 5 052 lignes et 12 colonnes. Les 22 occupations nulles,
dont 9 lignes avec décès positifs, sont exclues du taux de survie sans imputation.
Les 1 290 pays non résolus restent signalés. Les victimes au sol ne sont pas
additionnées comme un bilan de personnes uniques, car certains événements
partagent un même bilan entre plusieurs lignes.

## Hypothèses des simulations

La sensibilité impose une baisse relative des décès à occupation constante.
Elle ne démontre l'effet d'aucune intervention réelle.
Monte-Carlo tire des lignes entières avec remise, en gardant les occupants et décès
associés. Le nombre de lignes, les répétitions et la graine sont réglables.
Les quantiles décrivent des collections fictives, sans prévoir d'accidents futurs.

Le principe Monte-Carlo figure dans le TD supplémentaire. Le rééchantillonnage de
lignes historiques est une adaptation à expliquer et à valider si l'enseignant
impose les techniques exactes des exercices.

## Sources

- [Dataset Kaggle](https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023)
- [Périmètre PlaneCrashInfo](https://www.planecrashinfo.com/database.htm)
- Supports de Ryan Belbachir fournis par l'étudiant, détaillés dans Correspondance_cours.md.
- Référentiel ISO : export pycountry 26.2.16 / iso-codes fourni en CSV.

Les supports du cours ne sont pas redistribués dans ce dépôt.
