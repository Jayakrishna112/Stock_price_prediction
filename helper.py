from MySql import MySql
from model_trainer import ModelTrainer
from holiday_calculator import Holidays
from Data_Extractor import DataExtractor


class HelperClass:
    def __init__(self):
        self.model = None
        self.data = None

    def Data_loader(self):
        mysql = MySql()
        # connecting to the database
        mysql.connect()
        # extracting data from the database
        self.data = mysql.data_loader()
        
        mysql.disconnect()

    def model_trainer(self):

        holiday_class = Holidays()

        holidays = holiday_class.calculate(self.data.iloc[0][0], self.data.iloc[-1][0])

        model_class = ModelTrainer()
        
        self.model = model_class.build_model(holidays)

        model_class.model_fit(self.model, self.data)

    def data_uploader(self):
        try:
            daily_data = DataExtractor()

            my_sql = MySql()

            today_data = daily_data.MyExecutor()
            self.data = None
            if not today_data.empty:
                today_data_list = list(today_data.iloc[0])
                my_sql.MyExecutor(today_data_list)

        except Exception as e:
            print(e)
