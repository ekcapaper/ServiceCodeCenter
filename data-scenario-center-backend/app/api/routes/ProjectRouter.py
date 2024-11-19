from fastapi import APIRouter

from starlette import status

from app.dto.ResponseDSC import ResponseDSC

from app.dto.project.CreateProjectDto import CreateProjectDto
from app.dto.project.GetProjectDto import GetProjectDto
from app.dto.project.PatchProjectDto import PatchProjectDto
from app.core.ProjectManager import project_manager_instance

router = APIRouter()

@router.post("/projects", status_code=status.HTTP_201_CREATED, response_model=ResponseDSC)
def create_projects(create_project_dto: CreateProjectDto):
    project = project_manager_instance.create_project(create_project_dto)
    return ResponseDSC(
        status="success",
        data=project,
    )


# API 엔드포인트 구현
@router.get("/projects")
def get_all_project_info() -> ResponseDSC[list[GetProjectDto]]:
    """모든 프로젝트 목록 조회"""
    projects = project_manager_instance.get_projects()
    return ResponseDSC(
        data=projects
    )

@router.get("/projects/{project_id}")
def get_project(project_id: int) -> ResponseDSC[GetProjectDto]:
    """프로젝트 조회 """
    project = project_manager_instance.get_project(project_id)
    return ResponseDSC(
        status="success",
        data=project
    )

@router.patch("/projects/{project_id}")
def update_project_state(project_id: int, patch_project_state: PatchProjectDto) -> ResponseDSC[GetProjectDto]:
    project_manager_instance.update_project(project_id, patch_project_state)
    return ResponseDSC(
        data=project_manager_instance.get_project(project_id)
    )
