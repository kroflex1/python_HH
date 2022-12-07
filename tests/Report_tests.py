import unittest
from main import Report

class MyTestCase(unittest.TestCase):
    def test_format_city_1(self):
        self.assertEqual('Санкт\nПетербург', Report.format_city('Санкт-Петербург'))
    def test_format_city_2(self):
        self.assertEqual('Санкт\nПетербург', Report.format_city('Санкт - Петербург'))
    def test_format_city_3(self):
        self.assertEqual('Санкт\nПетербург', Report.format_city('Санкт Петербург'))
