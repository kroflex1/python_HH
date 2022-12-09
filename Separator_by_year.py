import pandas as pd
from datetime import datetime


class SeparatorByYear:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_files_separated_by_years(self):
        df = pd.read_csv(self.file_name)
        df["years"] = df["published_at"].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)
        years = df["years"].unique()
        for year in years:
            data = df[df["years"] == year]
            data.iloc[:, :-1].to_csv(rf"csv_files\part_{year}.csv", index=False)


sep = SeparatorByYear("vacancies_by_year.csv")
sep.get_files_separated_by_years()
