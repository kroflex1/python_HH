import pandas as pd
from datetime import datetime
import numpy

from Currency_Controller import Currency_Controller


class Vacancies_Controller:
    """Класс, преобразует переданный dataframe, объединяя столбцы salary_from, salary_to и currency в один столбец salary .
             Attributes:
                df(dateframe): вакансии
                currency_values(dateframe): значения валют по месяцам
        """

    def __init__(self):
        """Инициализирует класс Vacancies_Controller"""
        self.df = pd.read_csv("vacancies_dif_currencies.csv")
        self.currency_values = pd.read_csv("currency.csv")

    def create_filtered_file(self):
        """Создаёт отфильтрованный по зарплатам csv файл"""
        currency_controller = Currency_Controller()
        self.df = currency_controller.filter_vacancies_by_currency(self.df)

        self.df['salary'] = self.df.apply(self.get_salary, axis=1)
        self.df = self.df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

        self.df.to_csv(rf"formated.csv", index=False)

    def get_salary(self, row):
        """Возвращает зарплату в зависимости от полей salary_from, salary_to, salary_currency
            Returns:
                float:зарплата
        """
        if (pd.isna(row['salary_from']) and pd.isna(row['salary_to'])) or pd.isna(row['salary_currency']):
            return numpy.nan
        if row['salary_currency'] == 'RUR':
            currency_value = 1
        else:
            current_date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
            currency_row = self.currency_values[self.currency_values['date'] == current_date.strftime('%Y-%m')]
            currency_value = currency_row.iloc[0][row['salary_currency']]
        if currency_value == 0:
            return numpy.nan
        if pd.isna(row['salary_from']):
            x = float(row['salary_to']) * currency_value
            return x
        if pd.isna(row['salary_to']):
            x = float(row['salary_from']) * currency_value
            return x
        else:
            x = (float(row['salary_to']) + float(row['salary_from'])) / 2 * currency_value
            return x



x = pd.read_csv('formated.csv')
x = x.head(100)
x.to_csv(rf"salary_info_100.csv", index=False)