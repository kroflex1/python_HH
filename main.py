from DataSet import DataSet
from StatisticalDataProcessor import StatisticalDataProcessor
from Report import Report

if __name__ == "__main__":
    data_type = input('Выберите метод работы: ')
    dataset = DataSet()

    if (data_type == 'Вакансии'):
        dataset.print_table()

    elif (data_type == 'Статистика'):
        statistical_data_processor = StatisticalDataProcessor(dataset)
        report = Report()
        report.generate_pdf(statistical_data_processor.get_final_year_statistics(),
                              statistical_data_processor.get_final_city_statistics(),
                              statistical_data_processor.name_of_profession)
    else:
        print('Вы ввели неверную команду')
