# Задание 2.3.2
![image](https://user-images.githubusercontent.com/48649189/204853405-afa7ffda-0594-4c64-bc06-f8cc7d16a888.png)
![image](https://user-images.githubusercontent.com/48649189/204853507-0361ac16-2b98-4238-be16-566684c97458.png)
![image](https://user-images.githubusercontent.com/48649189/204853643-77215a17-8c00-4620-a96c-7b7a3807d399.png)

# Задание 2.3.3
Замеры вывода времени работы по выводу таблицы таблицы
![1](https://user-images.githubusercontent.com/48649189/206187260-b311e32d-a207-4ae8-a7cb-a1a2ca697f62.png)

## Варианты преобразования даты
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
## Измерим скорость выполнения функций
![image](https://user-images.githubusercontent.com/48649189/206188128-c88ffa03-127a-4a1d-924b-fd17a13dcecc.png)

**Самая быстрая функция это get_year_3**
![4](https://user-images.githubusercontent.com/48649189/206187923-27b34e98-44f0-4c82-a3c4-f4eae3768c46.png)

**После неё идёт функция get_year_2**
![3](https://user-images.githubusercontent.com/48649189/206188015-89bbcc66-d69a-4bf6-a8ea-c08dc34c57ff.png)

**Самой же медленной является функция get_year_1**
![2](https://user-images.githubusercontent.com/48649189/206188239-2aede464-983a-4c7b-93d6-8cd0cdcebd21.png)

# Задание 3.2.1

![image](https://user-images.githubusercontent.com/48649189/206664238-6330db43-cc0b-4209-9571-cc9be67e16d4.png)
## Несколько файлов csv, разделенныз по годам
[part_2007.csv](https://github.com/kroflex1/python_HH/files/10193285/part_2007.csv)
[part_2008.csv](https://github.com/kroflex1/python_HH/files/10193288/part_2008.csv)

