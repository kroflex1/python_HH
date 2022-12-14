# Содержание
* [2.3.2](#2_3_2)
* [2.3.3](#2_3_3)
* [3.2.1](#3_2_1)
* [3.2.2](#3_2_2)
* [3.2.3](#3_2_3)
* [3.3.1](#3_3_1)
* [3.3.2](#3_3_2)
* [3.3.3](#3_3_3)
* [3.4.1](#3_4_1)
* [3.4.2](#3_4_2)
* [3.4.3](#3_4_3)
* [3.5.1](#3_5_1)
* [3.5.2](#3_5_2)
* [3.5.3](#3_5_3)


## Задание 2.3.2 <a name="2_3_2"></a> 
![image](https://user-images.githubusercontent.com/48649189/204853405-afa7ffda-0594-4c64-bc06-f8cc7d16a888.png)
![image](https://user-images.githubusercontent.com/48649189/204853507-0361ac16-2b98-4238-be16-566684c97458.png)
![image](https://user-images.githubusercontent.com/48649189/204853643-77215a17-8c00-4620-a96c-7b7a3807d399.png)

## Задание 2.3.3 <a name="2_3_3"></a> 
Замеры вывода времени работы по выводу таблицы таблицы
![1](https://user-images.githubusercontent.com/48649189/206187260-b311e32d-a207-4ae8-a7cb-a1a2ca697f62.png)

### Варианты преобразования даты
```Python
from datetime import datetime

def get_year_1(date_string):
    year = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z').year
    return year

def get_year_2(date_string):
    year = int(date_string.split("-")[0])
    return year

def get_year_3(date_string):
    year = int(date_string[:4])
    return year

date_string =  '2022-05-31T17:32:31+0300'

for i in range(1000000):
    get_year_1(date_string)
for i in range(1000000):
    get_year_2(date_string)
for i in range(1000000):
    get_year_3(date_string)
```
### Измерим скорость выполнения функций
![image](https://user-images.githubusercontent.com/48649189/206188128-c88ffa03-127a-4a1d-924b-fd17a13dcecc.png)

**Самая быстрая функция это get_year_3**
![4](https://user-images.githubusercontent.com/48649189/206187923-27b34e98-44f0-4c82-a3c4-f4eae3768c46.png)

**После неё идёт функция get_year_2**
![3](https://user-images.githubusercontent.com/48649189/206188015-89bbcc66-d69a-4bf6-a8ea-c08dc34c57ff.png)

**Самой же медленной является функция get_year_1**
![2](https://user-images.githubusercontent.com/48649189/206188239-2aede464-983a-4c7b-93d6-8cd0cdcebd21.png)

## Задание 3.2.1 <a name="3_2_1"></a> 

![image](https://user-images.githubusercontent.com/48649189/206664238-6330db43-cc0b-4209-9571-cc9be67e16d4.png)
## Несколько файлов csv, разделенныз по годам
[part_2007.csv](https://github.com/kroflex1/python_HH/files/10193285/part_2007.csv)
[part_2008.csv](https://github.com/kroflex1/python_HH/files/10193288/part_2008.csv)

## Задание 3.2.2 <a name="3_2_2"></a> 

Скорость работы StatisticalDataProcessor до 
![1](https://user-images.githubusercontent.com/48649189/206855618-a77eb59b-1e9d-4d8c-834e-8e680d314787.png)
Скорость работы StatisticalDataProcessor после
![2](https://user-images.githubusercontent.com/48649189/206855635-21174e4c-3ea5-476c-a9ea-003eda1004b5.png)

## Задание 3.2.3 <a name="3_2_3"></a> 

Скорость работы StatisticalDataProcessor до 
![2](https://user-images.githubusercontent.com/48649189/206855635-21174e4c-3ea5-476c-a9ea-003eda1004b5.png)
Скорость работы StatisticalDataProcessor после
![3](https://user-images.githubusercontent.com/48649189/206870409-158406ea-e12f-4b3e-a110-42f7dcb6267a.png)

## Задание 3.3.1 <a name="3_3_1"></a> 
**Частность валют**

![image](https://user-images.githubusercontent.com/48649189/208850302-54c1ccbb-b4c7-4cf7-b3e5-08e75c864fc1.png)

**сsv файл с курсом валют по месяцам**

![image](https://user-images.githubusercontent.com/48649189/208899540-f61ac737-d4ef-438b-a93a-56977ea36441.png)
Файл: [currency.csv](https://github.com/kroflex1/python_HH/files/10277394/currency.csv)

**Разделеенные cvs файлы**

![image](https://user-images.githubusercontent.com/48649189/208851053-bf463667-347a-4ae0-a0ff-8231a452f7ec.png)

## Задание 3.3.2 <a name="3_3_2"></a> 
![image](https://user-images.githubusercontent.com/48649189/208931998-aad8a88d-5423-4247-8ff7-80b3e48ff08e.png)
**Файл:** [salary_info_100.csv](https://github.com/kroflex1/python_HH/files/10278622/salary_info_100.csv)

## Задание 3.3.3 <a name="3_3_3"></a> 
![image](https://user-images.githubusercontent.com/48649189/208973027-3706e640-474d-4aef-87f5-7e33d48179e2.png)
**Файл:**[vacancies_from_HH.csv](https://github.com/kroflex1/python_HH/files/10280097/vacancies_from_HH.csv)

## Задание 3.4.1 <a name="3_4_1"></a> 
![image](https://user-images.githubusercontent.com/48649189/208931998-aad8a88d-5423-4247-8ff7-80b3e48ff08e.png)
**Файл:** [salary_info_100.csv](https://github.com/kroflex1/python_HH/files/10278622/salary_info_100.csv)

## Задание 3.4.2 <a name="3_4_2"></a> 
Исходные данные взяты из файла "vacancies_dif_currencies.csv"

**Файл:** [out.pdf](https://github.com/kroflex1/python_HH/files/10298266/out.pdf)

## Задание 3.4.3 <a name="3_4_3"></a> 
Исходные данные взяты из файла "vacancies_dif_currencies.csv"

**Файл:** [out.pdf](https://github.com/kroflex1/python_HH/files/10300016/out.pdf)

## Задание 3.5.1 <a name="3_5_1"></a> 
**Название Файла: currency_dynamic.sqlite** 


## Задание 3.5.2 <a name="3_5_2"></a> 
![ex2](https://user-images.githubusercontent.com/48649189/209556937-91bbd64c-905e-40cc-904b-b5184359c104.png)



## Задание 3.5.3 <a name="3_5_3"></a> 
Программа по выводу данных

```Python
    def initialize_statistics_from_database(self):
    file_name = input('Введите название файла: ')
    self.name_of_profession = input("Введите название профессии:  ")
    vacancy_controller = Vacancies_Controller()
    vacancy_controller.create_formatted_file(file_name)

    self.con = sqlite3.connect('currency_dynamic.sqlite')

    self.print_average_salary_from_database()
    self.print_number_of_vacancies()
    self.print_average_salary_profession()
    self.print_number_of_vacancies_profession()

    self.print_salary_level_by_city()
    self.print_vacancy_rate()


def print_average_salary_from_database(self):
    data = pd.read_sql_query(
        "SELECT strftime('%Y', published_at) as year, ROUND(AVG(salary), 4) as average_salary FROM formatted GROUP BY strftime('%Y', published_at)",
        self.con)
    print(data)
    print('\n')


def print_number_of_vacancies(self):
    data = pd.read_sql_query(
        "SELECT  strftime('%Y', published_at) as year, COUNT(name) as count FROM formatted GROUP BY strftime('%Y', published_at)",
        self.con)
    print(data)
    print('\n')


def print_average_salary_profession(self):
    data = pd.read_sql_query(
        f"SELECT  strftime('%Y', published_at) as year, ROUND(AVG(salary),4) as average_salary FROM formatted WHERE name LIKE '%{self.name_of_profession}%' GROUP BY strftime('%Y', published_at)",
        self.con)
    print(data)
    print('\n')


def print_number_of_vacancies_profession(self):
    data = pd.read_sql_query(
        f"SELECT  strftime('%Y', published_at) as year, COUNT(name) as count FROM formatted WHERE name LIKE '%{self.name_of_profession}%' GROUP BY strftime('%Y', published_at)",
        self.con)
    print(data)
    print('\n')


def print_salary_level(self):
    amount = self.con.execute('SELECT COUNT(*) FROM formatted').fetchone()[0]
    data = pd.read_sql_query(
        f"SELECT area_name, ROUND(AVG(salary),4) as average_salary FROM formatted GROUP BY area_name HAVING COUNT(name) >= {amount} / 100 ORDER BY AVG(salary) DESC LIMIT 10",
        self.con)
    print(data)
    print('\n')


def print_vacancy_rate(self):
    amount = self.con.execute('SELECT COUNT(*) FROM formatted').fetchone()[0]
    data = pd.read_sql_query(
        f"SELECT  area_name, ROUND(CAST(COUNT(name) AS FLOAT) / {amount},4) as rate  FROM formatted GROUP BY area_name HAVING COUNT(name) >= {amount}/ 100 ORDER BY COUNT(name) / {amount} DESC LIMIT 10",
        self.con)
    print(data)
    print('\n')
```

![image](https://user-images.githubusercontent.com/48649189/209555810-28484d05-d44a-4294-b9e1-0871b0437c17.png)

Вывод программы по вакансии Программист:
**Динамика уровня зарплат по годам**

![image](https://user-images.githubusercontent.com/48649189/209555850-39c718f5-aecb-4da0-a906-def816d7f42f.png)

**Динамика количества вакансий по годам**

![image](https://user-images.githubusercontent.com/48649189/209555976-411f77d5-d277-4346-b62a-e34a1c65c877.png)

**Динамика уровня зарплат по годам для выбранной профессии**

![image](https://user-images.githubusercontent.com/48649189/209555994-040b4ec6-8d51-4122-82e7-78c78e0979c5.png)

**Динамика количества вакансий по годам для выбранной профессии**

![image](https://user-images.githubusercontent.com/48649189/209556016-738927c5-d3f2-45bb-b44a-50b8b20b3748.png)

**Уровень зарплат по городам**

![image](https://user-images.githubusercontent.com/48649189/209556031-8dde2388-d92d-4c2b-b5be-09d8e1beb7df.png)

**Доля вакансий по городам**

![image](https://user-images.githubusercontent.com/48649189/209556050-ea32f0bd-3381-4167-be7f-6d1078b00428.png)













