"""Reproduire le nettoyage, les statistiques, les tableaux et les figures hors interface."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analyse import ROOT, SOURCE, load_raw, clean_data, audit_data, select_data, indicators, annual_table, survival_by_decade, source_sha256
from simulations import simulate_burden, severity_sensitivity
from graphiques import annual_figure, category_figure, severity_figure, survival_figure, box_figure, correlation_figure, simulation_figure


def main():
    raw = load_raw()
    cleaned = clean_data(raw)
    audit = audit_data(raw, cleaned)
    data = select_data(cleaned, (1908, 2025))
    stats = indicators(data)
    out = ROOT / 'outputs'
    figs = out / 'figures'
    figs.mkdir(parents=True, exist_ok=True)
    (ROOT / 'data/processed').mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(ROOT / 'data/processed/accidents_prepares.csv', index=False)
    cleaned.loc[~cleaned.survival_valid].to_csv(out / 'anomalies_survie.csv', index=False)
    cleaned[['country_raw','country','country_iso3','geo_status']].drop_duplicates().sort_values('country_raw').to_csv(out / 'correspondance_pays.csv', index=False)
    annual_table(data, 1908, 2025).to_csv(out / 'evolution_annuelle.csv', index=False)
    survival_by_decade(data).to_csv(out / 'survie_decennies.csv', index=False)
    data[['aboard','fatalities','ground']].describe().to_csv(out / 'statistiques_descriptives.csv')
    comparison = []
    for label, bounds in [('1980–1999',(1980,1999)), ('2000–2019',(2000,2019))]:
        comparison.append({'period':label, **indicators(select_data(cleaned,bounds))})
    pd.DataFrame(comparison).to_csv(out / 'comparaison_periodes.csv', index=False)
    quality_comparison = []
    for label, sample in [('Toutes les lignes', data), ('Pays brut renseigné', data[data.country_raw.ne('')]), ('Pays résolu seulement', data[data.country_iso3.ne('')])]:
        quality_comparison.append({'rule': label, **indicators(sample)})
    pd.DataFrame(quality_comparison).to_csv(out / 'comparaison_nettoyage.csv', index=False)
    sensitivity = []
    for reduction in [0, .1, .2, .3]:
        sensitivity.append({'reduction':reduction, **severity_sensitivity(data,reduction)})
    pd.DataFrame(sensitivity).to_csv(out / 'sensibilite.csv',index=False)
    sim = simulate_burden(data, records=50, repetitions=1000, seed=42)
    sim.to_csv(out / 'simulation_reference.csv', index=False)
    simstats = {'records':50,'repetitions':1000,'seed':42, 'pool':int(data.survival_valid.sum()),
                'mean':float(sim.fatalities.mean()),'std_population':float(sim.fatalities.std(ddof=0)),
                'q05':float(np.quantile(sim.fatalities,.05)), 'q50':float(np.quantile(sim.fatalities,.5)), 'q95':float(np.quantile(sim.fatalities,.95))}
    geo = data[data.country_iso3.ne('')].country.value_counts().head(10)
    manufacturers = data.manufacturer.value_counts().head(10)
    decade = survival_by_decade(data)
    # Invariants utiles et indépendants des nombres actuellement présents dans le fichier.
    assert len(raw) == len(cleaned)
    assert 0 <= stats['survival_rate'] <= 1
    assert stats['survivors'] + stats['survival_fatalities'] == stats['survival_aboard']
    assert annual_table(data).records.sum() == len(data)
    assert (sim.survivors + sim.fatalities == sim.aboard).all()
    payload = {'source_sha256':source_sha256(), 'source_bytes':SOURCE.stat().st_size,
               'audit':audit, 'scope':'1908–2025, années calendaires hors année 2026 partielle',
               'indicators':stats, 'periods':comparison, 'cleaning_comparison':quality_comparison, 'simulation':simstats,
               'top_countries':geo.to_dict(), 'top_manufacturers':manufacturers.to_dict(),
               'decades':decade.to_dict('records'),
               'geo_status':cleaned.geo_status.value_counts().to_dict()}
    (out / 'resultats.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    charts = {
        '01_evolution':annual_figure(data,1908,2025),
        '02_pays':category_figure(data,'country'),
        '03_constructeurs':category_figure(data,'manufacturer'),
        '04_gravite':severity_figure(data),
        '05_survie':survival_figure(data),
        '06_comparaison':box_figure(data),
        '07_correlations':correlation_figure(data),
        '08_simulation':simulation_figure(sim),
    }
    for name, fig in charts.items():
        fig.savefig(figs / (name+'.png'),dpi=180,facecolor='white')
        plt.close(fig)
    print(json.dumps(payload,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
