import math
import pandas as pd
import multiprocessing
import concurrent.futures
import os.path

from Separator import Separator


class StatisticalDataProcessor:
    """Класс для представления статистики по вакансиям.

    Attributes:
        dataset(list<Vacancy>): Список вакансий
        name_of_profession(str): Название вакансии, по которой будет полученя статистика
        average_salary(list<str>): Динамика уровня зарплат по годам
        average_salary_profession(list<str>): Динамика уровня зарплат по годам для выбранной профессии
        number_of_vacancies(list<str>): Динамика количества вакансий по годам
        number_of_vacancies_profession(list<str>): Динамика количества вакансий по годам для выбранной профессии
        salary_level(list<str>): Уровень зарплат по городам (в порядке убывания)
        vacancy_rate(list<str>):  Доля вакансий по городам (в порядке убывания)
        """

    def __init__(self):
        """Инициализирует объект StatisticalDataProcessor"""
        self.name_of_profession = None
        self.years = None
        self.folder_name = None
        self.main_df = None
        self.average_salary = {}
        self.number_of_vacancies = {}
        self.average_salary_profession = {}
        self.number_of_vacancies_profession = {}
        self.salary_level = {}
        self.vacancy_rate = {}

        self.region = None
        self.regions = None
        self.folder_regions_name = None
        self.average_salary_region = {}
        self.vacancy_rate_region = {}
        self.average_salary_profession_region = {}
        self.number_of_vacancies_profession_region = {}

    def initialize_statistics(self):
        """Собирает статистику по зарплаты по годам, количества вакансий по годам, зарплат по годам для выбранной профессии, количество вакансий по годам для выбранной профессии, уровень зарплат по городам, доля вакансий по городам"""
        file_name = input("Введите название файла: ")
        self.name_of_profession = input("Введите название профессии:  ")

        separator = Separator()
        separator.create_files_separated_by_years(file_name)
        self.years = list(separator.unique_years)
        self.folder_name = separator.folder_name
        self.main_df = separator.main_df

        self.average_salary = {}
        self.number_of_vacancies = {}
        self.average_salary_profession = {}
        self.number_of_vacancies_profession = {}
        self.initialize_year_statistics()

        self.salary_level = {}
        self.vacancy_rate = {}
        self.initialize_city_statistics()

    def initialize_statistics_by_region(self):
        """Собирает статистику по уровеню зарплат по городам, доли вакансий по городам, уровню зарплат по годам для выбранной профессии и региона, количества вакансий по годам для выбранной профессии и региона """
        file_name = input("Введите название файла: ")
        self.name_of_profession = input("Введите название профессии: ")
        self.region = input("Введите название региона: ")

        separator = Separator()
        separator.create_files_separated_by_years(file_name)
        self.years = list(separator.unique_years)
        self.folder_name = separator.folder_name
        self.main_df = separator.main_df

        self.salary_level = {}
        self.vacancy_rate = {}
        self.initialize_city_statistics()

        self.average_salary_profession_region = {}
        self.number_of_vacancies_profession_region = {}
        self.initialize_year_and_region_statistics()

    def print_statistic(self):
        """Выводит вcю имеющиеся статистику"""
        print(f'Динамика уровня зарплат по годам: {self.average_salary}')
        print(f'Динамика количества вакансий по годам: {self.number_of_vacancies}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {self.average_salary_profession}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {self.number_of_vacancies_profession}')
        print(f'Уровень зарплат по городам (в порядке убывания): {self.salary_level}')
        print(f'Доля вакансий по городам (в порядке убывания): {self.vacancy_rate}')

    def initialize_year_statistics(self):
        """Добавляет в словари статистик значения из файла
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            wait_complete = []
            for task in self.years:
                future = executor.submit(self.get_statistic_by_year, task)
                wait_complete.append(future)

        for res in concurrent.futures.as_completed(wait_complete):
            result = res.result()
            year = result[0]
            self.average_salary[year] = result[1]
            self.number_of_vacancies[year] = result[2]
            self.average_salary_profession[year] = result[3]
            self.number_of_vacancies_profession[year] = result[4]

        self.average_salary = dict(sorted(self.average_salary.items()))
        self.number_of_vacancies = dict(sorted(self.number_of_vacancies.items()))
        self.average_salary_profession = dict(sorted(self.average_salary_profession.items()))
        self.number_of_vacancies_profession = dict(sorted(self.number_of_vacancies_profession.items()))

    def get_statistic_by_year(self, year):
        """Возвращает статистку за год в порядке:
            Год,
            Среднее значение зарплаты за год,
            Количество вакансий за год.
            Среднее значение зарплаты за год для выбранной профессии.
            Количество вакансий за год для выбранной профессии
        """
        file_path = rf"{self.folder_name}\part_{year}.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df_vacancy = df[df["name"].str.contains(self.name_of_profession)]

            average_salary = math.floor(df["salary"].mean())
            number_of_vacancies = len(df.index)
            average_salary_profession = 0 if df_vacancy.empty else math.floor(df_vacancy["salary"].mean())
            number_of_vacancies_profession = 0 if df_vacancy.empty else len(df_vacancy.index)

            return [year, average_salary, number_of_vacancies, average_salary_profession,
                    number_of_vacancies_profession]

    def initialize_city_statistics(self):
        """Заполняет словари salary_level и vacancy_rate значениями"""
        pd.set_option('expand_frame_repr', False)
        df = self.main_df.copy(deep=True)
        df_length = len(df.index)

        df['count'] = df.groupby('area_name')['area_name'].transform('count')
        df = df[df['count'] / df_length >= 0.01]
        df_cities = df.groupby('area_name', as_index=False)['salary'].mean().sort_values(by='salary', ascending=False)
        df_cities['salary'] = df_cities['salary'].apply(lambda x: float(x))
        df_cities = df_cities.head(10)
        self.salary_level = dict(zip(df_cities['area_name'], df_cities['salary']))

        df['share'] = df['count'] / df_length
        df_share = df.groupby('area_name', as_index=False)['share'].mean().sort_values(by='share', ascending=False)
        df_share = df_share.head(10)
        self.vacancy_rate = dict(zip(df_share['area_name'], round(df_share['share'], 4)))

    def initialize_year_and_region_statistics(self):
        """Добавляет в словари статистик значения из файла
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            wait_complete = []
            for task in self.years:
                future = executor.submit(self.get_statistic_by_year_and_region, task)
                wait_complete.append(future)

        for res in concurrent.futures.as_completed(wait_complete):
            result = res.result()
            year = result[0]
            self.average_salary_profession_region[year] = result[1]
            self.number_of_vacancies_profession_region[year] = result[2]

        self.average_salary_profession_region = dict(sorted(self.average_salary_profession_region.items()))
        self.number_of_vacancies_profession_region = dict(sorted(self.number_of_vacancies_profession_region.items()))

    def get_statistic_by_year_and_region(self, year):
        """Возвращает статистку за год в порядке:
            Год,
            Среднее значение зарплаты за год в заданном регионе,
            Количество вакансий за год в заданном регионе.
        """
        file_path = rf"{self.folder_name}\part_{year}.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = df[(df["name"].str.contains(self.name_of_profession)) & (df["area_name"] == self.region)]

            average_salary = math.floor(df["salary"].mean())
            vacancy_rate = len(df.index)
            return [year, average_salary, vacancy_rate]

    def get_final_year_statistics(self):
        """Возвращает статистку по зарплате и количеству вакансий в словари
        Returns:
            list<dict<int,int>>: Список статистик по зарплате и количеству вакансий
        """
        return [self.average_salary,
                self.average_salary_profession,
                self.number_of_vacancies,
                self.number_of_vacancies_profession]

    def get_final_city_statistics(self):
        """Возвращает статистику по городам в словари
        Returns:
            list<dict<int,float>>: Список статистике по городам
        """
        return [self.salary_level,
                self.vacancy_rate]

    def get_final_region_statistics(self):
        """Конвертирует статистку по зарплате и количеству вакансий в словари
            Returns:
                list<dict<int,int>>: Список статистик по зарплате и количеству вакансий
        """
        return [self.average_salary_profession_region,
                self.number_of_vacancies_profession_region]

    def __convert_dictionary_to_list(self, dic):
        """Преобразует словарь в список
        Args:
            dict<int, string>: словарь
        Returns:
            list<str>: список
        """
        return ', '.join([f'{key}: {value}' for key, value in dic.items()])
