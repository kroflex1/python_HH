import csv
import re
import sys
import math
import prettytable
from prettytable import PrettyTable
from datetime import datetime

class InputConect:
    """Класс для печатанья таблицы по вакансиям.
        Attributes:
            russian_versions(dict<str, str>): Перевод названия столбцов
            decoding(dict<str, str>): Перевод значений валюы и опыта с английского на русский
            work_experience_convertor_weight(dict<str, int>): Вес опыта
            formatter_dic(dict<str, str or datetime or list>): Преобразует строку к правильному виду
            filters(dict<str, lambda>): Как должны фильтроваться те или иные поля
            sorting_rules(dict<str, lambda>): Как должны сортироваться те или иные поля
            fields(list<str>): Требуемые столбцы
            vacancy_numbers(int): количество вакансий
        """

    def __init__(self, dataset):
        """Инициализирует класс InputConnect
        Args:
            dataset(Dataset): Информация о вакансиях
        """
        self.russian_versions = {'name': 'Название',
                                 'description': 'Описание',
                                 'key_skills': 'Навыки',
                                 'experience_id': 'Опыт работы',
                                 'premium': 'Премиум-вакансия',
                                 'employer_name': 'Компания',
                                 'salary_from': 'Нижняя граница вилки оклада',
                                 'salary_to': 'Верхняя граница вилки оклада',
                                 'salary_gross': 'Оклад указан до вычета налогов',
                                 'salary_currency': 'Идентификатор валюты оклада',
                                 'area_name': 'Название региона',
                                 'published_at': 'Дата и время публикации вакансии'
                                 }
        self.decoding = {"noExperience": "Нет опыта",
                         "between1And3": "От 1 года до 3 лет",
                         "between3And6": "От 3 до 6 лет",
                         "moreThan6": "Более 6 лет",
                         "AZN": "Манаты",
                         "BYR": "Белорусские рубли",
                         "EUR": "Евро",
                         "GEL": "Грузинский лари",
                         "KGS": "Киргизский сом",
                         "KZT": "Тенге",
                         "RUR": "Рубли",
                         "UAH": "Гривны",
                         "USD": "Доллары",
                         "UZS": "Узбекский сум",
                         'True': 'Да',
                         'False': 'Нет'
                         }
        self.work_experience_convertor_weight = {
            "noExperience": 0,
            "between1And3": 1,
            "between3And6": 2,
            "moreThan6": 3
        }
        self.formatter_dic = {
            'Название': lambda vacancy: vacancy.name,
            'Описание': lambda vacancy: vacancy.description,
            'Навыки': lambda vacancy: ";".join(vacancy.key_skills),
            'Опыт работы': lambda vacancy: self.decoding[vacancy.experience_id],
            'Премиум-вакансия': lambda vacancy: self.decoding[vacancy.premium],
            'Компания': lambda vacancy: vacancy.employer_name,
            'Оклад': lambda vacancy: self.format_salary_information(vacancy),
            'Название региона': lambda vacancy: vacancy.area_name,
            'Дата публикации вакансии': lambda vacancy: vacancy.published_at.strftime('%d.%m.%Y'),
        }
        self.filters = {
            'Компания': lambda employer_name, vacancy: employer_name == vacancy.employer_name,
            'Оклад': lambda salary, vacancy: int(float(vacancy.salary.salary_from)) <= int(float(salary)) <= int(
                float(vacancy.salary.salary_to)),
            'Дата публикации вакансии': lambda date, vacancy: date == vacancy.published_at.strftime('%d.%m.%Y'),
            'Навыки': lambda skills, vacancy: set(skills.split(', ')).issubset(vacancy.key_skills),
            'Опыт работы': lambda experience_id, vacancy: experience_id == self.decoding[vacancy.experience_id],
            'Премиум-вакансия': lambda premium, vacancy: premium == self.decoding[vacancy.premium],
            'Идентификатор валюты оклада': lambda salary_currency, vacancy: salary_currency == self.decoding[
                vacancy.salary_currency],
            'Название': lambda name, vacancy: name == vacancy.name,
            'Название региона': lambda area_name, vacancy: area_name == vacancy.area_name,
        }
        self.sorting_rules = {
            'Навыки': lambda vacancy: len(vacancy.key_skills),
            'Оклад': lambda vacancy: ((float(vacancy.salary.salary_from) + float(vacancy.salary.salary_to)) / 2) *
                                     self.currency_to_rub[
                                         vacancy.salary_currency],
            'Дата публикации вакансии': lambda vacancy: datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z'),
            'Компания': lambda vacancy: vacancy.employer_name,
            'Опыт работы': lambda vacancy: self.work_experience_convertor_weight[vacancy.experience_id],
            'Премиум-вакансия': lambda vacancy: self.decoding[vacancy.premium],
            'Название региона': lambda vacancy: vacancy.area_name,
            'Название': lambda vacancy: vacancy.name,
            'Идентификатор валюты оклада': lambda vacancy: self.decoding(vacancy.salary_currency)
        }

        self.fields = dataset.fields
        self.vacancy_numbers = dataset.vacancy_numbers
        data_vacancies = self.get_filtered_data_vacancies(dataset.vacancies_objects, dataset.filtering_parameter)
        self.sort_data_vacancies(data_vacancies, dataset.sorting_parameter, dataset.is_reverse_sorting)
        self.table = self.create_table(data_vacancies)

    def get_filtered_data_vacancies(self, dataset, filtering_parameter):
        """Филтурет вакансии по переданному параметру
        Args:
            dataset(list<Vacancy>): Список вакансий
            filtering_parameter(str): Параметр фильтрации
        Resturns:
            list<Vacancy>
        """
        if filtering_parameter != '':
            parameters = filtering_parameter.split(': ')
            filter_name = parameters[0]
            filter_value = parameters[1]
            filtered_data_vacancies = [row for row in dataset if self.filters[filter_name](filter_value, row)]
            if len(filtered_data_vacancies) == 0:
                print('Ничего не найдено')
                sys.exit()
            return filtered_data_vacancies
        return dataset

    def sort_data_vacancies(self, data_vacancies, sorting_parameter, is_reverse_sorting):
        """Сортирует вакансии по переданному параметру
        Args:
            data_vacancies(list<Vacancy>): Список вакансий
            sorting_parameter(str): Параметр сортировки
            is_reverse_sorting(str): Порядок сортировки(Да - прямой, Нет - обратный)
        Resturns:
            list<Vacancy>
        """
        if sorting_parameter != '':
            is_reverse = False if is_reverse_sorting == 'Нет' or is_reverse_sorting == '' else True
            data_vacancies.sort(key=self.sorting_rules[sorting_parameter], reverse=is_reverse)

    def formatter(self, vacancy):
        """Форматирует вакансию к стандартному виду
        Args:
            dataset(Vacancy): вакансия
        Resturns:
                Vacancy
                """
        formatted_vacancy = {}
        for key, value in self.formatter_dic.items():
            formatted_vacancy[key] = value(vacancy)
        return formatted_vacancy

    def format_vacancy_for_table(self, vacancy):
        """Форматирует вакансию к специальному виду для таблицы
        Args:
            vacancy(dict<str, str>): Вакансия
        Resturns:
            dict<str,str>: Форматированная вакансия
        """
        if len(vacancy['Навыки']) > 100:
            vacancy['Навыки'] = vacancy['Навыки'][:100] + '...'
        vacancy['Навыки'] = '\n'.join(vacancy['Навыки'].split(';'))
        for key, value in vacancy.items():
            if key == 'Навыки':
                continue
            if len(value) > 100:
                vacancy[key] = value[:100] + '...'

    def create_table(self, data_vacancies):
        """Создаёт таблицу
        Args:
            data_vacancies(dict<str,str>)
        Returns:
            PrettyTable: Таблица
        """
        if len(data_vacancies) == 0:
            print('Нет данных')
            sys.exit()
        table = PrettyTable()
        columns = ['№'] + list(self.formatter(data_vacancies[0]).keys())
        table.field_names = columns
        for index, vacancy in enumerate(data_vacancies):
            formatted_vacancy = self.formatter(vacancy)
            self.format_vacancy_for_table(formatted_vacancy)
            table.add_row([str(index + 1)] + list(formatted_vacancy.values()))
        table.max_width = 20
        table.align = 'l'
        table.hrules = prettytable.ALL
        return table

    def print_table(self):
        """Печатает таблицу"""
        vacancy_numbers = self.vacancy_numbers.split(' ') if self.vacancy_numbers != '' else []
        fields = ['№'] + self.fields.split(', ') if self.fields != '' else self.table.field_names
        start = int(vacancy_numbers[0]) - 1 if len(vacancy_numbers) >= 1 else 0
        end = int(vacancy_numbers[1]) - 1 if len(vacancy_numbers) == 2 else len(self.table.rows)
        print(self.table.get_string(start=start, end=end, fields=fields))

    def format_salary_information(self, vacancy):
        """Приводит информацию  о зарплате к стандатному виду для таблицы
        Args:
            vacancy(Vacancy): Ваканси
        Resturns:
            str: Отформатированная информация о зарплате
        """

        def format_salary(salary):
            salary = int(float(salary))
            salary = ' '.join(f'{salary:,}'.split(','))
            return salary

        is_salary_gross = 'Без вычета налогов' if vacancy.salary.salary_gross == 'True' else 'С вычетом налогов'
        return f'{format_salary(vacancy.salary.salary_from)} - {format_salary(vacancy.salary.salary_to)} ({self.decoding[vacancy.salary.salary_currency]}) ({is_salary_gross})'
