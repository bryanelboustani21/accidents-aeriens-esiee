"""Lecture, nettoyage et indicateurs. Aucun fichier source n'est modifié.

Les règles sont explicites pour pouvoir être expliquées pendant l'oral.
Une ligne désigne un enregistrement du fichier, pas nécessairement un événement unique.
"""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "raw" / "aircrashesFullData.csv"
AS_OF = pd.Timestamp("2026-11-06")
MONTHS = {m: i + 1 for i, m in enumerate([
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"])}
COLS = {"Year": "year", "Quarter": "quarter_raw", "Month": "month_raw",
        "Day": "day", "Country/Region": "country_raw",
        "Aircraft Manufacturer": "manufacturer_raw", "Aircraft": "aircraft",
        "Location": "location", "Operator": "operator", "Ground": "ground",
        "Fatalities (air)": "fatalities", "Aboard": "aboard"}

# Rapprochements exacts. Aucun rapprochement approximatif de pays n'est utilisé.
ALIASES = {
    "russia": "RUS", "iran": "IRN", "syria": "SYR", "laos": "LAO",
    "vietnam": "VNM", "taiwan": "TWN", "south korea": "KOR",
    "south sudan": "SSD", "moldova": "MDA", "bolivia": "BOL",
    "venezuela": "VEN", "tanzania": "TZA", "brunei": "BRN",
    "england": "GBR", "scotland": "GBR", "us": "USA", "u.s.": "USA",
    "burma": "MMR", "surinam": "SUR", "curacao": "CUW",
    "bosnia-herzegovina": "BIH", "cape verde": "CPV",
    "afghanstan": "AFG", "aregntina": "ARG", "australila": "AUS",
    "baangladesh": "BGD", "boliva": "BOL", "bugaria": "BGR",
    "bulgeria": "BGR", "djbouti": "DJI", "hati": "HTI",
    "hunary": "HUN", "inodnesia": "IDN", "jamacia": "JAM",
    "kazakastan": "KAZ", "kazakstan": "KAZ", "manmar": "MMR",
    "mauretania": "MRT", "mexic": "MEX", "morroco": "MAR",
    "nambia": "NAM", "napal": "NPL", "philipines": "PHL",
    "philippine": "PHL", "phillipines": "PHL", "uzbekstan": "UZB",
    "cameroons": "CMR", "guadaloupe": "GLP",
}
US_STATES = "Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada Ohio Oklahoma Oregon Pennsylvania Tennessee Texas Utah Vermont Virginia Washington Wisconsin Wyoming".split()
# Les noms en plusieurs mots et Georgia restent ambigus dans ce fichier tronqué.
CANADA_PROVINCES = ["Alberta", "Manitoba", "Ontario", "Quebec", "Saskatchewan", "Yukon", "Nunavut", "Labrador"]
AUSTRALIA_STATES = ["Queensland", "Tasmania"]
REGION_ALIASES = {**{x.casefold(): "USA" for x in US_STATES},
                  **{x.casefold(): "CAN" for x in CANADA_PROVINCES},
                  **{x.casefold(): "AUS" for x in AUSTRALIA_STATES}}
AMBIGUOUS = {"georgia", "congo", "victoria"}
ISO_NAMES = {}
COUNTRY_NAMES = {}
# Petit fichier de référence fourni. Pas de bibliothèque géographique à installer.
for row in pd.read_csv(ROOT / "data/reference/iso_countries.csv").to_dict("records"):
    ISO_NAMES[row["name"].casefold()] = row["iso3"]
    COUNTRY_NAMES[row["iso3"]] = row["canonical_name"]


def text_clean(value):
    """Uniformise seulement les espaces, sans réordonner les mots."""
    if pd.isna(value):
        return ""
    return " ".join(str(value).split())


def resolve_country(value):
    """Retourne code ISO, libellé et règle. Les ambiguïtés restent visibles."""
    value = text_clean(value)
    key = value.casefold()
    if not key:
        return "", "Non renseigné", "manquant"
    if key in AMBIGUOUS:
        return "", "Non résolu", "ambigu"
    code = ISO_NAMES.get(key)
    status = "nom ISO exact"
    if not code and key in ALIASES:
        code, status = ALIASES[key], "alias explicite"
    if not code and key in REGION_ALIASES:
        code, status = REGION_ALIASES[key], "région explicite"
    if code:
        return code, COUNTRY_NAMES[code], status
    return "", "Non résolu", "non résolu"


MANUFACTURERS = ["McDonnell Douglas", "de Havilland Canada", "de Havilland", "Lockheed", "Boeing", "Douglas", "Airbus", "Antonov", "Ilyushin", "Tupolev", "Fokker", "Curtiss", "Junkers", "Convair", "Fairchild", "Sikorsky", "Cessna", "Embraer", "Beechcraft", "Piper", "Avro", "ATR", "Vickers", "Dornier", "Bristol", "Bell", "Grumman", "Saab"]


def manufacturer_family(value):
    """Regroupe des préfixes explicites, sans estimer le constructeur inconnu."""
    value = text_clean(value)
    if not value or value.startswith("?"):
        return "Non identifié"
    if " / " in value:
        return "Plusieurs constructeurs / à vérifier"
    if value.casefold().startswith("doublas") or value.casefold().startswith("douglass"):
        return "Douglas"
    if value.casefold().startswith("antonv"):
        return "Antonov"
    for family in MANUFACTURERS:
        if value.casefold().startswith(family.casefold()):
            return family
    return value


def load_raw(path=SOURCE):
    data = pd.read_csv(path)
    missing = set(COLS) - set(data.columns)
    if missing:
        raise ValueError(f"Colonnes absentes : {sorted(missing)}")
    return data


def clean_data(raw):
    """Conserve les anomalies et ajoute des drapeaux plutôt que d'inventer des valeurs."""
    d = raw.rename(columns=COLS).copy()
    d.insert(0, "source_row", np.arange(len(d)) + 2)
    duplicate = raw.duplicated(keep="first")
    d["duplicate_exact"] = duplicate.to_numpy()
    for col in ["quarter_raw", "month_raw", "country_raw", "manufacturer_raw", "aircraft", "location", "operator"]:
        d[col] = d[col].map(text_clean)
    d["operator_missing"] = d["operator"].eq("")
    d["operator"] = d["operator"].replace("", "Non renseigné")
    for col in ["year", "day", "ground", "fatalities", "aboard"]:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    d["month"] = d["month_raw"].map(MONTHS)
    d["date"] = pd.to_datetime(d[["year", "month", "day"]], errors="coerce")
    d["date_valid"] = d["date"].notna() & d["date"].le(AS_OF)
    d["quarter"] = d["date"].dt.quarter
    d["quarter_mismatch"] = d["quarter_raw"].ne("Qtr " + d["quarter"].astype("Int64").astype(str))
    geo = d["country_raw"].map(resolve_country)
    d[["country_iso3", "country", "geo_status"]] = pd.DataFrame(geo.tolist(), index=d.index)
    d["manufacturer"] = d["manufacturer_raw"].map(manufacturer_family)
    numeric = d[["fatalities", "aboard", "ground"]]
    d["counts_valid"] = numeric.notna().all(axis=1) & numeric.ge(0).all(axis=1) & numeric.mod(1).eq(0).all(axis=1)
    d["fatalities_exceed_aboard"] = d["fatalities"].gt(d["aboard"])
    # Les zéros d'occupation ne sont pas remplacés. Ils excluent le calcul de survie.
    d["survival_valid"] = d["counts_valid"] & d["aboard"].gt(0) & ~d["fatalities_exceed_aboard"]
    d["survivors"] = np.nan
    d["survival_rate"] = np.nan
    ok = d["survival_valid"]
    d.loc[ok, "survivors"] = d.loc[ok, "aboard"] - d.loc[ok, "fatalities"]
    d.loc[ok, "survival_rate"] = d.loc[ok, "survivors"] / d.loc[ok, "aboard"]
    d["analysis_valid"] = d["date_valid"] & d["counts_valid"] & ~d["duplicate_exact"]
    d["decade"] = (d["year"] // 10 * 10).astype("Int64")
    return d


def audit_data(raw, cleaned):
    d = cleaned
    return {
        "raw_rows": len(raw), "raw_columns": len(raw.columns),
        "year_min": int(d.year.min()), "year_max": int(d.year.max()),
        "date_min": str(d.date.min().date()), "date_max": str(d.date.max().date()),
        "missing_country": int(d.country_raw.eq("").sum()),
        "missing_operator": int(d.operator_missing.sum()),
        "exact_duplicates": int(d.duplicate_exact.sum()),
        "invalid_dates": int((~d.date_valid).sum()),
        "quarter_mismatches": int(d.quarter_mismatch.sum()),
        "invalid_counts": int((~d.counts_valid).sum()),
        "zero_aboard": int(d.aboard.eq(0).sum()),
        "fatalities_exceed_aboard": int(d.fatalities_exceed_aboard.sum()),
        "survival_excluded": int((~d.survival_valid).sum()),
        "geography_resolved": int(d.country_iso3.ne("").sum()),
        "geography_unresolved": int(d.country_iso3.eq("").sum()),
        "analysis_rows": int(d.analysis_valid.sum()),
        "survival_rows": int((d.analysis_valid & d.survival_valid).sum()),
        "manufacturer_changed": int(d.manufacturer.ne(d.manufacturer_raw).sum()),
    }


def select_data(d, years=None, countries=None, manufacturers=None, survival_only=False):
    mask = d.analysis_valid.copy()
    if years is not None:
        mask &= d.year.between(*years)
    if countries:
        mask &= d.country.isin(countries)
    if manufacturers:
        mask &= d.manufacturer.isin(manufacturers)
    if survival_only:
        mask &= d.survival_valid
    return d.loc[mask].copy()


def indicators(d):
    """Un taux pondéré utilise uniquement des numérateurs/dénominateurs appariés."""
    s = d[d.survival_valid]
    denominator = s.aboard.sum()
    return {"records": len(d), "fatalities": int(d.fatalities.sum()),
            "median_fatalities": float(d.fatalities.median()) if len(d) else None,
            "survival_records": len(s), "survival_aboard": int(denominator),
            "survival_fatalities": int(s.fatalities.sum()),
            "survivors": int(s.survivors.sum()),
            "survival_rate": float(s.survivors.sum() / denominator) if denominator > 0 else None,
            "geo_coverage": float(d.country_iso3.ne("").mean()) if len(d) else None}


def annual_table(d, start=None, end=None):
    if d.empty and (start is None or end is None):
        return pd.DataFrame(columns=["year", "records", "fatalities"])
    lo = int(d.year.min()) if start is None else start
    hi = int(d.year.max()) if end is None else end
    # Un zéro signifie « aucun enregistrement dans ce fichier », pas zéro accident réel.
    return d.groupby("year").agg(records=("source_row", "size"), fatalities=("fatalities", "sum")).reindex(range(lo, hi + 1), fill_value=0).rename_axis("year").reset_index()


def survival_by_decade(d):
    s = d[d.survival_valid]
    out = s.groupby("decade").agg(records=("source_row", "size"), aboard=("aboard", "sum"), survivors=("survivors", "sum"))
    out["survival_rate"] = out.survivors / out.aboard
    return out.reset_index()


def source_sha256(path=SOURCE):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
