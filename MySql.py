import pyodbc
from pandas import read_sql
from decouple import config
import logging as lg


class MySql:
    __connected = False
    _connection = None
    error = False

    def __init__(self):
        try:
            lg.basicConfig(filename='logfile.log', level=lg.INFO, format='%(asctime)s %(message)s')
            self.__password = config('DB_PASSWORD')
            self.__db_name = config('DB_NAME')
            self.__server = config('SERVER')
            self.__db_user = config('DB_USER')
            self.db_driver = config('DB_DRIVER')
            self.connection_string = (f'DRIVER={self.db_driver};SERVER={self.__server};'
                                      f'DATABASE={self.__db_name};UID={self.__db_user};'
                                      f'PWD={self.__password}')
            self.error = False
        except Exception as e:
            self.error = True
            lg.exception('Error in MySQl.__init__() :', e)

    def connect(self):
        try:
            self._connection = pyodbc.connect(self.connection_string)
            self.__connected = True
            self.error = False
        except pyodbc.Error as e:
            self.error = True
            lg.error('Error in MySql.connect() :', e)

    def insert_data(self, values):
        try:
            if self.__connected:
                insert_query = ("INSERT INTO Stocks (Date, Close_Price, Open_Price, High_Price, Low_Price)"
                                " VALUES (?, ?, ? ,? , ?)")
                cursor = self._connection.cursor()
                cursor.execute(insert_query, values)
                lg.info('values successfully inserted into the table')
                cursor.close()
                self.__connected = self._connection.closed
                self.error = False

        except pyodbc.Error as e:
            self.error = True
            lg.error('Error in MySql.insert_data() :', e)

    def data_loader(self):
        try:
            stocks_data = None
            query = 'select * from Stocks'

            if not self.__connected:
                self.connect()

            if self.__connected:
                stocks_data = read_sql(query, self._connection)

            return stocks_data
        except pyodbc.Error as e:
            lg.error('Error in MySql.data_loader() :', e)

    def MyExecutor(self, mydata):
        while not self.__connected:
            self.connect()

        self.insert_data(mydata)

        if not self.error:
            self._connection.commit()
        else:
            self.MyExecutor(mydata)

        self._connection.close()

    def disconnect(self):
        try:
            if not self.__connected:
                self._connection.close()

        except pyodbc.Error as e:
            lg.error('Error in MySql.disconnect() :', e)
