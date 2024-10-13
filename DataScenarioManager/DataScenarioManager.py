import asyncio
import os
import aiofiles

import yaml
from watchfiles import awatch
import os

import aiofiles
import yaml
from watchfiles import awatch
from DataScenario import DataScenario
from RunningDataScenario import RunningDataScenario

class DataScenarioManager:
    def __init__(self):
        self.__projects_path = "./projects"
        self.__data_scenario_list = []
        self.__running_data_scenario_list = []

    async def load_projects_dsm(self):
        self.__data_scenario_list = []
        async def load_yaml(file_path):
            async with aiofiles.open(file_path, mode='r') as file:
                contents = await file.read()
                return yaml.safe_load(contents)

        def list_yaml_files(directory):
            yaml_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('dsm.yaml'):
                        yaml_files.append(os.path.join(root, file))
            return yaml_files

        yaml_files = list_yaml_files(self.__projects_path)
        for yaml_file in yaml_files:
            yaml_dict = await load_yaml(yaml_file)
            self.__data_scenario_list.append(
                DataScenario(
                    name=yaml_dict["name"],
                    description=yaml_dict["description"]
                )
            )

    @property
    def data_scenario_list(self):
        return self.__data_scenario_list

    def run_scenario(self, scenario_name):
        data_scenario = list(filter(lambda scenario: scenario.name == scenario_name, self.__data_scenario_list))[0]
        self.__running_data_scenario_list.append(RunningDataScenario(data_scenario))

    @property
    def running_data_scenario_list(self):
        return self.__running_data_scenario_list

    async def watch_project_dsm(self):
        async for changes in awatch(self.__projects_path):
            for change in changes:
                pass

if __name__ == '__main__':
    dsm = DataScenarioManager()
    asyncio.run(dsm.load_projects_dsm())
