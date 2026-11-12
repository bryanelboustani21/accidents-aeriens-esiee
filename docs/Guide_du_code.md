# Comprendre app.py

## Problématique

Comment le nombre d’accidents et leur bilan humain changent-ils selon le constructeur, le modèle d’avion, l’opérateur et la période étudiée ?

## 1. Les bibliothèques

`streamlit` affiche la page et les commandes. `pandas` lit et manipule le tableau.
`numpy` fournit les calculs et les valeurs manquantes. `matplotlib` dessine les
courbes et les barres. `seaborn` dessine l'histogramme.

## 2. charger_donnees : préparer un tableau utilisable

```python
brut = pd.read_csv("data/raw/aircrashesFullData.csv", sep=",")
```

Un CSV est un fichier texte. La virgule sépare les champs. La première ligne
contient les noms de colonnes. `brut` est un DataFrame : un tableau avec des
lignes et des colonnes. Le résultat est 5 052 lignes et 12 colonnes.
Les guillemets protègent un texte contenant lui-même une virgule. Il faut
laisser le lecteur CSV les traiter, plutôt que découper chaque ligne à la main.

`drop_duplicates()` enlève les lignes identiques. `.copy()` crée une copie.
Le fichier brut reste intact. `pd.to_numeric(..., errors="coerce")` convertit
une colonne en nombres et met une valeur impossible à convertir en manquante.
`np.nan` désigne une valeur numérique manquante.

```python
df = df[(df["Year"] >= 1908) & (df["Year"] <= 2023)].copy()
```

Chaque comparaison produit des vrais et des faux. `&` impose les deux conditions.
Les crochets conservent seulement les lignes vraies. Il reste 5 017 lignes.
`astype(int)` donne des années entières.

`fillna` remplace une absence de texte. `str.split().str.join(" ")` uniformise
les espaces. Les trois colonnes Constructeur, Modele et Operateur servent aux
menus, les colonnes anglaises originales restent consultables.

`str.startswith("?")` repère un libellé dont le début ne permet pas d’identifier
la catégorie. Ces valeurs deviennent Non renseigné dans les menus. Les 15 lignes
concernées conservent leur texte brut et leurs bilans ; aucun constructeur ni
modèle n’est inventé.

`str.startswith` reconnaît un début explicite, comme Boeing. Le masque
`restant` garantit que de Havilland Canada garde sa famille spécifique avant
le test de Havilland. Les variantes écrites Boeing B 737 et Boeing 737 Max...
sont regroupées sous Boeing 737. Aucune reconstruction automatique des autres
modèles n'est faite.

Pour Air France, `str.contains("air france", regex=False)` cherche ces mots
consécutifs. Ce sont seulement les mentions explicites de la base. Le programme
ne transforme pas Transaviaexport en Transavia.

`Year // 10 * 10` calcule le début de décennie : 1987 donne 1980.
`@st.cache_data` évite de relire le fichier à chaque déplacement de curseur,
comme dans test.py. `return` renvoie le brut et le tableau préparé.

## 3. calculer_indicateurs : définir les populations

Le total déclaré additionne les décès renseignés de la sélection. Les lignes
sans décès à bord sont celles avec Fatalities (air) = 0. Le programme les compte
avec `nombre_sans_deces`, puis calcule `100 * nombre_sans_deces / len(connus)`.
Le dénominateur comprend seulement les lignes dont le bilan est connu.

Pour calculer la survie, on retient Aboard > 0, décès connus et
0 ≤ décès ≤ Aboard. Les 22 occupations nulles de 1908–2023 ne permettent pas
un taux et ne sont pas inventées. Elles restent dans les autres indicateurs.
Les 9 décès supérieurs aux occupants sont inclus dans ces 22 cas.

```python
valides["Survivants"] = valides["Aboard"] - valides["Fatalities (air)"]
total_survivants = valides["Survivants"].sum()
total_occupants = valides["Aboard"].sum()
taux_survie = 100 * total_survivants / total_occupants
```

Exemple : 10 survivants sur 10 occupants et 0 sur 100. La survie globale vaut
10/110 = 9,09 %. La moyenne des taux 100 % et 0 % vaut 50 % et décrit autre chose.
Le dashboard utilise le taux global. `if len(valides) > 0` évite une division
sans population. Un taux impossible à calculer s'affiche Non calculable.

## 4. afficher_application : filtres et affichage

Les selectbox et le slider fonctionnent comme les contrôles de test.py.
Les options du modèle dépendent du constructeur, celles de l'opérateur des
choix précédents. L'option Tous conserve toutes les catégories disponibles.
La période s'applique en dernier et peut donner une sélection vide. Le message
correspondant indique une absence de ligne dans le fichier.

`st.columns` dispose les quatre indicateurs. `st.metric` affiche leur valeur.
Ce sont des compléments d'affichage simples au cours, sans nouveau calcul.

`groupby("Decennie").size()` compte les lignes par décennie.
`np.arange` fabrique la liste des décennies et `reindex(..., fill_value=0)`
complète les décennies sans ligne. `plt.subplots` crée une figure et un axe.
`ax.plot` trace la courbe, `ax.bar` les barres, `sns.histplot` l'histogramme.
`st.pyplot(fig)` montre la figure, comme dans le TD Streamlit.
`plt.close(fig)` ferme la figure après affichage pour libérer la mémoire.

L'histogramme utilise 20 intervalles égaux entre minimum et maximum de la
sélection. `np.mean` et `np.median` en donnent la moyenne et la médiane.
Les intervalles se recalculent après un filtre : ne pas comparer directement
les hauteurs de deux histogrammes dont les bornes ont changé.

`head(50)` limite l'extrait à 50 lignes. Le bouton télécharge toutes les lignes
de la sélection. `to_csv(index=False, sep=",")` génère le CSV. L'encodage
utf-8-sig aide Excel à reconnaître les accents. La checkbox montre la méthode.

Le bloc `if __name__ == "__main__"` lance l'interface lorsque le programme
s'exécute. Il permet aussi de vérifier les fonctions sans afficher l'application.

## Questions à expliquer avec ses mots

Pourquoi exclure Aboard = 0 de la survie ? Pourquoi garder ces lignes ailleurs ?
Pourquoi un taux global diffère-t-il d'une moyenne des taux par accident ?
Pourquoi garder un événement très grave ? Pourquoi la courbe ne mesure-t-elle
pas un risque par vol ? Que signifie une sélection vide ? Quelles corrections
des noms sont certaines et lesquelles restent impossibles ?
