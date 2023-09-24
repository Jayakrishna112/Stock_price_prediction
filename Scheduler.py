import logging as lg
import copy
from helper import HelperClass
import time


class Scheduler:
    def __init__(self):
        lg.basicConfig(filename='logfile.log', level=lg.INFO, format='%(asctime)s %(message)s')
        self.df = None
        self.model = None

    def schedule(self):
        helper = HelperClass()
        if time.strftime("%H:%M") == '17::00':
            helper.data_uploader()
        helper.Data_loader()
        self.df = copy.deepcopy(helper.data)
        helper.model_trainer()
        self.model = helper.model


def my_task(my_schedule):
    my_schedule.schedule()

