"""Graphiques Matplotlib / Seaborn et justifications à afficher dans l'application."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from analyse import annual_table, survival_by_decade

BLUE, TEAL, ORANGE = "#174A78", "#168D99", "#C16C32"
sns.set_theme(style="whitegrid", font="DejaVu Sans", rc={
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#24384B", "text.color": "#10253F",
    "grid.alpha": 0.25, "figure.dpi": 130})


def annual_figure(d, start=None, end=None):
    a = annual_table(d, start, end)
    fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True, layout="constrained")
    axes[0].plot(a.year, a.records, color=BLUE, linewidth=2)
    axes[0].set(ylabel="Enregistrements", title="Évolution annuelle dans le fichier")
    axes[1].plot(a.year, a.fatalities, color=ORANGE, linewidth=2)
    axes[1].set(ylabel="Décès à bord déclarés", xlabel="Année")
    return fig


def category_figure(d, column="country", n=10):
    if column == "country":
        counts = d[d.country_iso3.ne("")].country.value_counts().head(n)
        title = "Pays identifiés : enregistrements les plus nombreux"
    else:
        counts = d.manufacturer.value_counts().head(n)
        title = "Constructeurs regroupés : enregistrements les plus nombreux"
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    counts.sort_values().plot.barh(ax=ax, color=TEAL)
    ax.set(title=title, xlabel="Nombre d'enregistrements", ylabel="")
    return fig


def severity_figure(d):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
    sns.histplot(data=d, x="fatalities", bins=35, color=BLUE, ax=axes[0])
    axes[0].set(title="Distribution des décès à bord", xlabel="Décès par enregistrement", ylabel="Effectif")
    sns.scatterplot(data=d[d.survival_valid], x="aboard", y="fatalities", s=15, alpha=.35, color=TEAL, ax=axes[1])
    max_x = max(1, d.aboard.max())
    axes[1].plot([0, max_x], [0, max_x], color=ORANGE, linestyle="--", linewidth=1)
    axes[1].set(title="Occupants et décès à bord", xlabel="Personnes à bord", ylabel="Décès à bord")
    return fig


def survival_figure(d):
    s = survival_by_decade(d)
    fig, ax = plt.subplots(figsize=(11, 4), layout="constrained")
    ax.bar(s.decade.astype(str), s.survival_rate * 100, color=TEAL)
    ax.set(title="Survie agrégée parmi les occupants recensés", ylabel="Survivants / occupants valides (%)", xlabel="Décennie de la sélection", ylim=(0, 100))
    ax.tick_params(axis="x", rotation=35)
    return fig


def box_figure(d):
    periods = d[d.year.between(1980, 2019)].copy()
    periods["period"] = np.where(periods.year < 2000, "1980–1999", "2000–2019")
    fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
    sns.boxplot(data=periods, x="period", y="fatalities", order=["1980–1999", "2000–2019"], color="#9FC4D7", ax=ax, fliersize=3)
    ax.set(title="Deux périodes de vingt ans", xlabel="Période", ylabel="Décès à bord par enregistrement")
    return fig


def correlation_figure(d):
    s = d[d.survival_valid][["year", "aboard", "fatalities"]].rename(columns={
        "year": "Année", "aboard": "Occupants", "fatalities": "Décès à bord"})
    fig, ax = plt.subplots(figsize=(7, 4.7), layout="constrained")
    sns.heatmap(s.corr(), annot=True, fmt=".2f", cmap="BrBG", vmin=-1, vmax=1, square=True, ax=ax)
    ax.set_title("Corrélations de Pearson sur les lignes valides")
    return fig


def simulation_figure(results):
    fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
    sns.histplot(results.fatalities, bins=35, color=TEAL, ax=ax)
    q05, q50, q95 = np.quantile(results.fatalities, [.05, .5, .95])
    for q, label in [(q05, "Q05"), (q50, "Médiane"), (q95, "Q95")]:
        ax.axvline(q, linestyle="--", linewidth=1.5, label=f"{label} : {q:,.0f}")
    ax.legend()
    ax.set(title="Distribution des totaux fictifs de décès à bord", xlabel="Décès à bord dans une répétition", ylabel="Nombre de répétitions")
    return fig


JUSTIFICATIONS = {
    "annual": "Les courbes montrent l'évolution chronologique. Deux panneaux séparent les unités. Les variations décrivent le fichier et ne mesurent pas le risque par vol.",
    "country": "Les barres horizontales facilitent la comparaison de catégories dont les noms sont longs. Les pays non résolus sont exclus du graphique et leur nombre reste affiché.",
    "manufacturer": "Les barres comparent des effectifs recensés. La taille des flottes et leur utilisation étant inconnues, ce graphique ne classe pas la sécurité des constructeurs.",
    "severity": "L'histogramme révèle la dissymétrie et les événements extrêmes. Le nuage de points relie occupants et décès à bord. La diagonale correspond à 100 % de décès à bord.",
    "survival": "Les barres représentent un taux pondéré : somme des survivants divisée par somme des occupants, sur les mêmes lignes valides. Les décennies aux extrémités de la sélection peuvent être partielles.",
    "box": "La boîte à moustaches compare les médianes, la dispersion centrale et les valeurs extrêmes sur deux périodes de même durée. Un point extrême ne constitue pas automatiquement une erreur.",
    "correlation": "La heatmap synthétise des associations linéaires. Le nombre de décès est structurellement lié au nombre d'occupants. La corrélation avec l'année n'établit aucun lien causal.",
    "simulation": "L'histogramme montre la variabilité de répétitions fictives. Q05 et Q95 bornent la partie centrale des simulations, sans constituer un intervalle de confiance ni une prévision.",
}
