"""Contrôles des risques réels : dénominateurs, anomalies, filtrage, simulation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest
import pandas as pd
import numpy as np
from analyse import load_raw, clean_data, indicators, select_data, resolve_country
from simulations import simulate_burden, severity_sensitivity


class TestMetier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw()
        cls.d = clean_data(cls.raw)

    def test_source_preserved_and_traceable(self):
        self.assertEqual(len(self.raw), len(self.d))
        self.assertEqual(self.d.source_row.tolist(), list(range(2, len(self.d)+2)))
        self.assertEqual(self.raw.columns.tolist()[0], 'Year')

    def test_survival_identity_and_bounds(self):
        v = self.d[self.d.survival_valid]
        self.assertTrue((v.survivors + v.fatalities == v.aboard).all())
        self.assertTrue(v.survival_rate.between(0, 1).all())
        self.assertTrue(self.d.loc[self.d.aboard.eq(0), 'survival_rate'].isna().all())

    def test_weighted_rate_not_mean_of_rates(self):
        d = self.d[self.d.survival_valid].head(2).copy()
        d['aboard'] = [10, 100]
        d['fatalities'] = [0, 100]
        d['survivors'] = [10, 0]
        self.assertAlmostEqual(indicators(d)['survival_rate'], 10/110)

    def test_ambiguous_geography_not_guessed(self):
        for value in ['New', 'South', 'Georgia', 'Congo', 'Victoria', '']:
            self.assertEqual(resolve_country(value)[0], '')
        self.assertEqual(resolve_country('California')[0], 'USA')
        self.assertEqual(resolve_country(' France ')[0], 'FRA')

    def test_invalid_and_future_date_excluded(self):
        r = self.raw.head(2).copy()
        r.loc[r.index[0], ['Year','Month','Day']] = [2025,'February',30]
        r.loc[r.index[1], ['Year','Month','Day']] = [2099,'January',1]
        self.assertFalse(clean_data(r).analysis_valid.any())

    def test_filter_and_empty_population(self):
        d = select_data(self.d, (1980,1999))
        self.assertTrue(d.year.between(1980,1999).all())
        empty = select_data(self.d, (1800,1801))
        self.assertEqual(indicators(empty)['records'], 0)
        self.assertIsNone(indicators(empty)['survival_rate'])

    def test_simulation_consistency_and_seed(self):
        a = simulate_burden(self.d, 30, 100, 42)
        b = simulate_burden(self.d, 30, 100, 42)
        pd.testing.assert_frame_equal(a,b)
        self.assertTrue((a.fatalities <= a.aboard).all())
        self.assertTrue((a.survivors + a.fatalities == a.aboard).all())
        with self.assertRaises(ValueError):
            simulate_burden(self.d.iloc[:0])

    def test_sensitivity_boundaries(self):
        baseline = severity_sensitivity(self.d, 0)
        zero = severity_sensitivity(self.d, 1)
        self.assertEqual(baseline['observed_fatalities'], baseline['hypothetical_fatalities'])
        self.assertEqual(zero['hypothetical_fatalities'], 0)
        self.assertEqual(zero['hypothetical_survival_rate'], 1)


if __name__ == '__main__':
    unittest.main()
