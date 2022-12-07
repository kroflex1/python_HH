from datetime import datetime

class Salary:
    """Класс для представления зарплаты.

    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница  вилки оклада
        salary_currency (str): Валюята оклада
        salary_gross (str): Указан ли оклад до вычета налогов
        average (int): Средняя зарплата
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

    def __init__(self, salary_from, salary_to, salary_currency, salary_gross="True"):
        """Инициализирует объект Salary, выполняет конвертацию для целоисленных полей

        Args:
            salary_from (str or int or float):Нижняя граница вилки оклада
            salary_to (str or int or float): Верхняя граница  вилки оклада
            salary_gross (str or int or float): Валюята оклада
            salary_currency(str): Указан ли оклад до вычета налогов
        """
        self.salary_from = float(salary_from) * self.currency_to_rub[salary_currency]
        self.salary_to = float(salary_to) * self.currency_to_rub[salary_currency]
        self.salary_currency = salary_currency
        self.salary_gross = salary_gross
        self.average = int((self.salary_from + self.salary_to) / 2)


class Vacancy:
    """Класс для представления ваканcии.

    Attributes:
        name(str): Название вакансии
        salary(Salary): Информация о зарплатае вакансии
        area_name(str): Место работы
        published_at(str): Где опубликовано
        description(str): Описание вакансии
        key_skills(list<str>): Необходимые навыки для вакансии
        experience_id(str): Необходимый опыт работы
        premium(str): Премиум
        employer_name(str): Название компании
    """

    def __init__(self, vacancy_information):
        """Инициализирует объект Vacancy

        Args:
             vacancy_information(dict<str:str>): Словарь, в котором записаны значения вакансии
        """
        self.name = vacancy_information['name']
        self.salary = Salary(vacancy_information['salary_from'], vacancy_information['salary_to'],
                             vacancy_information['salary_currency'])
        self.area_name = vacancy_information['area_name']
        self.published_at = datetime.strptime(vacancy_information['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        self.description = vacancy_information['description']
        self.key_skills = vacancy_information['key_skills'].split(';')
        self.experience_id = vacancy_information['experience_id']
        self.premium = vacancy_information['premium']
        self.employer_name = vacancy_information['employer_name']