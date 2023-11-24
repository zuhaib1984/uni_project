import unittest
import pandas as pd
from tradeapp.consumers import bollinger_band


class BollingerBandTestCase(unittest.TestCase):
    def test_bollinger_band_return_correct_bands(self):

        data = {
            'Open': [123, 120, 121, 123, 120, 121, 123, 120, 121],
            'High': [123, 125, 128, 123, 120, 121, 123, 120, 121],
            'Low': [120, 123, 125, 123, 120, 121, 123, 120, 121],
            'Close': [120, 121, 120, 123, 120, 121, 123, 120, 121],
        }
        df = pd.DataFrame(data)

        df = bollinger_band(df, 4, 4)



        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
