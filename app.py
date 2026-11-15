import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def charger_donnees():

    # Dans un premier temps on va récuperer les données et transformer en tableau d'ou le sep=","
    # qui nous permet en autre de convertir en tableau pour le programme
    brut = pd.read_csv("aircrashesFullData.csv", sep=",")

    # PARTIE FILTRAGE
    df = brut.drop_duplicates().copy()
    for colonne in ["Year", "Aboard", "Fatalities (air)"]:
        df[colonne] = pd.to_numeric(df[colonne], errors="coerce")
        
    for colonne in ["Aboard", "Fatalities (air)"]:
        df.loc[df[colonne] < 0, colonne] = np.nan

    # choix de nos paramètres 
    df = df[(df["Year"] >= 1908) & (df["Year"] <= 2023)].copy()
    df["Year"] = df["Year"].astype(int)
    
    
    for source, cible in [("Aircraft Manufacturer", "Constructeur"),
                          ("Aircraft", "Modele"), ("Operator", "Operateur")]:
        df[cible] = df[source].fillna("Non renseigné")
        df[cible] = df[cible].str.split().str.join(" ")
        df[cible] = df[cible].replace("", "Non renseigné")


            # La on à remarqué que à chaque fois que les gens qui mettent les infos ne connaissent pas ils mettent '?'
            # au tout debut. Ici on va juste repertoriés ses lignes avec startswith qui est booléen (attribut true or false)
            # et ensuite on va leurs attribué 'Non renseigné'
        inconnu = df[cible].str.startswith("?")
        df.loc[inconnu, cible] = "Non renseigné"



    # Listes des constructeurs redondant pour simplifier les écritures du genre si on à Boeing Industry ou Boeing aircraft
    # les 2 deviennent simplement Boeing
    familles = ["McDonnell Douglas", "de Havilland Canada", "de Havilland",
                "Boeing", "Airbus", "Douglas", "Lockheed", "Antonov", "Fokker"]
    origine = df["Constructeur"].str.lower()

    # les constructeurs toujours pas ranger 
    restant = pd.Series(True, index=df.index)
    for famille in familles:
        masque = restant & origine.str.startswith(famille.lower())
        df.loc[masque, "Constructeur"] = famille
        restant = restant & ~masque

    # Les variantes du 737 deviennent « Boeing 737 » par exemple.
    modele_brut = df["Modele"].str.lower()
    for numero in ["707", "717", "720", "727", "737", "747", "757", "767", "777", "787"]:
        prefixes = ("boeing b " + numero, "boeing " + numero, "boeing b" + numero)
        masque = (df["Constructeur"] == "Boeing") & modele_brut.str.startswith(prefixes)
        df.loc[masque, "Modele"] = "Boeing " + numero

    # Ici on à pris l'exemple de Air france pour standardiser 
    masque = df["Operateur"].str.lower().str.contains("air france", regex=False)
    df.loc[masque, "Operateur"] = "Air France (mention explicite)"
    return df


def calculer_indicateurs(selection):
     # PARTIE KPI
    
    # Décès qu'on connais total et pourcentage de vol sans décès
    connus = selection[selection["Fatalities (air)"].notna()]
    deces = np.nan
    sans_deces = np.nan
    if len(connus) > 0:
        deces = connus["Fatalities (air)"].sum()
        nombre_sans_deces = len(connus[connus["Fatalities (air)"] == 0])
        sans_deces = 100 * nombre_sans_deces / len(connus)

    # Filtration des valeurs aberrantes (exemple le nombre de mort plus élevé que les passagers)
    # Calcul du nombre de survivant et le taux de survie global
    masque = ((selection["Aboard"] > 0)
              & (selection["Fatalities (air)"] >= 0)
              & (selection["Fatalities (air)"] <= selection["Aboard"]))
    valides = selection[masque].copy()
    valides["Survivants"] = valides["Aboard"] - valides["Fatalities (air)"]
    taux_survie = np.nan
    if len(valides) > 0:
        total_survivants = valides["Survivants"].sum()
        total_occupants = valides["Aboard"].sum()
        taux_survie = 100 * total_survivants / total_occupants
    return valides, deces, taux_survie, sans_deces


