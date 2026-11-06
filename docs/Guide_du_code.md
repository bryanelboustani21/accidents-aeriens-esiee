# Comprendre le code et les résultats

## 1. Ce qui se passe au lancement

`app.py` charge le CSV avec `load_raw`, appelle `clean_data`, puis affiche une page
choisie dans la barre latérale. Les filtres sélectionnent un sous-ensemble sans modifier
le fichier brut. Les calculs et graphiques travaillent sur cette sélection.

## 2. Lecture et types

Un DataFrame est un tableau dont les colonnes portent des noms. `pd.read_csv`
lit le fichier et crée ce tableau. `pd.to_numeric(..., errors='coerce')` transforme
en nombres les valeurs exploitables et signale les échecs par une valeur manquante.
`pd.to_datetime` assemble l'année, le mois et le jour en une date comparable.

## 3. Nettoyage et drapeaux

`source_row` indique le numéro de ligne dans le CSV original, en comptant l'en-tête.
Il sert à retrouver une anomalie. `country_raw` et `manufacturer_raw` gardent
les libellés originaux avec seulement une normalisation des espaces.

`resolve_country` applique des correspondances exactes : un nom ISO, un alias
écrit explicitement ou une région reconnue. `New` et `South` ne suffisent pas à
identifier un pays. `Georgia`, `Congo` et `Victoria` sont ambigus dans ce fichier.
Aucune correction approximative ne leur attribue arbitrairement un pays.

Les colonnes booléennes indiquent si une condition est vraie ou fausse :

| Colonne | Sens |
|---|---|
| `date_valid` | Date lisible et non postérieure au 6 novembre 2026 |
| `counts_valid` | Occupants, décès à bord et décès au sol renseignés, entiers et non négatifs |
| `fatalities_exceed_aboard` | Décès à bord supérieurs aux occupants |
| `survival_valid` | Comptes valides, occupants strictement positifs et décès cohérents |
| `analysis_valid` | Date et comptes valides, et absence de doublon exact à retirer |

La validité générale ne garantit pas l'exactitude historique de chaque ligne.
Les 22 occupations nulles sont exclues seulement du calcul de survie. Parmi elles,
9 lignes indiquent des décès positifs. On ne transforme ni ces occupants en décès,
ni ces décès en zéro. Les anomalies restent consultables.

## 4. Taux pondéré de survie

Sur les mêmes lignes valides :

`survivants = occupants - décès_à_bord`

`taux = somme(survivants) / somme(occupants)`

Exemple fictif : 10 survivants sur 10 occupants dans une ligne, puis 0 sur 100
dans une autre. Le taux agrégé vaut 10 / 110 = 9,1 %, pas la moyenne simple
de 100 % et 0 %, qui donnerait 50 %. Le premier calcul pondère par les personnes.

Le taux concerne cette sélection d'accidents. Il ne désigne pas la probabilité
de survivre à un voyage en avion.

## 5. Groupby et filtres

`groupby('year')` rassemble les lignes d'une même année. `agg` calcule un effectif
et une somme par groupe. `between(1980,1999)` produit un masque booléen pour la
période. `isin(...)` teste si la catégorie appartient à la liste choisie.
Un `reindex` réintroduit les années absentes avec zéro enregistrement dans le fichier.
Cela ne signifie pas zéro accident réel pendant ces années.

## 6. Simulation avec remise, pas à pas

1. Garder les lignes compatibles avec le calcul de survie.
2. Transformer les colonnes occupants/décès en tableau NumPy.
3. Tirer des indices de lignes avec `RandomState(seed).randint`.
4. Récupérer des lignes entières avec ces indices. La même ligne peut revenir.
5. Additionner occupants et décès pour chaque répétition.
6. Répéter 1 000 fois et décrire la distribution des totaux.

On tire les deux colonnes ensemble : cela évite d'associer les décès d'un grand
appareil aux occupants d'un autre. La graine 42 reproduit les mêmes tirages.
Q05 est le 5e centile des résultats, Q95 le 95e. Les valeurs peuvent être
interpolées et donc non entières. L'intervalle central des simulations n'est
pas un intervalle de confiance sur la sécurité aérienne.

Hypothèses : les lignes sont échangeables, tirées indépendamment avec la même
probabilité. La source mélange des périodes et opérations différentes. Changer
la période ou le pays modifie la population simulée. Ce modèle pédagogique
n'est donc pas un outil de prévision ni une démonstration causale.

## 7. Sensibilité de gravité

Pour une réduction relative r : `F_hypothétique = F_observé * (1-r)`.
Une baisse relative de 10 % ne signifie pas une hausse de 10 points du taux
de survie. Les résultats théoriques peuvent être décimaux. Le calcul ne dit pas
qu'une mesure réelle produira cette baisse : il impose la baisse pour en explorer l'effet.

## 8. Statistiques et graphiques

La moyenne est sensible aux grands événements. La médiane décrit une valeur
centrale plus robuste. Le boxplot montre la médiane et l'intervalle interquartile.
Les moustaches s'étendent aux valeurs dans 1,5 fois l'intervalle interquartile.
Un point au-delà est atypique selon cette règle, pas nécessairement erroné.

Une corrélation mesure une association linéaire. Occupants et décès sont liés par
la capacité de l'appareil et par la contrainte décès <= occupants sur les lignes valides.
Une forte corrélation ne démontre donc pas qu'un grand appareil est plus dangereux.

## 9. Questions probables à l'oral

- Pourquoi ne pas supprimer toutes les lignes incomplètes ? Parce que l'utilité
  d'une ligne dépend du calcul. Un pays absent n'empêche pas une analyse annuelle.
- Pourquoi exclure 2026 par défaut ? L'année et la collecte sont partielles.
- Pourquoi ne pas additionner tous les décès au sol ? Certains bilans d'un même
  événement apparaissent sur plusieurs lignes, sans identifiant fiable de regroupement.
- Pourquoi ne pas classer les compagnies par danger ? Le nombre de vols manque.
- Pourquoi garder des événements extrêmes ? Une grande valeur peut être réelle.
- Pourquoi le taux de survie ne monte-t-il pas forcément quand les effectifs baissent ?
  Les deux indicateurs n'ont pas le même dénominateur et la composition de la base change.
