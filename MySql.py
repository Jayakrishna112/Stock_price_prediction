import pyodbc
from pandas import read_sql
import logging as lg


class MySql:
    __connected = False
    _connection = None
    error = False

    def __init__(self):
        try:
            lg.basicConfig(filename='logfile.log', level=lg.INFO, format='%(asctime)s %(message)s')
            self.__password = 'Invalid@1330'
            self.__db_name = 'msqldatabase'
            self.__server = 'tcp:mysqlserver1330.database.windows.net'
            self.__db_user = 'azureuser'
            self.db_driver = '{ODBC Driver 18 for SQl Server}'
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

        self.disconnect()

    def disconnect(self):
        try:
            if not self.__connected:
                self._connection.close()

        except pyodbc.Error as e:
            lg.error('Error in MySql.disconnect() :', e)
