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
        """Инициализирует класс Vacancies_Controller
            Args: file_name(str): файл с вакансиями"""
        self.currency_values = pd.read_csv("currency.csv")

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

    def create_formatted_file(self,vacancy_file_name):
        """Создаёт отфильтрованный по зарплатам csv файл"""
        self.df = pd.read_csv(vacancy_file_name)
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
            return None
        if row['salary_currency'] == 'RUR':
            currency_value = 1
        else:
            current_date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
            currency_row = self.currency_values[self.currency_values['date'] == current_date.strftime('%Y-%m')]
            currency_value = currency_row.iloc[0][row['salary_currency']]
        if pd.isna(currency_value):
            return None
        if pd.isna(row['salary_from']):
            x = float(row['salary_to']) * currency_value
            return x
        if pd.isna(row['salary_to']):
            x = float(row['salary_from']) * currency_value
            return x
        else:
            x = (float(row['salary_to']) + float(row['salary_from'])) / 2 * currency_value
            return x

