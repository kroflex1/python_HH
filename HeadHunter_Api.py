import requests
import pandas as pd
from datetime import datetime

class HeadHunter_Vacancies:
    def __init__(self):
        self.dates = []
        self.__initialize_dates()

    def get_vacancies(self):
        all_vacancies = []
        for i in range(len(self.dates) - 1):
            all_vacancies.extend(self.__read_vacancies(self.dates[i], self.dates[i + 1]))

        df = pd.DataFrame.from_dict( all_vacancies)
        df.to_csv('vacancies_from_HH.csv', index=False)

    def __initialize_dates(self):
        date1 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=0, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date2 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=4, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date3 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=8, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date4 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=12, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date5 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=16, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date6 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=20, minute=0,
                                                                                             second=0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        date7 = datetime.strptime('2022-12-20T00:00:00+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=23, minute=59,
                                                                                             second=59).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.dates = [date1, date2, date3, date4, date5, date6, date7]

    def __read_vacancies(self, start_date, end_date):
        def try_get_json(page, start_date, end_date):
            for i in range(50):
                response = requests.get(
                    f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from={start_date}&date_to={end_date}')
                if response.status_code == 200:
                    return response.json()
            raise requests.exceptions.RetryError('Не удалось получить ответ от сервеа')
        json = requests.get(
            f'https://api.hh.ru/vacancies?specialization=1&per_page=100&date_from={start_date}&date_to={end_date}').json()
        pages = json['pages']
        vacancies = []
        for page in range(pages):
            json = try_get_json(page, start_date, end_date)
            for vacancy in json['items']:
                new_vacancy = {'name': vacancy['name'],
                               'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
                               'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
                               'salary_currency': vacancy['salary']['currency'] if vacancy['salary'] else None,
                               'area_name': vacancy['area']['name'],
                               'published_at': vacancy['published_at']}
                vacancies.append(new_vacancy)
        return vacancies
