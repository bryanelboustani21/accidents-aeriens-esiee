"""Simulations pédagogiques conditionnelles aux accidents déjà recensés.

Aucune fréquence d'accident par vol et aucun effet causal ne sont estimés.
"""
import numpy as np
import pandas as pd


def simulate_burden(data, records=50, repetitions=1000, seed=42):
    """Tire des lignes entières avec remise et préserve le lien occupants/décès.

    Chaque répétition contient exactement `records` enregistrements fictifs.
    Les quantiles décrivent ces répétitions, pas un intervalle de confiance.
    """
    if not 1 <= records <= 500 or not 1 <= repetitions <= 5000:
        raise ValueError("Nombre de lignes : 1..500 ; répétitions : 1..5000.")
    valid = data.loc[data.survival_valid, ["aboard", "fatalities"]].to_numpy(dtype=float)
    if not len(valid):
        raise ValueError("Aucune ligne compatible avec une simulation de survie.")
    # Même générateur que dans test.py fourni avec les supports du cours.
    rng = np.random.RandomState(seed)
    chosen = rng.randint(0, len(valid), size=(repetitions, records))
    draws = valid[chosen]
    aboard = draws[:, :, 0].sum(axis=1)
    fatalities = draws[:, :, 1].sum(axis=1)
    survivors = aboard - fatalities
    return pd.DataFrame({"repetition": np.arange(1, repetitions + 1),
                         "aboard": aboard.astype(int), "fatalities": fatalities.astype(int),
                         "survivors": survivors.astype(int), "survival_rate": survivors / aboard})


def severity_sensitivity(data, reduction=0.10):
    """Une baisse relative imposée des décès, à nombre d'occupants constant."""
    if not 0 <= reduction <= 1:
        raise ValueError("La réduction relative doit appartenir à [0, 1].")
    d = data.loc[data.survival_valid]
    fatalities = float(d.fatalities.sum())
    aboard = float(d.aboard.sum())
    simulated = fatalities * (1 - reduction)
    return {"aboard": aboard, "observed_fatalities": fatalities,
            "hypothetical_fatalities": simulated,
            "hypothetical_difference": fatalities - simulated,
            "hypothetical_survival_rate": (aboard - simulated) / aboard if aboard else None}
