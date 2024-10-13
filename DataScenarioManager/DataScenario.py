class DataScenario:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description