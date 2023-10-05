import datetime
import logging as lg
import urllib3
from pandas import read_html, to_datetime, errors
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
        lg.basicConfig(filename="logfile.log", level=lg.INFO, format='%(asctime)s %(message)s')
        self.__completed = False
        __delta = datetime.timedelta(days=1)
        _today = datetime.datetime.today()
        self.end_date = int(datetime.datetime.timestamp(_today))
        self.start_date = int(datetime.datetime.timestamp(_today - __delta))

    def url_modifier(self, start, end):
        try:
            self.url = (f'https://in.investing.com/indices/s-p-cnx-nifty-historical-data?'
                        f'end_date={end}&st_date={start}&interval_sec=daily')
        except Exception as e:
            lg.exception('Exception in DataExtractor.url_modifier() :',e)

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
            self.html_table = self.parsed_data.find_all('section',
                                                        {'class': 'js-table-wrapper common-table-comp scroll-view'})

        except Exception as e:
            lg.exception('Exception in DataExtractor.section_selector() :', e)

    def table_convertor(self):
        try:
            self.Stocks_data = read_html(str(self.html_table[0]))[0]
            self.Stocks_data["Date"] = to_datetime(self.Stocks_data['Date'])
            self.Stocks_data.drop(columns=['Volume', 'Chg%'], inplace=True)
        except errors as e:
            lg.error('Error in DataExtractor.table_convertor() :', e)

    def MyExecutor(self):
        try:
            if not self.__completed:
                self.url_modifier(self.start_date, self.end_date)

                while not self._connected:
                    self.client_connector()

                self.html_parser()

                self.section_selector()

                self.table_convertor()

                return self.Stocks_data
        except ... as e:
            print(str(e))
