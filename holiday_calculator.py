from datetime import timedelta
from pandas import DataFrame


class Holidays:
    def __init__(self):
        self.delta = timedelta(days=1)

    def calculate(self, start, end):
        try:
            ds = []
            while start != end:
                if start.weekday() == 5 or start.weekday() == 6:
                    ds.append(start)
                start = start + self.delta

            holidays = DataFrame({'ds': ds})
            holidays['holiday'] = 'weekend'

            return holidays
        except Exception as e:
            print(e)
            return None
