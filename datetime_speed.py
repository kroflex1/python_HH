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

