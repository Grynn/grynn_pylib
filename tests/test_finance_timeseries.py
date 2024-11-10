import unittest
import pandas as pd
import numpy as np
from grynn_pylib.finance import timeseries

class TestTimeSeries(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame with a datetime index
        dates = pd.date_range(start='2020-01-01', periods=1000, freq='B')
        data = np.random.rand(1000) * 100
        self.df = pd.DataFrame(data, index=dates, columns=['price'])

    def test_rolling_cagr_normal_case(self):
        # Test the rolling CAGR with a normal case
        result = timeseries.rolling_cagr(self.df['price'])
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.df))

    def test_rolling_cagr_custom_window(self):
        # Test the rolling CAGR with a custom window
        window = 252 * 2  # 2 years
        result = timeseries.rolling_cagr(self.df['price'], window=window)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.df))

    def test_rolling_cagr_short_index_warning(self):
        # Test the rolling CAGR with a short index to trigger a warning
        short_df = self.df.iloc[:200]  # Less than 1 year of data
        with self.assertWarns(UserWarning):
            result = timeseries.rolling_cagr(short_df['price'])
            self.assertIsInstance(result, pd.Series)
            self.assertEqual(len(result), len(short_df))

    def test_rolling_cagr_edge_case(self):
        # Test the rolling CAGR with an edge case of exactly 1 year of data
        one_year_df = self.df.iloc[:252]  # Exactly 1 year of data
        result = timeseries.rolling_cagr(one_year_df['price'])
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(one_year_df))

    def test_rolling_cagr_zero_values(self):
        # Test the rolling CAGR with zero values in the data
        zero_data = np.zeros(1000)
        zero_df = pd.DataFrame(zero_data, index=self.df.index, columns=['price'])
        result = timeseries.rolling_cagr(zero_df['price'])
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(zero_df))
        self.assertTrue(result.isna().all())

if __name__ == "__main__":
    unittest.main()