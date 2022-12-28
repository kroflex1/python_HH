import pandas as pd
from datetime import datetime
import sqlite3

from Currency_Controller import Currency_Controller


class Vacancies_Controller:
    """Класс, преобразует переданный dataframe, объединяя столбцы salary_from, salary_to и currency в один столбец salary .
             Attributes:
                df(dateframe): вакансии
                currency_values(dateframe): значения валют по месяцам
        """

    def __init__(self):
        """Инициализирует класс Vacancies_Controller
            Args: file_name(str): файл с вакансиями"""
        self.currency_values = pd.read_csv("currency.csv")
        self.con = sqlite3.connect('currency_dynamic.sqlite')

    def get_formatted_dataframe(self, vacancies):
        """Возвращает dataframe с преобразованной зарлатой
           Args:
               vacancies(dataframe): вакансии
           Returns:
                 dataframe: вакансии со столбцом salary
        """
        currency_controller = Currency_Controller()
        vacancies = currency_controller.filter_vacancies_by_currency(vacancies)

        vacancies['salary'] = vacancies.apply(self.get_salary, axis=1)
        vacancies = vacancies.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

        return vacancies

    def create_formatted_file(self, vacancy_file_name):
        """Создаёт отфильтрованный по зарплатам csv файл"""
        self.df = pd.read_csv(vacancy_file_name)
        currency_controller = Currency_Controller()
        self.df = currency_controller.filter_vacancies_by_currency(self.df)

        self.df['salary'] = self.df.apply(self.get_salary, axis=1)
        self.df['published_at'] =  self.df.apply(
            lambda row: datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d'),
            axis=1)
        self.df = self.df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

        cursorObj = self.con.cursor()
        cursorObj.execute('CREATE TABLE IF NOT EXISTS salary_info (name text, salary float, area_name text, published_at date)')
        self.con.commit()
        self.df.to_sql('formatted', self.con, if_exists='replace', index=False)

    def get_salary(self, row):
        """Возвращает зарплату в зависимости от полей salary_from, salary_to, salary_currency
            Returns:
                float:зарплата
        """
        if (pd.isna(row['salary_from']) and pd.isna(row['salary_to'])) or pd.isna(row['salary_currency']):
            return None
        current_date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        currency_coefficient = self.get_currency_coefficient_from_db(row['salary_currency'],
                                                                     current_date.strftime('%Y-%m'))
        if not currency_coefficient:
            return None
        if pd.isna(row['salary_from']):
            x = float(row['salary_to']) * currency_coefficient
            return x
        if pd.isna(row['salary_to']):
            x = float(row['salary_from']) * currency_coefficient
            return x
        else:
            x = (float(row['salary_to']) + float(row['salary_from'])) / 2 * currency_coefficient
            return x

    def get_currency_coefficient_from_db(self, currency_name, current_date):
        """Получает коэффициент валлюты из базы данных
            Args:
                currency_name(str): название валюты
                current_date(str): текущая дата в формате  Y-m
            Returns:
                float: коэффициент валюты
        """
        if currency_name == 'RUR':
            return 1
        cursorObj = self.con.cursor()
        cursorObj.execute(f"SELECT {currency_name} FROM currency_dynamic WHERE date = '{current_date}'")
        rows = cursorObj.fetchall()
        for row in rows:
            return row[0]
