import csv
import re
import sys
import math
import prettytable
from prettytable import PrettyTable

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

    def __init__(self, dataset):
        """Инициализирует объект StatisticalDataProcessor

        Args:
            dataset(list<Vacancy>): Список вакансий
        """
        self.dataset = dataset
        self.name_of_profession = dataset.name_of_profession

        self.average_salary = self.get_salary_statistics()
        self.average_salary_profession = self.get_salary_statistics(self.name_of_profession)
        self.number_of_vacancies = self.get_number_of_vacancies_statistics()
        self.number_of_vacancies_profession = self.get_number_of_vacancies_statistics(self.name_of_profession)
        self.salary_level = self.get_salary_level_city_statistics()
        self.vacancy_rate = self.get_number_of_vacancies_city_statistics()

    def print_statistic(self):
        """Выводит свю имеющиеся статистику"""
        print('Динамика уровня зарплат по годам: {' + ', '.join(self.average_salary) + '}')
        print('Динамика количества вакансий по годам: {' + ', '.join(self.number_of_vacancies) + '}')
        print('Динамика уровня зарплат по годам для выбранной профессии: {' + ', '.join(
            self.average_salary_profession) + '}')
        print('Динамика количества вакансий по годам для выбранной профессии: {' + ', '.join(
            self.number_of_vacancies_profession) + '}')
        print('Уровень зарплат по городам (в порядке убывания): {' + ', '.join(self.salary_level) + '}')
        print('Доля вакансий по городам (в порядке убывания): {' + ', '.join(self.vacancy_rate) + '}')

    def get_final_year_statistics(self):
        """Конвертирует статистку по зарплате и количеству вакансий в словари
        Returns:
            list<dict<int,int>>: Список статистик по зарплате и количеству вакансий
        """
        return [self.convert_year_statistic_to_dictionary(self.average_salary),
                self.convert_year_statistic_to_dictionary(self.average_salary_profession),
                self.convert_year_statistic_to_dictionary(self.number_of_vacancies),
                self.convert_year_statistic_to_dictionary(self.number_of_vacancies_profession)]

    def get_final_city_statistics(self):
        """Конвертирует статистику по городам в словари
        Returns:
            list<dict<int,float>>: Список статистике по городам
        """
        return [self.convert_city_statistic_to_dictionary(self.salary_level),
                self.convert_city_statistic_to_dictionary(self.vacancy_rate)]

    def get_salary_statistics(self, name_of_profession=""):
        """ Возвращает динамику уровня зарплат по годам, если не передан аргумент name_of_profession.
            Возвращает динамику уровня зарплат по годам для профессии, если передан аргумент name_of_profession.
         Args:
             name_of_profession(str): Название вакансии, по которйо нужно получить статистику
         Returns:
            list<str>: Статистика по уровню зарплат по годам
        """
        salary_statistics = []
        current_year = self.dataset.vacancies_objects[0].published_at.year
        average_salary = 0
        number_of_vacancies = 0
        for vacancy in self.dataset.vacancies_objects:
            if vacancy.published_at.year != current_year and (
                    name_of_profession == "" or name_of_profession in vacancy.name):
                if number_of_vacancies == 0:
                    salary_statistics.append(f'{current_year}: {0}')
                else:
                    salary_statistics.append(f'{current_year}: {math.floor(average_salary / number_of_vacancies)}')
                current_year = vacancy.published_at.year
                average_salary = vacancy.salary.average
                number_of_vacancies = 1
            elif name_of_profession == "" or name_of_profession in vacancy.name:
                average_salary += vacancy.salary.average
                number_of_vacancies += 1
        if number_of_vacancies == 0:
            salary_statistics.append(f'{current_year}: {0}')
        else:
            salary_statistics.append(f'{current_year}: {math.floor(average_salary / number_of_vacancies)}')
        return salary_statistics

    def get_number_of_vacancies_statistics(self, name_of_profession=""):
        """ Возвращает динамику количества вакансий по годам, если не передан аргумент name_of_profession.
            Возвращает динамику уровня зарплат по годам для профессии, если передан аргумент name_of_profession.
        Args:
            name_of_profession(str): Название вакансии, по которйо нужно получить статистику
        Returns:
            list<str>: Статистика по количеству вакансий
        """
        number_of_vacancies_statistics = []
        current_year = self.dataset.vacancies_objects[0].published_at.year
        number_of_vacancies = 0
        for vacancy in self.dataset.vacancies_objects:
            if vacancy.published_at.year != current_year and (
                    name_of_profession == "" or name_of_profession in vacancy.name):
                number_of_vacancies_statistics.append(f'{current_year}: {number_of_vacancies}')
                current_year = vacancy.published_at.year
                number_of_vacancies = 1
            elif name_of_profession == "" or name_of_profession in vacancy.name:
                number_of_vacancies += 1
        number_of_vacancies_statistics.append(f'{current_year}: {number_of_vacancies}')
        return number_of_vacancies_statistics

    def get_salary_level_city_statistics(self):
        """ Возвращает уровень зарплат по городам (в порядке убывания)
        Returns:
            list<str>: Статистика по уровню зарплат по городам
        """
        number_of_vacancies = len(self.dataset.vacancies_objects)
        salary_at_cities = {}
        for vacancy in self.dataset.vacancies_objects:
            if vacancy.area_name not in salary_at_cities:
                salary_at_cities[vacancy.area_name] = (1, vacancy.salary.average)
            else:
                salary_at_cities[vacancy.area_name] = (salary_at_cities[vacancy.area_name][0] + 1,
                                                       salary_at_cities[vacancy.area_name][1] + vacancy.salary.average)
        salary_at_cities = dict(
            sorted(salary_at_cities.items(), key=lambda item: item[1][1] / item[1][0], reverse=True))
        average_salary_at_cities = []
        for city_name, value in salary_at_cities.items():
            if value[0] >= math.floor(number_of_vacancies / 100):
                average_salary_at_cities.append(f"'{city_name}': {math.floor(value[1] / value[0])}")
        return average_salary_at_cities[:10]

    def get_number_of_vacancies_city_statistics(self):
        """ Возвращает долю вакансий по городам (в порядке убывания)
        Returns:
             list<str>: Доля вакансий по городам (в порядке убывания)
        """
        number_of_all_vacancies = len(self.dataset.vacancies_objects)
        number_of_vacancies_at_cities = {}
        for vacancy in self.dataset.vacancies_objects:
            if vacancy.area_name not in number_of_vacancies_at_cities:
                number_of_vacancies_at_cities[vacancy.area_name] = 1
            else:
                number_of_vacancies_at_cities[vacancy.area_name] += 1
        salary_at_cities = dict(sorted(number_of_vacancies_at_cities.items(), key=lambda item: item[1], reverse=True))
        result = []
        for city_name, number_of_vacancies in salary_at_cities.items():
            if number_of_vacancies >= math.floor(number_of_all_vacancies / 100):
                result.append(f"'{city_name}': {round(number_of_vacancies / number_of_all_vacancies, 4)}")
        return result[:10]

    @staticmethod
    def convert_year_statistic_to_dictionary(statistic):
        """ Конвертирует статистку, связянную с зарплатой или с долей вакансий, в словарь
        Args:
            statistic(list<str>):
        Returns:
            dict<int, int>
        """
        return {int(i.split(': ')[0]): int(i.split(': ')[1]) for i in statistic}

    @staticmethod
    def convert_city_statistic_to_dictionary(statistic):
        """ Конвертирует статистку, связянную с городами, в словарь
        Args:
            statistic(list<str>):
        Returns:
            dict<string, float>
        """
        return {i.split(': ')[0][1:-1]: float(i.split(': ')[1]) for i in statistic}