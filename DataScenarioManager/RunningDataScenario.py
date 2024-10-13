import datetime
from DataScenario import DataScenario

class RunningDataScenario:
    def __init__(self, data_scenario=DataScenario):
        self.__data_scenario = data_scenario
        self.__start_time = datetime.datetime.now()

    # subprocess + conda
    def run(self):
        while True:
            import time
            time.sleep(5)
