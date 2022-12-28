from StatisticalDataProcessor import StatisticalDataProcessor
from Report import Report
from Vacancies_Controller import Vacancies_Controller
import pandas as pd

from Separator import Separator


if __name__ == "__main__":
    statistic= StatisticalDataProcessor()
    statistic.initialize_statistics_from_database()






