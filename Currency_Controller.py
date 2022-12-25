import requests
import pandas as pd
from datetime import datetime
from dateutil import rrule
from urllib.request import urlopen
import xml.etree.ElementTree as ET


class Currency_Controller:
    """Класс для создания csv файла с курсом фалют, основаным на полученном csv файле.

            Attributes:
                file_path(str): путь до csv файла
                df(dataframe): вакансии
                currencies(list<str>): список валют, втречающихся в файле вакансий более 5000 раз
        """
    def __init__(self):
        """Инициализирует класс Currency_Controller"""
        self.file_path = "vacancies_dif_currencies.csv"
        self.df = pd.read_csv(self.file_path)
        self.currencies = []

    def __initialize_currencies(self):
        """Заполняет список currencies валютами, которые встречаются более 5000 раз"""
        value = self.df['salary_currency'].value_counts()
        print(value)
        for currency, count in value.items():
            if count >= 5000 and currency !="RUR":
                self.currencies.append(currency)


    def __filter_vacancies_by_currency(self):
        """Фильтрует csv файл, оставляя лишь вакансии валюты которых встречаются более 5000 раз"""
        self.__initialize_currencies()
        self.df = self.df[self.df['salary_currency'].isin(self.currencies)]

    def filter_vacancies_by_currency(self, vacancies):
        """Фильтрует dataframe, оставляя лишь те вакансии валюты которых встречаются более 5000 раз
            Args:
                vacancies(dataframe): вакансии
            Returns:
                dataframe: отфильтрованные по валютам вакансии
        """
        value = vacancies['salary_currency'].value_counts()
        currencies = []
        for currency, count in value.items():
            if count >= 5000:
                currencies.append(currency)

        vacancies = vacancies[(vacancies['salary_currency'].isin(currencies)) | (pd.isna(vacancies['salary_currency']))]
        return vacancies


    def create_currency_dateframe(self):
        """Получает csv файл с инфомарцией о валютах по месяцам"""
        self.__filter_vacancies_by_currency()
        minDate = datetime.strptime(self.df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z').replace(day=12, hour=12, minute=0,
                                                                                            second=0)
        maxDate = datetime.strptime(self.df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z').replace(day=12, hour=12, minute=0,
                                                                                            second=0)
        result = {'date': []}
        for currency in self.currencies:
            result[currency] = []

        for current_date in rrule.rrule(rrule.MONTHLY, dtstart=minDate, until=maxDate):
            tree = ET.parse(
                urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=12/{current_date.strftime("%m/%Y")}d=1'))
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
                    result[currency].append(None)
        new_df = pd.DataFrame(result)
        new_df.to_csv(rf"currency.csv", index=False)