def afficher_application():

    # PARTIE Affichage
    
    st.set_page_config(page_title="SkyStats", layout="wide")
    st.title("SkyStats : accidents aériens, bilan historique")
    
    df = charger_donnees()
    
    #st.write("Au fil des années, le réseau aérien n'a eu de cesse de s'améliorer, ce qui fait baisser le taux d'accident.")
    st.write("Comment le nombre d’accidents et leur bilan humain changent-ils selon le constructeur, le modèle d’avion, l’opérateur et la période étudiée ?")
    st.caption("Jeu de données : Air Crashes Full Data — sélection 1908–2023.")
    st.info("Ces chiffres décrivent les événements présents dans le fichier. Le nombre total de vols est inconnu : ils ne permettent pas de calculer un risque par vol ni de classer la sécurité des avions ou des compagnies.")
    sns.set_theme(style="whitegrid")
    
    # Graphique global : morts par an de 1908-2023 (indépendant des filtres)
    deces_par_an = df.groupby("Year")["Fatalities (air)"].sum(min_count=1)
    fig_global, ax_global = plt.subplots(figsize=(10, 4))
    ax_global.plot(deces_par_an.index, deces_par_an.values, color="red")
    ax_global.set_title("Décès à bord déclarés par an dans la base (1908–2023)")
    ax_global.set_xlabel("Année")
    ax_global.set_ylabel("Nombre de morts")
    st.pyplot(fig_global)
    plt.close(fig_global)
    st.caption("Vue globale, indépendante des filtres : décès à bord déclarés, hors décès au sol.")

    st.write("Choisissez un constructeur, un avion et un opérateur pour explorer les données de 1908 à 2023.")
    # st.info("une analyse des infos")

    # Les options d'un menu dépendent des choix effectués au-dessus.
    st.sidebar.header("Votre sélection")
    constructeur = st.sidebar.selectbox("Constructeur", ["Tous"] + sorted(df["Constructeur"].unique()))
    selection = df.copy()
    if constructeur != "Tous":
        selection = selection[selection["Constructeur"] == constructeur]
    modele = st.sidebar.selectbox("Type d'appareil", ["Tous"] + sorted(selection["Modele"].unique()))
    if modele != "Tous":
        selection = selection[selection["Modele"] == modele]
    operateur = st.sidebar.selectbox("Compagnie / opérateur", ["Tous"] + sorted(selection["Operateur"].unique()))
    if operateur != "Tous":
        selection = selection[selection["Operateur"] == operateur]
    debut, fin = st.sidebar.slider("Période d'analyse", 1908, 2023, (2014, 2023))
    selection = selection[(selection["Year"] >= debut) & (selection["Year"] <= fin)]
    st.sidebar.caption("Les libellés commençant par ? sont classés Non renseigné. Les textes d'origine restent consultables dans le tableau.")

    st.subheader("Les chiffres de votre sélection")
    #st.caption(f"{constructeur} / {modele} / {operateur} / {debut}–{fin}")
    if selection.empty:
        st.warning("Aucun enregistrement pour cette sélection. Cela ne prouve pas une absence d'accidents. Élargissez la période ou choisissez « Tous ».")
        return
    
    valides, deces, survie, sans_deces = calculer_indicateurs(selection)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Enregistrements", len(selection))
    c2.metric("Décès à bord déclarés", "Non calculable" if pd.isna(deces) else f"{deces:,.0f}".replace(",", " "))
    c3.metric("Survie globale", "Non calculable" if pd.isna(survie) else f"{survie:.1f} %")
    c4.metric("Sans décès à bord", "Non calculable" if pd.isna(sans_deces) else f"{sans_deces:.1f} %")
    st.caption("Décès déclarés : somme des bilans connus, y compris les lignes dont le nombre de personnes à bord est incohérent. Sans décès à bord : part des bilans connus égaux à zéro.")
    st.caption(f"Survie : {len(valides)} lignes cohérentes sur {len(selection)}. Le taux utilise le total des survivants divisé par le total des occupants de ces mêmes lignes.")


    
    # Graphique Pie Chart

    st.subheader("1. Bilans humains de la sélection")
    if valides.empty:
        st.info("Données insuffisantes pour la répartition survivants / décès.")
    else:
        total_survivants = valides["Survivants"].sum()
        total_deces = valides["Fatalities (air)"].sum()
        
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        ax1.pie([total_survivants, total_deces], 
                labels=["Survivants", "Décès"], 
                autopct="%1.1f%%", 
                colors=["#2baf62", "#e74c3c"])
        ax1.set_title(f"Répartition survivants / décès ({len(valides)} enregistrements)")
        st.pyplot(fig1)
        plt.close(fig1)


    # Graphique 2 : des pires années de la sélection en termes d'accidents

    st.subheader("2. Années avec le plus d'accidents")
    accidents_par_an = selection["Year"].value_counts().head(10).sort_values()
    if accidents_par_an.empty:
        st.info("Aucune donnée.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(accidents_par_an.index.astype(str), accidents_par_an.values, color="#3498db")
        ax.set_xlabel("Nombre d'accidents")
        ax.set_ylabel("Année")
        st.pyplot(fig)
        plt.close(fig)
    
    # Graphique 3 : Modèles impliqués de la sélection
    st.subheader("3. Modèles d'avions les plus impliqués")
    top_modeles = selection["Modele"].value_counts().head(5).sort_values()
    if top_modeles.empty or (len(top_modeles) == 1 and modele != "Tous"):
        st.info("Sélection trop restreinte pour un classement des modèles.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(top_modeles.index, top_modeles.values, color="#9b59b6")
        ax.set_xlabel("Nombre d'accidents")
        ax.set_ylabel("Modèle")
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Données sélectionnées")
    st.caption("Aperçu limité à 50 lignes ; le téléchargement contient toute la sélection.")
    colonnes = ["Year", "Constructeur", "Modele", "Operateur", "Aircraft Manufacturer",
                "Aircraft", "Operator", "Country/Region", "Location", "Aboard", "Fatalities (air)", "Ground"]
    st.dataframe(selection[colonnes].head(50), hide_index=True)
    st.download_button("Télécharger la sélection (CSV)",
                       data=selection[colonnes].to_csv(index=False, sep=",").encode("utf-8-sig"),
                       file_name="selection_accidents.csv", mime="text/csv")


    st.subheader("Interprétation et limites")
    st.write("Le résultat dépend des lignes retenues. Les effectifs, les bilans humains et la survie apportent des informations différentes. Les noms incomplets, la collecte historique et le mélange des opérations limitent nos comparaisons.")
    st.write("Le bilan présenté porte sur les décès à bord. La colonne Ground reste consultable dans le tableau, mais elle n’est pas additionnée : un même bilan au sol peut être répété pour plusieurs appareils impliqués dans un événement.")
    st.write("Les survivants sont calculés par différence entre personnes à bord et décès à bord. Le fichier ne permet pas de distinguer les blessés des personnes indemnes, ni d’analyser les causes des accidents.")
    st.write("Les opérations militaires et civiles ont des contextes différents. Un opérateur militaire ne signifie pas automatiquement une mission de guerre ; un accident commercial ne signifie pas automatiquement une panne technique.")
    st.subheader("Source :")
    st.markdown("[Dataset Kaggle](https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023)")

if __name__ == "__main__":
    afficher_application()

  #  python -m streamlit run Projet_final/Projet_final.py