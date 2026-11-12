# Méthodes et supports du cours

## Problématique

Comment le nombre d’accidents et leur bilan humain changent-ils selon le constructeur, le modèle d’avion, l’opérateur et la période étudiée ?

| Programme | Notion | Support fourni |
|---|---|---|
| imports, def, if, for, listes et return | Bases de Python | Chap1_Cours1_2 |
| read_csv et DataFrame | Lecture CSV et tableau | Chap1_Cours4, p. 4–7 et TD Pandas |
| fillna, conversions, copie et filtres | Préparation des données | Chap1_Cours4 et TP03 |
| masques booléens et & | Sélection des lignes | Chap1_Cours4, p. 8 |
| groupby et sommes | Agrégation | Chap1_Cours4, p. 11–17 |
| np.arange, np.mean, np.median | Tableaux et statistiques | Chap1_Cours3 et TD NumPy |
| Courbe et barres | Évolution et comparaison | Chap2_Cours1, p. 10–11 |
| Histogramme | Distribution | Chap2_Cours1, p. 8 et TP04 |
| sidebar, selectbox, slider et checkbox | Commandes interactives | Streamlit_Cours_TD, p. 1–6 |
| plt.subplots et st.pyplot | Affichage de graphiques | Streamlit_Cours_TD, p. 2–4 |
| cache_data et download_button | Cache et téléchargement | test.py |

Les numéros désignent les pages PDF. Les regroupements de noms sont une
application des conditions et des chaînes de caractères. Les préfixes retenus
sont explicites et les colonnes originales restent disponibles.
Les libellés commençant par `?` sont classés Non renseigné dans les menus.
Cette règle concerne 15 lignes pour le constructeur et le type d’appareil,
sans supprimer ces lignes ni changer les bilans humains.

Compléments pratiques à expliquer : pd.to_numeric, drop_duplicates, astype,
les méthodes str, reindex et copy ne figurent pas tous explicitement dans
les diapositives de base. Leur rôle est détaillé dans Guide_du_code.md.
Le taux global de survie utilise simplement des sommes et une division.
st.metric, st.columns et st.caption organisent l'affichage. Le bloc main
sépare l'exécution de l'import pour les vérifications.

La structure reprend test.py : imports, préparation du DataFrame, commandes
latérales, filtre, statistiques, graphiques et téléchargement. Les données
historiques remplacent les données artificielles de cet exemple.

L'énoncé du projet demande de simuler une présentation au client. La
présentation utilise des scénarios de filtres. Aucun rééchantillonnage ni modèle
prédictif n'est nécessaire dans cette version.
