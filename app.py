"""Lancer avec : python -m streamlit run app.py"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from analyse import load_raw, clean_data, audit_data, select_data, indicators
from simulations import simulate_burden, severity_sensitivity
from graphiques import (annual_figure, category_figure, severity_figure, survival_figure,
                        box_figure, correlation_figure, simulation_figure, JUSTIFICATIONS)


def fmt(value):
    return f"{value:,.0f}".replace(",", " ")


def show(fig, key):
    st.pyplot(fig)
    plt.close(fig)
    st.caption(JUSTIFICATIONS[key])


@st.cache_data
def prepare():
    raw = load_raw()
    cleaned = clean_data(raw)
    return raw, cleaned, audit_data(raw, cleaned)


def main():
    st.set_page_config(page_title="Accidents aériens | Analyse ESIEE", layout="wide")
    raw, cleaned, audit = prepare()
    st.sidebar.title("Accidents aériens")
    page = st.sidebar.radio("Navigation", ["Vue d'ensemble", "Qualité des données", "Évolution", "Répartition", "Gravité et survie", "Scénarios", "Méthode et sources"])
    st.sidebar.subheader("Périmètre de l'analyse")
    include_latest = st.sidebar.checkbox("Inclure 2026 (année partielle)", value=False)
    last = 2026 if include_latest else 2025
    years = st.sidebar.slider("Période", 1908, last, (1908, last))
    countries = st.sidebar.multiselect("Pays identifiés (vide = tous)", sorted(cleaned.loc[cleaned.country_iso3.ne(""), "country"].unique()))
    manufacturers = st.sidebar.multiselect("Constructeurs regroupés (vide = tous)", sorted(cleaned.manufacturer.unique()))
    data = select_data(cleaned, years, countries, manufacturers)
    stats = indicators(data)
    st.title(page)
    st.caption(f"Kaggle / Jonathan Ogwumike · Sélection {years[0]}–{years[1]} · {fmt(len(data))} enregistrements")
    st.info("Les chiffres décrivent les enregistrements de cette base historique. Le nombre total de vols est inconnu : aucun risque d'accident par vol n'est calculé.")
    if include_latest:
        st.warning("2026 est partielle dans le fichier (dernier enregistrement : 1er août). Une année sans ligne signifie une absence dans le fichier, pas l'absence d'accidents réels.")

    if page == "Qualité des données":
        st.write("Cet audit concerne le fichier complet. Les filtres de période, pays et constructeur ne modifient pas les totaux de qualité ci-dessous.")
        cols = st.columns(4)
        for c, title, value in zip(cols, ["Lignes brutes", "Pays manquants", "Occupation nulle", "Décès > occupants"],
                                   [audit['raw_rows'], audit['missing_country'], audit['zero_aboard'], audit['fatalities_exceed_aboard']]):
            c.metric(title, fmt(value))
        rules = pd.DataFrame([
            ["Dates", "Reconstruire année/mois/jour. Écarter dates invalides ou futures des analyses temporelles.", audit['invalid_dates']],
            ["Doublons exacts", "Conserver une seule occurrence si nécessaire. Aucun identifiant d'événement ne permet de fusionner les lignes proches.", audit['exact_duplicates']],
            ["Pays", "Noms ISO exacts, alias écrits et régions explicites. Aucune supposition sur New, South, Georgia ou Congo.", audit['geography_unresolved']],
            ["Opérateur", "Conserver la ligne et afficher Non renseigné.", audit['missing_operator']],
            ["Survie", "Exclure du taux les occupations nulles et les décès supérieurs aux occupants. Conserver les lignes signalées dans les autres analyses.", audit['survival_excluded']],
        ], columns=["Contrôle", "Décision", "Lignes concernées"])
        st.dataframe(rules, hide_index=True)
        st.warning("Les compteurs d'anomalies se recouvrent. Les 9 lignes où les décès dépassent les occupants appartiennent aux 22 lignes d'occupation nulle.")
        st.subheader("Traçabilité des pays")
        mapping = cleaned[["country_raw", "country", "country_iso3", "geo_status"]].drop_duplicates().sort_values("country_raw")
        st.dataframe(mapping, hide_index=True)
        st.subheader("Lignes exclues du calcul de survie")
        excluded = cleaned.loc[~cleaned.survival_valid, ["source_row", "date", "location", "aboard", "fatalities", "ground"]]
        st.dataframe(excluded, hide_index=True)
        st.subheader("Avant / après")
        left, right = st.columns(2)
        left.write("Fichier brut")
        left.dataframe(raw.head(8))
        right.write("Données préparées")
        right.dataframe(cleaned[["source_row", "date", "country", "geo_status", "aboard", "fatalities", "survival_valid"]].head(8))
        st.download_button("Télécharger les données préparées et leurs drapeaux", cleaned.to_csv(index=False).encode("utf-8-sig"), "accidents_prepares.csv", "text/csv")
        return

    if page == "Méthode et sources":
        st.subheader("La question étudiée")
        st.write("Comment les enregistrements d'accidents aériens et leur gravité varient-ils selon les périodes, les lieux et les appareils déclarés ?")
        st.subheader("Définition des indicateurs")
        st.write("Une ligne est un enregistrement, pas nécessairement un événement unique. Les décès à bord sont les valeurs déclarées par la source. Le taux de survie est calculé uniquement sur les lignes dont l'occupation est strictement positive et les comptes cohérents.")
        st.code("taux_survie = somme(occupants - décès_à_bord) / somme(occupants)")
        st.write("Les décès au sol restent dans le tableau. Leur somme globale n'est pas présentée comme un bilan de victimes uniques : le 11 septembre 2001, deux lignes de New York portent chacune 2 750 décès au sol.")
        st.write("Les noms de pays suivent un référentiel actuel et des corrections explicites. Certains territoires et noms historiques restent non résolus. Une comparaison géographique dépend donc aussi de la qualité du renseignement.")
        st.subheader("Simulations")
        st.write("L'analyse de sensibilité impose une hypothèse. Le tirage avec remise génère des collections fictives d'enregistrements ressemblant à la sélection. Il suppose l'échangeabilité des lignes et ignore les dépendances entre événements. Il ne prédit ni les accidents à venir ni les effets d'une mesure de sécurité.")
        st.subheader("Sources")
        st.markdown("- [Dataset Kaggle](https://www.kaggle.com/datasets/jogwums/air-crashes-full-data-1908-2023)\n- [Périmètre de la source historique PlaneCrashInfo](https://www.planecrashinfo.com/database.htm)\n- Supports de Ryan Belbachir fournis avec le projet : NumPy, Pandas, Matplotlib/Seaborn, Streamlit et TD supplémentaire.")
        st.caption("Le rééchantillonnage est une adaptation de Monte-Carlo à expliquer. Voir docs/Correspondance_cours.md. Pas d'apprentissage automatique.")
        return

    if data.empty:
        st.warning("Aucun enregistrement dans cette sélection. Élargissez la période ou retirez un filtre.")
        return
    if page == "Vue d'ensemble":
        st.subheader("Une lecture descriptive d'une base historique")
        cols = st.columns(4)
        cols[0].metric("Enregistrements", fmt(stats['records']))
        cols[1].metric("Décès à bord déclarés", fmt(stats['fatalities']))
        cols[2].metric("Décès médians / ligne", f"{stats['median_fatalities']:.1f}")
        cols[3].metric("Survie sur lignes valides", f"{stats['survival_rate']:.1%}" if stats['survival_rate'] is not None else "Indisponible")
        st.caption(f"Survie : {fmt(stats['survival_records'])} lignes, {fmt(stats['survival_aboard'])} occupants. Couverture géographique résolue : {stats['geo_coverage']:.1%} de la sélection.")
        show(annual_figure(data, *years), "annual")
        st.subheader("Données de la sélection")
        st.dataframe(data[["source_row", "date", "country", "manufacturer", "aboard", "fatalities", "survival_rate"]].sort_values("date", ascending=False), hide_index=True)
        st.download_button("Exporter la sélection", data.to_csv(index=False).encode("utf-8-sig"), "selection_accidents.csv", "text/csv")
    elif page == "Évolution":
        show(annual_figure(data, *years), "annual")
        st.subheader("Survie par décennie")
        show(survival_figure(data), "survival")
        st.caption("Les données mélangent des types d'opérations différents, notamment des transports militaires et des accidents remarquables. Une évolution de composition peut modifier les indicateurs.")
    elif page == "Répartition":
        st.write(f"Pays identifiés : {fmt(data.country_iso3.ne('').sum())} / {fmt(len(data))} lignes. Les lieux non résolus restent dans les autres analyses.")
        if data.country_iso3.ne("").any():
            show(category_figure(data, "country"), "country")
        else:
            st.warning("Aucun pays résolu dans cette sélection.")
        show(category_figure(data, "manufacturer"), "manufacturer")
        st.caption("Le regroupement constructeur repose sur des préfixes explicites. Des modèles ou libellés mal extraits peuvent subsister. Le fichier ne sépare pas proprement aviation commerciale, militaire et générale.")
    elif page == "Gravité et survie":
        show(severity_figure(data), "severity")
        st.dataframe(data[["aboard", "fatalities", "ground"]].describe().round(2))
        if len(data[data.survival_valid]) >= 3:
            show(correlation_figure(data), "correlation")
        if data.year.between(1980, 1999).any() and data.year.between(2000, 2019).any():
            show(box_figure(data), "box")
    elif page == "Scénarios":
        mode = st.selectbox("Scénario à démontrer", ["Comparer deux périodes", "Traitement des données manquantes", "Hypothèse sur la gravité", "Monte-Carlo : collections fictives"])
        if mode == "Comparer deux périodes":
            st.write("Même durée de vingt ans. Les filtres pays et constructeur s'appliquent. Cette comparaison utilise ses propres périodes, indépendamment du curseur latéral.")
            results = []
            for label, bounds in [("1980–1999", (1980, 1999)), ("2000–2019", (2000, 2019))]:
                m = indicators(select_data(cleaned, bounds, countries, manufacturers))
                results.append({"Période": label, "Enregistrements": m['records'], "Décès à bord": m['fatalities'], "Décès médians": m['median_fatalities'], "Lignes valides survie": m['survival_records'], "Survie pondérée (%)": None if m['survival_rate'] is None else 100*m['survival_rate']})
            st.dataframe(pd.DataFrame(results), hide_index=True)
            st.caption("Ces différences ne mesurent pas le risque par vol. Le périmètre et la complétude de la base peuvent varier selon les périodes.")
        elif mode == "Traitement des données manquantes":
            st.write("Trois populations permettent de distinguer absence de valeur et libellé géographique inexploitable.")
            variants = [("Toutes les lignes préparées", data), ("Pays brut non manquant", data[data.country_raw.ne("")]), ("Pays résolu seulement", data[data.country_iso3.ne("")])]
            result = []
            for label, sample in variants:
                m = indicators(sample)
                result.append({"Règle": label, "Lignes": m['records'], "Décès à bord": m['fatalities'], "Survie pondérée (%)": None if m['survival_rate'] is None else 100*m['survival_rate']})
            st.dataframe(pd.DataFrame(result), hide_index=True)
            st.caption("Le changement de taux reflète le changement de population. Il ne prouve pas qu'une règle de nettoyage améliore la sécurité. Un pays renseigné peut quand même être non résolu.")
        elif mode == "Hypothèse sur la gravité":
            reduction = st.slider("Baisse relative hypothétique des décès à bord (%)", 0, 100, 10)
            result = severity_sensitivity(data, reduction / 100)
            st.warning("Hypothèse imposée, pas effet estimé d'une intervention. Occupants et nombre de lignes constants. Valeurs théoriques éventuellement non entières.")
            a, b, c = st.columns(3)
            a.metric("Décès observés (lignes valides)", fmt(result['observed_fatalities']))
            b.metric("Décès théoriques", f"{result['hypothetical_fatalities']:,.1f}")
            c.metric("Écart théorique", f"{result['hypothetical_difference']:,.1f}")
            st.code("décès_théoriques = décès_observés × (1 − réduction_relative)")
        else:
            st.write("Chaque répétition tire des lignes historiques avec remise dans la sélection. On tire occupants et décès ensemble pour conserver leur cohérence.")
            records = st.slider("Enregistrements fictifs par répétition", 1, 200, 50)
            repetitions = st.slider("Nombre de répétitions", 100, 3000, 1000, step=100)
            seed = st.number_input("Graine aléatoire", min_value=0, max_value=9999, value=42)
            valid_n = int(data.survival_valid.sum())
            st.caption(f"Base de tirage : {valid_n} lignes cohérentes. Avec remise signifie qu'une même ligne peut être tirée plusieurs fois.")
            if valid_n < 30:
                st.warning("Moins de 30 lignes de référence : la diversité simulée sera limitée.")
            if valid_n:
                results = simulate_burden(data, records, repetitions, int(seed))
                show(simulation_figure(results), "simulation")
                q = np.quantile(results.fatalities, [.05, .5, .95])
                st.dataframe(pd.DataFrame({"Statistique": ["Moyenne", "Écart-type", "Q05", "Médiane", "Q95"], "Décès fictifs": [results.fatalities.mean(), results.fatalities.std(ddof=0), *q]}), hide_index=True)
                st.warning("Simulation conditionnelle à un nombre imposé d'enregistrements. Aucune fréquence d'accident, indépendance causale ou prévision aéronautique n'est démontrée.")
                st.download_button("Exporter les répétitions simulées", results.to_csv(index=False).encode(), "simulation.csv", "text/csv")
            else:
                st.warning("Aucune ligne compatible avec le calcul de survie.")


if __name__ == "__main__":
    main()
