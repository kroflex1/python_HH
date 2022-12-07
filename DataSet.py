from InputConect import InputConect
from Vacancy  import Vacancy
from datetime import datetime
import re
import sys
import csv

class DataSet:
    """Класс для представления вакансий.

    Attributes:
        file_name(str): Название файла, откуда будут взяты данные для вакансий
        name_of_profession(str): Название професии, по которой можно будет получить список вакансий
        vacancies_objects(list<Vacancy>): Список вакансий
        filtering_parameter(str):параметр фильтрации
        sorting_parameter(str):параметр сортировки
        is_reverse_sorting(str):порядок сортировки
        vacancy_numbers(str): диапазон вывода
        fields(str):требуемые столбцы
    """

    def __init__(self):
        """Инициализирует объект Dataset"""
        self.file_name = input('Введите название файла: ')
        self.name_of_profession = input('Введите название профессии: ')
        self.vacancies_objects = self.__read_data_vacancies()

    def __read_data_vacancies(self):
        """Преобразуе данные из файла в list<Vacancy>
        Returns:
            list<Vacancy>: Список вакансий
        """
        list_naming, list_data = DataSet.csv_reader(self.file_name)
        data_vacancies = DataSet.csv_filer(list_data, list_naming)
        return [Vacancy(vacancy_information) for vacancy_information in data_vacancies]

    def print_table(self):
        """Выводит таблицу по переданным пользователем параметрам
        """
        self.filtering_parameter = input('Введите параметр фильтрации: ')
        self.sorting_parameter = input('Введите параметр сортировки: ')
        self.is_reverse_sorting = input('Обратный порядок сортировки (Да / Нет): ')
        self.vacancy_numbers = input('Введите диапазон вывода: ')
        self.fields = input('Введите требуемые столбцы: ')
        DataSet.check_entered_data(self.filtering_parameter, self.sorting_parameter, self.is_reverse_sorting)

        input_conect = InputConect(self)
        input_conect.print_table()

    @staticmethod
    def csv_reader(file_name):
        """Возращает из прочитанного файла список столбоцов и список вакансий
        Args:
            file_name(str): навзание файла
        Returns:
            list<str>
            list<list<str>>
        """
        file_csv = open(file_name, encoding='utf_8_sig')
        reader_csv = csv.reader(file_csv)
        list_data = [x for x in reader_csv]
        if len(list_data) == 0:
            print("Пустой файл")
            sys.exit()
        return list_data[0], list_data[1:]

    @staticmethod
    def csv_filer(reader, list_naming):
        """Проверяет столбцы и списки вакансии на ошибки, и преобразует список вакансии в словарь
        Args:
            reader(list<list<str>>): навзание файла
            list_naming(list<str>): Название столбцов
        Returns:
            list<dict<str, str>>: Список вакансий в виде словарей
        """
        rows = [x for x in reader if len(x) == len(list_naming) and '' not in x]
        dictionary_rows = [DataSet.convert_row_to_dictionary(list_naming, row) for row in rows]
        return dictionary_rows

    @staticmethod
    def convert_row_to_dictionary(columns_name, row):
        """Конвертирует список в словарь
        Args:
            columns_name(list<str>): Название столбцов
            row(list<str>): Строка(вакансия)
        Returns:
            dict<str, str>: Вакансия в виде словаря
        """
        dict = {}
        for i in range(len(columns_name)):
            dict[columns_name[i]] = DataSet.convert_cell_to_standard(row[i])
        return dict

    @staticmethod
    def convert_cell_to_standard(cell):
        """Приводит ячейку к стандратному виду
        Args:
            cell(str): ячейка
        Returns:
            cell(str or list<str>): Отформотировання ячейка
        """
        words = re.sub(r'<[^>]*>', '', cell).split('\n')
        for i in range(len(words)):
            words[i] = ' '.join(words[i].split())
        return ';'.join(map(str, words))

    @staticmethod
    def check_entered_data(filtering_parameter, sorting_parameter, is_reverse_sorting):
        """Проверяет введённые параметры вывода таблицы(фильтр, сортировка, порядок) на корректность ввода
         Args:
            filtering_parameter(str): Фильтр
            sorting_parameter(str): Параметр сортировки
            is_reverse_sorting(str): В каком порядке выводится таблица
        """
        currency_to_rub = {
            "AZN": 35.68,
            "BYR": 23.91,
            "EUR": 59.90,
            "GEL": 21.74,
            "KGS": 0.76,
            "KZT": 0.13,
            "RUR": 1,
            "UAH": 1.64,
            "USD": 60.66,
            "UZS": 0.0055,
        }
        work_experience_convertor_weight = {
            "noExperience": 0,
            "between1And3": 1,
            "between3And6": 2,
            "moreThan6": 3
        }
        decoding = {"noExperience": "Нет опыта",
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
        sorting_rules = {
            'Навыки': lambda vacancy: len(vacancy.key_skills),
            'Оклад': lambda vacancy: ((float(vacancy.salary.salary_from) + float(vacancy.salary.salary_to)) / 2) *
                                     currency_to_rub[
                                         vacancy.salary_currency],
            'Дата публикации вакансии': lambda vacancy: datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z'),
            'Компания': lambda vacancy: vacancy.employer_name,
            'Опыт работы': lambda vacancy: work_experience_convertor_weight[vacancy.experience_id],
            'Премиум-вакансия': lambda vacancy: decoding[vacancy.premium],
            'Название региона': lambda vacancy: vacancy.area_name,
            'Название': lambda vacancy: vacancy.name,
            'Идентификатор валюты оклада': lambda vacancy: decoding(vacancy.salary_currency)
        }
        filters = {
            'Компания': lambda employer_name, vacancy: employer_name == vacancy.employer_name,
            'Оклад': lambda salary, vacancy: int(float(vacancy.salary.salary_from)) <= int(float(salary)) <= int(
                float(vacancy.salary.salary_to)),
            'Дата публикации вакансии': lambda date, vacancy: date == vacancy.published_at.strftime('%d.%m.%Y'),
            'Навыки': lambda skills, vacancy: set(skills.split(', ')).issubset(vacancy.key_skills),
            'Опыт работы': lambda experience_id, vacancy: experience_id == decoding[vacancy.experience_id],
            'Премиум-вакансия': lambda premium, vacancy: premium == decoding[vacancy.premium],
            'Идентификатор валюты оклада': lambda salary_currency, vacancy: salary_currency == decoding[
                vacancy.salary_currency],
            'Название': lambda name, vacancy: name == vacancy.name,
            'Название региона': lambda area_name, vacancy: area_name == vacancy.area_name,
        }
        if filtering_parameter != '' and ':' not in filtering_parameter:
            print('Формат ввода некорректен')
            sys.exit()
        parameters = filtering_parameter.split(': ')
        if filtering_parameter != '' and parameters[0] not in filters.keys():
            print('Параметр поиска некорректен')
            sys.exit()
        if sorting_parameter != '' and is_reverse_sorting not in ('Да', 'Нет', ''):
            print('Порядок сортировки задан некорректно')
            sys.exit()
        if sorting_parameter != '' and sorting_parameter not in sorting_rules.keys():
            print('Параметр сортировки некорректен')
            sys.exit()