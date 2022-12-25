from StatisticalDataProcessor import StatisticalDataProcessor
from Report import Report
import pandas as pd

from Separator import Separator


if __name__ == "__main__":
    statistic = StatisticalDataProcessor()
    statistic.initialize_statistics_by_region()
    report = Report()
    report.generate_pdf_region( statistic.get_final_region_statistics(), statistic.get_final_city_statistics(), statistic.name_of_profession, statistic.region)




