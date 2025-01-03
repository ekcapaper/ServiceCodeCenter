import pathlib
import random

import aiofiles
import yaml
import os

from app.dto.project.CreateProjectDto import CreateProjectDto
from app.dto.project.PatchProjectDto import PatchProjectDto

class ProjectInfoManager:
    def __init__(self):
        self.projects = {}
        self.project_path = "./"
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
        project_path = self.project_path
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
                self.projects[data_scenario_data["id"]] ={
                    "id": data_scenario_data["id"],
                    "name": data_scenario_data["name"],
                    "description": data_scenario_data["description"],
                    "conda_environment": data_scenario_data["conda-environment"],
                    "target_state": data_scenario_data["target-state"],
                    "script_path": pathlib.Path(str(yaml_file)).parent / "main.py",
                    "cwd": pathlib.Path(str(yaml_file)).parent
                }
            except KeyError as ke:
                # temp
                print(ke)

    def create_project(self, create_project_dto:CreateProjectDto):
        project_one_path = (pathlib.Path("/app/app/projects") / create_project_dto.name)
        project_one_path.mkdir(parents=True)

        yaml.dump(create_project_dto, open(project_one_path / "project.yaml", 'w'), default_flow_style=False)

        data = {
            'project': {
                'id': random.randint(10000, 10000000000),
                'name': create_project_dto.name,
                'description': create_project_dto.description,
                'conda-environment': create_project_dto.conda_environment,
                'target-state': 'stopped'
            }
        }

        # YAML 파일로 저장
        yaml_file_name = project_one_path / "project.yaml"
        with open(yaml_file_name, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)

        py_file_name = project_one_path / "main.py"
        with open(py_file_name, 'w') as file:
            pass

        self.load_projects_dsm()
        return self.projects[data["project"]["id"]]

    def get_project(self, id_):
        return self.projects[id_]

    def get_projects(self):
        return list(self.projects.values())

    def update_project(self, id_: int, patch_project_dto:PatchProjectDto):
        self.projects[id_]["target_state"] = patch_project_dto.target_state

        #
        project_setting_path = pathlib.Path(self.projects[id_]["cwd"]) / "project.yaml"

        # YAML 파일 불러오기
        with open(project_setting_path, 'r') as file:
            data = yaml.safe_load(file)

        # target-state 변경
        data['project']['target-state'] = patch_project_dto.target_state

        # 변경된 내용을 YAML 파일에 저장
        with open(project_setting_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)


project_info_manager_instance = ProjectInfoManager()
project_info_manager_instance.load_projects_dsm()