import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def charger_donnees():
    # Une virgule sépare les colonnes. Le fichier d'origine reste intact.
    brut = pd.read_csv("data/raw/aircrashesFullData.csv", sep=",")
    df = brut.drop_duplicates().copy()
    for colonne in ["Year", "Aboard", "Fatalities (air)"]:
        df[colonne] = pd.to_numeric(df[colonne], errors="coerce")
    for colonne in ["Aboard", "Fatalities (air)"]:
        df.loc[df[colonne] < 0, colonne] = np.nan

    # Périmètre choisi pour le projet : 1908 à 2023 inclus.
    df = df[(df["Year"] >= 1908) & (df["Year"] <= 2023)].copy()
    df["Year"] = df["Year"].astype(int)
    for source, cible in [("Aircraft Manufacturer", "Constructeur"),
                          ("Aircraft", "Modele"), ("Operator", "Operateur")]:
        df[cible] = df[source].fillna("Non renseigné").str.split().str.join(" ")
        df[cible] = df[cible].replace("", "Non renseigné")

    # Préfixes explicites. Les autres noms restent tels qu'ils sont écrits.
    familles = ["McDonnell Douglas", "de Havilland Canada", "de Havilland",
                "Boeing", "Airbus", "Douglas", "Lockheed", "Antonov", "Fokker"]
    origine = df["Constructeur"].str.lower()
    restant = pd.Series(True, index=df.index)
    for famille in familles:
        masque = restant & origine.str.startswith(famille.lower())
        df.loc[masque, "Constructeur"] = famille
        restant = restant & ~masque

    # Les variantes explicitement écrites du 737 deviennent « Boeing 737 ».
    modele_brut = df["Modele"].str.lower()
    for numero in ["707", "717", "720", "727", "737", "747", "757", "767", "777", "787"]:
        prefixes = ("boeing b " + numero, "boeing " + numero, "boeing b" + numero)
        masque = (df["Constructeur"] == "Boeing") & modele_brut.str.startswith(prefixes)
        df.loc[masque, "Modele"] = "Boeing " + numero

    # Cette règle ne reconnaît que les mentions exactes « air france ».
    masque = df["Operateur"].str.lower().str.contains("air france", regex=False)
    df.loc[masque, "Operateur"] = "Air France (mention explicite)"
    df["Decennie"] = (df["Year"] // 10) * 10
    return brut, df


def calculer_indicateurs(selection):
    # Décès connus : dénominateur de la part des lignes sans décès.
    connus = selection[selection["Fatalities (air)"].notna()]
    sans_deces = np.nan
    if len(connus) > 0:
        sans_deces = 100 * (connus["Fatalities (air)"] == 0).mean()

    # Même population pour les survivants, les décès et les occupants.
    masque = ((selection["Aboard"] > 0)
              & (selection["Fatalities (air)"] >= 0)
              & (selection["Fatalities (air)"] <= selection["Aboard"]))
    valides = selection[masque].copy()
    valides["Survivants"] = valides["Aboard"] - valides["Fatalities (air)"]
    taux_survie = np.nan
    if len(valides) > 0:
        taux_survie = 100 * valides["Survivants"].sum() / valides["Aboard"].sum()
    deces = connus["Fatalities (air)"].sum() if len(connus) > 0 else np.nan
    return valides, deces, taux_survie, sans_deces


def afficher_application():
    st.set_page_config(page_title="Accidents aériens", layout="wide")
    st.title("Accidents aériens : bilan historique")
    st.write("Choisissez un constructeur, un appareil et un opérateur pour explorer les données de 1908 à 2023.")
    st.info("Ces résultats décrivent les événements présents dans le fichier. Le nombre total de vols est inconnu : aucun risque par vol n'est calculé.")
    brut, df = charger_donnees()

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
    debut, fin = st.sidebar.slider("Période d'analyse", 1908, 2023, (1908, 2023))
    selection = selection[(selection["Year"] >= debut) & (selection["Year"] <= fin)]
    st.sidebar.caption("Certains noms d'opérateurs sont incomplets. Les libellés bruts restent consultables dans le tableau.")

    st.subheader("Les chiffres de votre sélection")
    st.caption(f"{constructeur} / {modele} / {operateur} / {debut}–{fin}")
    if selection.empty:
        st.warning("Aucun enregistrement pour cette sélection. Cela ne prouve pas une absence d'accidents. Élargissez la période ou choisissez « Tous ».")
        return
    valides, deces, survie, sans_deces = calculer_indicateurs(selection)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Enregistrements", len(selection))
    c2.metric("Décès à bord déclarés", "Non calculable" if pd.isna(deces) else f"{deces:,.0f}".replace(",", " "))
    c3.metric("Survie globale", "Non calculable" if pd.isna(survie) else f"{survie:.1f} %")
    c4.metric("Sans décès à bord", "Non calculable" if pd.isna(sans_deces) else f"{sans_deces:.1f} %")
    st.caption(f"Survie : {len(valides)} lignes cohérentes sur {len(selection)}. Le taux utilise le total des survivants divisé par le total des occupants de ces mêmes lignes.")
    st.caption("Sans décès à bord : part des lignes dont le bilan à bord est connu et égal à zéro. Les décès au sol ne sont pas inclus dans ces indicateurs.")

    sns.set_theme(style="whitegrid")
    st.subheader("1. Évolution par décennie")
    decennies = np.arange((debut // 10) * 10, (fin // 10) * 10 + 1, 10)
    evolution = selection.groupby("Decennie").size().reindex(decennies, fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.plot(evolution.index, evolution.values, marker="o", color="#174A78")
    ax.set_xlabel("Début de décennie")
    ax.set_ylabel("Nombre d'enregistrements")
    ax.set_xticks(decennies)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("La courbe permet de suivre les effectifs dans le temps. Les décennies aux extrémités peuvent être partielles. Zéro signifie aucune ligne dans le fichier pour cette sélection.")

    st.subheader("2. Survivants et décès à bord")
    if valides.empty:
        st.info("Aucune ligne ne permet de calculer la répartition entre survivants et décès.")
    else:
        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.bar(["Survivants", "Décès à bord"],
               [valides["Survivants"].sum(), valides["Fatalities (air)"].sum()],
               color=["#168D99", "#174A78"])
        ax.set_ylabel("Personnes déclarées")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"Les barres comparent les deux groupes sur {len(valides)} lignes cohérentes. Les lignes avec occupation nulle ou décès supérieurs à l'occupation sont exclues de ce graphique.")

    st.subheader("3. Distribution des décès à bord")
    deces_connus = selection["Fatalities (air)"].dropna()
    if deces_connus.empty:
        st.info("Aucun bilan à bord connu dans la sélection.")
    else:
        fig, ax = plt.subplots(figsize=(10, 3.6))
        sns.histplot(deces_connus, bins=20, color="#168D99", ax=ax)
        ax.set_xlabel("Décès à bord par enregistrement")
        ax.set_ylabel("Nombre d'enregistrements")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.write(f"Moyenne : {np.mean(deces_connus):.2f} décès. Médiane : {np.median(deces_connus):.0f} décès.")
        st.caption("L'histogramme montre la répartition de la gravité. Les grandes valeurs restent dans l'analyse car elles peuvent correspondre à des événements réels.")

    st.subheader("Données sélectionnées")
    colonnes = ["Year", "Constructeur", "Modele", "Operateur", "Aircraft Manufacturer",
                "Aircraft", "Operator", "Country/Region", "Location", "Aboard", "Fatalities (air)"]
    st.dataframe(selection[colonnes].head(50), hide_index=True)
    st.download_button("Télécharger la sélection (CSV)",
                       data=selection[colonnes].to_csv(index=False, sep=",").encode("utf-8-sig"),
                       file_name="selection_accidents.csv", mime="text/csv")

    if st.checkbox("Afficher le nettoyage et les définitions"):
        st.write(f"Fichier brut : {brut.shape[0]} lignes et {brut.shape[1]} colonnes. Périmètre 1908–2023 : {len(df)} lignes.")
        st.write(f"Doublons exacts : {brut.duplicated().sum()}. Opérateurs absents dans le fichier brut : {brut['Operator'].isna().sum()}.")
        st.write("Les nombres sont convertis avec Pandas. Une valeur invalide reste manquante. Les espaces sont uniformisés. Les opérateurs absents portent le libellé Non renseigné.")
        st.write("Les constructeurs sont regroupés par préfixe explicite. Pour Boeing, les modèles 707, 717, 720, 727, 737, 747, 757, 767, 777 et 787 sont regroupés par famille écrite. Les autres types conservent leur libellé.")
        st.write("Air France (mention explicite) regroupe seulement les textes contenant air france. Ce filtre ne garantit pas de retrouver tous les événements de cette compagnie. Transaviaexport reste distincte de Transavia.")
        st.write("Survie globale = 100 × somme des survivants / somme des occupants. Sans décès à bord = 100 × nombre de lignes à zéro décès / nombre de lignes au bilan connu.")
    st.subheader("Interprétation et limites")
    st.write("Le résultat dépend des lignes retenues. Les effectifs, les bilans humains et la survie apportent des informations différentes. Les noms incomplets, la collecte historique et le mélange des opérations limitent les comparaisons.")
    st.caption("Source : Kaggle, Jonathan Ogwumike, Air Crashes Full Data. Le CSV fourni va jusqu'en 2026. Ce dashboard retient volontairement 1908–2023. Il ne contient pas de colonne Summary ni de causes d'accidents.")
    st.markdown("[Dataset Kaggle](https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023)")


if __name__ == "__main__":
    afficher_application()
