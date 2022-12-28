import pandas as pd
import sqlite3

def Ex1():
    df = pd.read_csv('currency.csv')

    conn = sqlite3.connect('currency_dynamic.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS test (date text, USD float, EUR float, KZT float, UAH float, BYR float)')
    conn.commit()
    df.to_sql('currency_dynamic', conn, if_exists='replace', index = False)
    c.execute('SELECT * FROM currency_dynamic')
    for row in c.fetchmany(10):
        print(row)
    conn.close()
