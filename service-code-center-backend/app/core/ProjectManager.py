import asyncio
import copy

from app.dto.project.CreateProjectDto import CreateProjectDto
from app.dto.project.GetProjectDto import GetProjectDto
from app.dto.project.PatchProjectDto import PatchProjectDto

from app.core.ProjectInfoManager import project_info_manager_instance
from app.core.ProjectExecutionManager import project_execution_manager_instance


# 중복 코드
# dict -> dto 필요
class ProjectManager:
    project_info_manager = project_info_manager_instance
    project_execution_manager = project_execution_manager_instance
    
    def create_project(self, create_project_dto: CreateProjectDto):
        project_info_dto = project_info_manager_instance.create_project(create_project_dto)
        project_dto = {
                "id": project_info_dto["id"],
                "name": project_info_dto["name"],
                "description": project_info_dto["description"],
                "conda_environment": project_info_dto["conda_environment"],
                "target_state": project_info_dto["target_state"],
                "current_state": project_execution_manager_instance.check_running_project(project_info_dto["id"])
        }
        return project_dto
    
    def get_project(self, id_):
        project_info_dto = project_info_manager_instance.get_project(id_)
        project_dto = {
                "id": project_info_dto["id"],
                "name": project_info_dto["name"],
                "description": project_info_dto["description"],
                "conda_environment": project_info_dto["conda_environment"],
                "target_state": project_info_dto["target_state"],
                "current_state": project_execution_manager_instance.check_running_project(project_info_dto["id"])
        }
        return project_dto

    def get_projects(self):
        projects = []
        projects_info = project_info_manager_instance.get_projects()
        for project_info_dto in projects_info:
            projects.append({
                "id": project_info_dto["id"],
                "name": project_info_dto["name"],
                "description": project_info_dto["description"],
                "conda_environment": project_info_dto["conda_environment"],
                "target_state": project_info_dto["target_state"],
                "current_state": project_execution_manager_instance.check_running_project(project_info_dto["id"])
            })
        return projects

    def update_project(self, id_: int, patch_project_dto: PatchProjectDto):
        result = project_info_manager_instance.update_project(id_, patch_project_dto)
        # 임시 코드
        #if patch_project_dto.target_state == "stopped":
        #    project_execution_manager_instance.stop_project(id_)
        #if patch_project_dto.target_state == "running":
        #    project_execution_manager_instance.start_project(id_)
        return result

    def sync_project_states(self):
        # 이미 중지된 프로젝트 정리
        project_execution_manager_instance.collect_garbage_project_executor()
        #print("sync")
        # 삭제 및 반영
        for project in project_manager_instance.get_projects():
            if project["target_state"] == "stopped":
                if project_execution_manager_instance.check_running_project(project["id"]) == "running":
                    project_execution_manager_instance.stop_project(project["id"])
            elif project["target_state"] == "running":
                #print(project)
                #print(project_execution_manager_instance.check_running_project(project["id"]))
                if project_execution_manager_instance.check_running_project(project["id"]) == "stopped":
                    #print("start")
                    project_execution_manager_instance.start_project(project["id"])

    async def loop_sync_project_states(self):
        while True:
            self.sync_project_states()
            await asyncio.sleep(1)







project_manager_instance = ProjectManager()