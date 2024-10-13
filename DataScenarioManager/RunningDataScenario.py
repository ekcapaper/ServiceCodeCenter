import datetime
import uuid

from DataScenario import DataScenario

class RunningDataScenario:
    def __init__(self, data_scenario=DataScenario):
        self.__data_scenario = data_scenario
        self.__start_time = datetime.datetime.now()
        self.__uid = str(uuid.uuid4())

    @property
    def uid(self):
        return self.__uid

    # subprocess + conda
    def run(self):
        while True:
            import time
            time.sleep(5)
