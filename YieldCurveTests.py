import unittest
from YieldCurve import yieldcurve_data, get_day_partially_inverted, get_day_fully_inverted, get_year_specific_url

class TestYieldCurve(unittest.TestCase):
    def get_2017_test_website_data(self):
        # TODO replace this with hard-coded data, instead of hitting the US Treasury API
        website = get_year_specific_url("2017")
        website_data, new_column = yieldcurve_data(website)
        return website_data

    def test_partial_invert_2017(self):
        website_data = self.get_2017_test_website_data()
        day_partially_inverted = get_day_partially_inverted(website_data)
        self.assertEqual(1, day_partially_inverted)

    def test_full_invert_2017(self):
        website_data = self.get_2017_test_website_data()
        day_fully_inverted = get_day_fully_inverted(website_data)
        self.assertEqual(5, day_fully_inverted)
