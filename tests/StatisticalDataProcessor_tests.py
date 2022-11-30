import unittest
from Program import StatisticalDataProcessor


class MyTestCase(unittest.TestCase):
    def test_convert_city_statistic_to_dictionary(self):
        statistics = ["'Казань': 156337", "'Москва': 142291", "'Санкт-Петербург': 111548", "'Уфа': 106750",
                      "'Ташкент': 101797", "'Екатеринбург': 95270", "'Владивосток': 87916", "'Набережные Челны': 81142",
                      "'Иркутск': 80357", "'Нижний Новгород': 74437"]
        result = {'Казань': 156337.0, 'Москва': 142291.0, 'Санкт-Петербург': 111548.0, 'Уфа': 106750.0,
                  'Ташкент': 101797.0, 'Екатеринбург': 95270.0, 'Владивосток': 87916.0, 'Набережные Челны': 81142.0,
                  'Иркутск': 80357.0, 'Нижний Новгород': 74437.0}
        self.assertEqual(result, StatisticalDataProcessor.convert_city_statistic_to_dictionary(statistics))

    def test_convert_year_statistic_to_dictionary(self):
        statistics = ['2019: 146789', '2022: 204316']
        result = {2019: 146789, 2022: 204316}
        self.assertEqual(result, StatisticalDataProcessor.convert_year_statistic_to_dictionary(statistics))
