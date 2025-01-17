import os
import yaml
import pathlib
import loguru
from app.core.ServiceCodeCenterProject import ServiceCodeCenterProject

def convert_project_to_dto(project):
    return {
        "id": project.id_,
        "name": project.name,
        "description": project.description,
        "entrypoint": project.entrypoint,
        "working_directory": str(project.working_directory)
    }

class ServiceCodeCenterProjectManager:
    __service_code_center_projects = {}

    def __init__(self, projects_dir_path:pathlib.Path):
        self.__projects_dir_path = projects_dir_path

    def __get_project_yaml_path_list(self):
        yaml_file_path_list = []
        for root, dirs, files in os.walk(self.__projects_dir_path):
            for file in files:
                if file.endswith('project.yaml'):
                    yaml_file_path_list.append(os.path.join(root, file))
        return yaml_file_path_list

    def __load_project_yaml(self, project_yaml_path, i):
        with open(project_yaml_path, mode='r') as file:
            contents = file.read()
            contents_dict = yaml.safe_load(contents)

            yaml_file_path_obj = pathlib.Path(project_yaml_path)

            service_code_project = ServiceCodeCenterProject(
                id_=i,
                name=yaml_file_path_obj.parent.name,
                description=contents_dict["project"]["description"],
                entrypoint=contents_dict["project"]["entrypoint"],
                working_directory=yaml_file_path_obj.parent
            )
            return service_code_project

    async def refresh(self):
        project_yaml_path_list = self.__get_project_yaml_path_list()
        for i, project_yaml_path in enumerate(project_yaml_path_list):
            try:
                service_code_project = self.__load_project_yaml(project_yaml_path, i)
                self.__service_code_center_projects[service_code_project.id_] = service_code_project
            except KeyError as e:
                loguru.logger.error(e)

    async def get_project_list(self):
        return map(convert_project_to_dto,self.__service_code_center_projects.values())

    async def get_project(self, project_id):
        return convert_project_to_dto(self.__service_code_center_projects[project_id])

    async def create_project(self, name: str, description: str, entrypoint: str):
        """
        새로운 프로젝트를 생성합니다.
        """
        project_dir = self.__projects_dir_path / name

        if project_dir.exists():
            raise FileExistsError(f"프로젝트 '{name}'가 이미 존재합니다.")

        project_dir.mkdir(parents=True, exist_ok=True)

        project_yaml_path = project_dir / "project.yaml"

        project_data = {
            "project": {
                "description": description,
                "entrypoint": entrypoint
            }
        }

        with open(project_yaml_path, 'w') as file:
            yaml.dump(project_data, file)

        loguru.logger.info(f"프로젝트 '{name}'가 생성되었습니다.")
        await self.refresh()

    async def patch_project(self, project_id: int, name: str = None, description: str = None, entrypoint: str = None):
        """
        기존 프로젝트의 정보를 업데이트합니다.
        """
        if project_id not in self.__service_code_center_projects:
            raise KeyError(f"ID가 {project_id}인 프로젝트가 존재하지 않습니다.")

        project = self.__service_code_center_projects[project_id]
        project_yaml_path = project.working_directory / "project.yaml"
        print(project)

        with open(project_yaml_path, 'r') as file:
            project_data = yaml.safe_load(file)

        if description:
            project_data["project"]["description"] = description
        if entrypoint:
            project_data["project"]["entrypoint"] = entrypoint

        with open(project_yaml_path, 'w') as file:
            yaml.dump(project_data, file)

        if name and project.name != name:
            new_project_dir = self.__projects_dir_path / name
            if new_project_dir.exists():
                raise FileExistsError(f"프로젝트 이름 '{name}'이 이미 존재합니다.")
            project.working_directory.rename(new_project_dir)

        loguru.logger.info(f"프로젝트 ID {project_id}가 수정되었습니다.")

        await self.refresh()