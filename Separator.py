import pandas as pd
from datetime import datetime
from Vacancies_Controller import Vacancies_Controller


class Separator:
    def __init__(self):
        self.main_df = None
        self.folder_name = None
        self.unique_years = None
        self.folder_regions_name  = None
        self.unique_regions  = None

    def create_files_separated_by_years(self, file_name):
        """Разделяет файлы по годам и оставляя лишь поля name, area_name, published_at, salary"""
        df = pd.read_csv(file_name)
        Vacancies_controller = Vacancies_Controller()
        df = Vacancies_controller.get_formatted_dataframe(df)
        df = df.dropna()
        df["years"] = df["published_at"].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)
        years = df["years"].unique()
        for year in years:
            data = df[df["years"] == year]
            data.iloc[:, :-1].to_csv(rf"csv_files\part_{year}.csv", index=False)
        self.main_df = df
        self.unique_years = years
        self.folder_name = "csv_files"

    def create_files_separated_by_region(self, file_name):
        """Разделяет файлы по городам и оставляя лишь поля name, area_name, published_at, salary"""
        df = pd.read_csv(file_name)
        Vacancies_controller = Vacancies_Controller()
        df = Vacancies_controller.get_formatted_dataframe(df)
        df = df.dropna()
        regions = df["area_name"].unique()
        self.unique_regions = []
        for region in regions:
            data = df[df["area_name"] == region]
            if len(data) >= len(df) / 100:
                self.unique_regions.append(region)
                data.to_csv(rf"regions\{region}.csv", index=False)
        self.main_df = df
        self.folder_regions_name = "regions"

