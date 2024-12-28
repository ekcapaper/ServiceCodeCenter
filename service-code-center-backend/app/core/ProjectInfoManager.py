import pathlib

import aiofiles
import yaml
import os

from app.dto.project.CreateProjectDto import CreateProjectDto
from app.dto.project.PatchProjectDto import PatchProjectDto

class ProjectInfoManager:
    def __init__(self):
        self.projects = []
        '''
        self.projects = [
            {
                "id": 0,
                "name": "projectA",
                "description": "This is Project A",
                "conda_environment": "development",
                "target_state": "stopped",
            },
            {
                "id": 1,
                "name": "projectB",
                "description": "This is Project B",
                "conda_environment": "development",
                "target_state": "stopped",
            }
        ]
        '''

    def load_projects_dsm(self):
        project_path = "./"
        def load_yaml(file_path):
            with open(file_path, mode='r') as file:
                contents = file.read()
                return yaml.safe_load(contents)

        def get_dsm_yaml_file_paths(directory):
            yaml_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('project.yaml'):
                        yaml_files.append(os.path.join(root, file))
            return yaml_files

        # 1. get paths
        yaml_files = get_dsm_yaml_file_paths(project_path)

        # 2. load yaml
        for yaml_file in yaml_files:
            try:
                yaml_dict = load_yaml(yaml_file)
                data_scenario_data = yaml_dict["project"]
                self.projects.append({
                    "id": data_scenario_data["id"],
                    "name": data_scenario_data["name"],
                    "description": data_scenario_data["description"],
                    "conda_environment": data_scenario_data["conda-environment"],
                    "target_state": data_scenario_data["target-state"],
                    "script_path": pathlib.Path(str(yaml_file)).parent / "main.py",
                    "cwd": pathlib.Path(str(yaml_file)).parent
                })
            except KeyError as ke:
                # temp
                print(ke)

    def create_project(self, create_project_dto:CreateProjectDto):
        # 코드 수정 필요
        # ID 관련 해서 겹치지 않도록
        id_ = len(self.projects)
        self.projects.append(
            {
                "id": id_,
                "name": create_project_dto.name,
                "description": create_project_dto.description,
                "conda_environment": create_project_dto.conda_environment,
                "target_state": "stopped",
            }
        )
        return self.projects[id_]

    def get_project(self, id_):
        return self.projects[id_]

    def get_projects(self):
        return self.projects

    def update_project(self, id_: int, patch_project_dto:PatchProjectDto):
        self.projects[id_]["target_state"] = patch_project_dto.target_state



project_info_manager_instance = ProjectInfoManager()
project_info_manager_instance.load_projects_dsm()