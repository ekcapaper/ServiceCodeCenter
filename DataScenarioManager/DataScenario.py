class DataScenario:
    def __init__(self, name, description, conda_environment, script_path):
        self.__name = name
        self.__description = description
        self.__conda_environment = conda_environment
        self.__script_path = script_path

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def conda_environment(self):
        return self.__conda_environment

    @property
    def script_path_str(self):
        return str(self.__script_path)
