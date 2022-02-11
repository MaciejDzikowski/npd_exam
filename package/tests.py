import unittest
import pandas as pd

from package import parsers as pp
from package import functions as pf


class TestPackage(unittest.TestCase):
    def test_get_id(self):
        df = pd.DataFrame({
            'WT': ['02', '01', '02'],
            'GT': ['02', '02', '03']
        })
        self.assertListEqual(list(pp.get_id(df, ['WT', 'GT'])),
                             ['0202', '0102', '0203'])


if __name__ == 'main':
    new_test = TestPackage()
    new_test.test_get_id()
