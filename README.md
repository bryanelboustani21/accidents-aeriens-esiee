# Accidents aériens : bilan historique

Projet ESIEE Paris. Version simple du 12 novembre 2026.

**[Ouvrir le dashboard en ligne](https://accidents-aeriens-esiee-berqbs6auc7f4txjtyjxip.streamlit.app/)**

L'utilisateur choisit un constructeur, un type d'appareil, un opérateur et une
période dans la barre latérale. La page affiche quatre indicateurs, trois
graphiques, un extrait des lignes sélectionnées et un téléchargement CSV.
La démonstration utilise ce lien hébergé, sans installation pour le public.

## Le code à étudier

Tout le programme est dans **app.py**, avec trois fonctions :
`charger_donnees`, `calculer_indicateurs`, `afficher_application`.
Le fichier brut est `data/raw/aircrashesFullData.csv` et les dépendances sont
dans `requirements.txt`. `.streamlit/config.toml` définit les couleurs.

## CSV et périmètre

`pd.read_csv("data/raw/aircrashesFullData.csv", sep=",")` lit la virgule comme
séparateur, en respectant les champs entre guillemets. Le fichier a 5 052 lignes
et 12 colonnes. Il contient des dates jusqu'en 2026. Le projet retient
volontairement **1908–2023**, soit **5 017 lignes**. Le CSV brut reste intact.

## Définitions des quatre indicateurs

- Enregistrements : nombre de lignes sélectionnées.
- Décès à bord déclarés : somme de `Fatalities (air)` renseignés.
- Survie globale : 100 × somme des survivants / somme des occupants, sur les
  mêmes lignes avec Aboard > 0 et 0 ≤ Fatalities (air) ≤ Aboard.
- Sans décès à bord : 100 × nombre de lignes à zéro décès / nombre de lignes
  dont le bilan à bord est connu.

Sur l'ensemble 1908–2023 : 111 686 décès à bord déclarés, 28,4 % de survie globale
et 1,7 % de lignes sans décès à bord. La survie repose sur 4 995 lignes valides.
Les barres survivants/décès utilisent cette population et peuvent donc présenter
un total de décès différent du total déclaré sur toutes les lignes.

## Nettoyage et limites

Les colonnes utiles deviennent numériques. Une valeur invalide ou négative
reste manquante. Les doublons exacts sont retirés, aucun n'est présent dans ce
fichier. Les espaces sont uniformisés et les opérateurs absents deviennent
Non renseigné. Neuf familles de constructeurs et dix modèles Boeing sont
regroupés par préfixes explicites. Les autres libellés restent tels qu'écrits.
Les colonnes originales restent dans le tableau et l'export.

Air France (mention explicite) regroupe seulement les textes contenant
« air france ». Ce filtre retrouve 7 lignes. Il ne reconstitue pas l'historique
complet de la compagnie. Transaviaexport reste distincte de Transavia.
Il n'existe aucune colonne Summary : aucune cause n'est estimée.
Le nombre total de vols manque, donc les résultats ne donnent pas le risque
par vol et ne classent pas les compagnies ou constructeurs par sécurité.

## Remise du code et vérifications

Pour télécharger le code : bouton **Code / Download ZIP** de ce dépôt.
Conserver les dossiers. Le code du projet est app.py.

Commandes de reproduction, depuis le dossier du projet :

```bash
pip install -r requirements.txt
python tests/verifier.py
streamlit run app.py
```

Le dashboard est déjà disponible en ligne. La commande Streamlit sert à la
reproduction du code par une personne qui souhaite l'exécuter elle-même.

## Guides

- `docs/Guide_du_code.md` : explications des instructions et des calculs.
- `docs/Guide_client.md` : manipulations et résultats attendus.
- `docs/Deroule_oral.md` : 16 diapositives, 18 minutes.
- `docs/Correspondance_cours.md` : lien avec les supports du cours.
- `docs/Checklist_rendu.md` : correspondance aux exigences.

Source Kaggle : https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023
Le fichier fourni par l'étudiant est la version effectivement étudiée.
