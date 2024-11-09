import os
import hashlib
import asyncio
import logging
import os
import sys
import pathlib
from typing import Optional

import aiofiles
import yaml
from fastapi import Depends
from watchfiles import awatch

class ProjectInfoManager:
    def __init__(self, project_folder_path):
        self.project_folder_path = project_folder_path
        self.projects_info = {}

    def convert_project_info_to_project_info_dto(self, project_info):
        pass

    def get_project(self, project_uid):
        pass

    def get_projects(self):
        pass


    async def refresh_projects_info(self):
        async def load_yaml(file_path):
            async with aiofiles.open(file_path, mode='r') as file:
                contents = await file.read()
                return yaml.safe_load(contents)

        def search_paths_data_scenario_yaml_file(directory):
            yaml_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('data-scenario.yaml'):
                        yaml_files.append(os.path.join(root, file))
            return yaml_files

        # 1. stop executors
        for data_scenario_name in self.__data_scenario_executors.keys():
            await self.stop_data_scenario(data_scenario_name)

        # 2. reset
        self.__data_scenario_executors = {}

        # 3. reload
        data_scenario_yaml_paths = search_paths_data_scenario_yaml_file(
            self.__data_scenario_center_settings.projects_path)
        for data_scenario_yaml_path in data_scenario_yaml_paths:
            data_scenario_yaml_path = str(data_scenario_yaml_path)
            try:
                yaml_dict = await load_yaml(data_scenario_yaml_path)
                script_path = pathlib.Path(str(data_scenario_yaml_path)).parent / "main.py"
                data_scenario_data = yaml_dict["DataScenario"]
                data_scenario = DataScenario(
                    name=data_scenario_data["name"],
                    description=data_scenario_data["description"],
                    conda_environment=data_scenario_data["conda-environment"],
                    script_path=script_path
                )
                data_scenario_executor = DataScenarioExecutor(data_scenario)
                self.__data_scenario_executors[data_scenario.name] = data_scenario_executor
            except KeyError as ke:
                self.__logger.error(f"{data_scenario_yaml_path} is not enough values")
                self.__logger.error(ke)

    def get_project_info(self, project_name):
        """특정 프로젝트 정보를 반환"""
        return self.projects_info.get(project_name, None)


project_info_manager = ProjectInfoManager("./")