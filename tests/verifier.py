"""Vérifications reproductibles, à lancer depuis le dossier du projet."""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import charger_donnees, calculer_indicateurs

brut, df = charger_donnees()
assert brut.shape == (5052, 12)
assert len(df) == 5017 and df["Year"].between(1908, 2023).all()
assert list(brut.columns) == ["Year", "Quarter", "Month", "Day", "Country/Region",
                             "Aircraft Manufacturer", "Aircraft", "Location", "Operator",
                             "Ground", "Fatalities (air)", "Aboard"]

valides, deces, survie, sans_deces = calculer_indicateurs(df)
assert deces == 111686 and len(valides) == 4995
assert valides["Aboard"].sum() == 155827
assert valides["Survivants"].sum() == 44214
assert np.isclose(survie, 100 * 44214 / 155827)
assert np.isclose(sans_deces, 100 * 86 / 5017)
assert (valides["Survivants"] + valides["Fatalities (air)"] == valides["Aboard"]).all()

boeing = df[(df["Constructeur"] == "Boeing") & (df["Modele"] == "Boeing 737")]
assert len(boeing) == 102 and boeing["Fatalities (air)"].sum() == 5806
assert len(boeing[boeing["Year"].between(1908, 1909)]) == 0
transaviaexport = df["Operator"].str.contains("Transaviaexport", case=False, na=False)
assert df.loc[transaviaexport, "Operateur"].str.contains("Transaviaexport", case=False).all()
assert not df.loc[transaviaexport, "Operateur"].eq("Transavia").any()

# Un taux global doit pondérer par les personnes, pas par le nombre de lignes.
exemple = pd.DataFrame({"Aboard": [10, 100, 0, 1], "Fatalities (air)": [0, 100, 0, 2]})
v, d, s, z = calculer_indicateurs(exemple)
assert len(v) == 2 and np.isclose(s, 100 * 10 / 110)
assert d == 102 and z == 50
assert np.isnan(calculer_indicateurs(exemple.iloc[0:0])[2])
assert np.isnan(calculer_indicateurs(exemple.iloc[2:4])[2])
inconnus = pd.DataFrame({"Aboard": [10], "Fatalities (air)": [np.nan]})
assert all(np.isnan(x) for x in calculer_indicateurs(inconnus)[1:])

print("Vérifications réussies : CSV, périmètre, regroupements, taux et cas limites.")
