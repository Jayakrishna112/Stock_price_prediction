import datetime
import logging as lg
import urllib3
from pandas import to_datetime, errors
from bs4 import BeautifulSoup as Bs


class DataExtractor:
    url = None
    client_request = None
    _connected = False
    data = None
    parsed_data = None
    html_table = None
    Stocks_data = None

    def __init__(self):
        lg.basicConfig(filename="logfile.log", level=lg.INFO,
                       format='%(asctime)s %(message)s')
        self._today = datetime.datetime.today()
        self.__completed = False

    def url_modifier(self):
        # start =
        try:
            self.url = (
                f'https://www.investing.com/indices/s-p-cnx-nifty-historical-data')
        except Exception as e:
            lg.exception('Exception in DataExtractor.url_modifier() :', e)

    def client_connector(self):
        try:
            host = urllib3.PoolManager()
            self.client_request = host.request('GET', self.url)
            self._connected = True

        except urllib3.exceptions as e:
            lg.exception('Exception in DataExtractor.client_connector()', e)

    def html_parser(self):
        try:
            self.parsed_data = Bs(self.client_request.data, 'html.parser')

        except Exception as e:
            lg.exception('Exception in DataExtractor.html_parser() :', e)

    def section_selector(self):
        try:
            self.html_table = self.parsed_data.find_all('table',
                                                        {'class': 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4'})

        except Exception as e:
            lg.exception('Exception in DataExtractor.section_selector() :', e)

    def table_convertor(self):
        try:
            data = []
            for row in self.html_table[0].find_all('tr')[1:]:
                row_data = [td.text.strip() for td in row.find_all('td')]
                data.append(row_data)
            self.Stocks_data = data[0][:-2]
            self.Stocks_data[0] = to_datetime(self.Stocks_data[0])
            self.Stocks_data[1] = float(self.Stocks_data[1].replace(',', ''))
            self.Stocks_data[2] = float(self.Stocks_data[2].replace(',', ''))
            self.Stocks_data[3] = float(self.Stocks_data[3].replace(',', ''))
            self.Stocks_data[4] = float(self.Stocks_data[4].replace(',', ''))
            if self.Stocks_data[0].to_pydatetime().date() != self._today.date():
                self.Stocks_data = []
        except ... as e:
            lg.error('Error in DataExtractor.table_convertor() :', e)

    def MyExecutor(self):
        try:
            if not self.__completed:
                self.url_modifier()

                while not self._connected:
                    self.client_connector()

                self.html_parser()

                self.section_selector()

                self.table_convertor()

                return self.Stocks_data
        except ... as e:
            print(str(e))

