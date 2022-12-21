import requests
import pandas as pd
from datetime import datetime
from dateutil.rrule import *
from urllib.request import urlopen
import xml.etree.ElementTree as ET


class Currency_Controller:
    def __init__(self):
        self.file_path = "vacancies_dif_currencies.csv"
        self.df = pd.read_csv(self.file_path)
        self.currencies = []
        self.get_currency_dateframe()

    def initialize_currencies(self):
        """Заполняет список currencies валютами, которые встречаются более 5000 раз"""
        value = self.df['salary_currency'].value_counts()
        print(value)
        for currency, count in value.items():
            if count >= 5000 and currency !="RUR":
                self.currencies.append(currency)


    def filter_file(self):
        """Фильтрует csv файл, оставляя лишь вакансии валюты которых встречаются более 5000 раз"""
        self.initialize_currencies()
        self.df = self.df[self.df['salary_currency'].isin(self.currencies)]

    def get_currency_dateframe(self):
        """Получает csv файл с инфомарцией о валютах по месяцам"""
        self.filter_file()
        minDate = datetime.strptime(self.df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z')
        maxDate = datetime.strptime(self.df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z')
        result = {'date': []}
        for currency in self.currencies:
            result[currency] = []

        for current_date in rrule(MONTHLY, dtstart=minDate, until=maxDate):
            tree = ET.parse(
                urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{current_date.strftime("%m/%Y")}d=1'))
            root = tree.getroot()
            for child in root.findall('Valute'):
                currency = child.find('CharCode').text
                if currency in result.keys():
                    if current_date.strftime('%Y-%m') not in result['date']:
                        result['date'] += [current_date.strftime('%Y-%m')]
                    currency_exchange_rate = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
                    result[currency].append(currency_exchange_rate)
            #Проверяем, значение валюты на пустоту
            for currency in self.currencies:
                if len(result[currency]) !=len(result['date']):
                    result[currency].append(0)
        new_df = pd.DataFrame(result)
        new_df.to_csv(rf"test.csv", index=False)


x = Currency_Controller()
