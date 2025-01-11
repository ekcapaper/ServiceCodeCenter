import pathlib
from typing import Optional

import yaml
import os


from fastapi import APIRouter, Depends

from starlette import status

from app.dto.ResponseDSC import ResponseDSC

from app.dto.project.CreateProjectDto import CreateProjectDto
from app.dto.project.GetProjectDto import GetProjectDto
from app.dto.project.PatchProjectDto import PatchProjectDto
from app.core.ProjectManager import project_manager_instance
from app.core.ServiceCodeCenterProjectManager import ServiceCodeCenterProjectManager
from app.dto.CamelModel import CamelModel

from fastapi import HTTPException
router = APIRouter()





async def get_service_code_center_project_manager() -> ServiceCodeCenterProjectManager:
    # 현재 작업 디렉토리
    current_dir = pathlib.Path.cwd()
    # 프로젝트 디렉토리
    projects_dir_path = current_dir.parent.parent / "projects"
    # 변환
    return ServiceCodeCenterProjectManager(projects_dir_path = projects_dir_path.absolute())

@router.get("/projects")
async def get_all_project_info(
        service_code_center_project_manager: ServiceCodeCenterProjectManager = Depends(get_service_code_center_project_manager)
)->ResponseDSC[list[GetProjectDto]]:
    """모든 프로젝트 목록 조회"""
    project_info_list = await service_code_center_project_manager.get_project_list()
    return ResponseDSC(
        data=project_info_list
    )

@router.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    service_code_center_project_manager: ServiceCodeCenterProjectManager = Depends(get_service_code_center_project_manager)
) -> ResponseDSC[GetProjectDto]:
    """프로젝트 조회 """
    project = await service_code_center_project_manager.get_project(project_id)
    return ResponseDSC(
        status="success",
        data=project
    )

@router.post("/projects/refresh")
async def refresh_project(
    service_code_center_project_manager: ServiceCodeCenterProjectManager = Depends(get_service_code_center_project_manager)
):
    await service_code_center_project_manager.refresh()
    return ResponseDSC(
        status="success",
    )

# 📌 프로젝트 생성 요청 데이터 모델
class CreateProjectRequest(CamelModel):
    name: str
    description: str
    entrypoint: str

# 📌 프로젝트 수정 요청 데이터 모델
class PatchProjectRequest(CamelModel):
    name: Optional[str] = None
    description: Optional[str] = None
    entrypoint: Optional[str] = None


@router.patch("/projects/{project_id}", response_model=ResponseDSC)
async def patch_project(project_id: int,
                        request: PatchProjectRequest,
                        service_code_center_project_manager: ServiceCodeCenterProjectManager = Depends(get_service_code_center_project_manager)):
    try:
        await service_code_center_project_manager.patch_project(
            project_id=project_id,
            name=request.name,
            description=request.description,
            entrypoint=request.entrypoint
        )
        return ResponseDSC(status="success", data={"message": f"프로젝트 ID {project_id}가 수정되었습니다."})
    except KeyError:
        raise HTTPException(status_code=404, detail=f"ID가 {project_id}인 프로젝트가 존재하지 않습니다.")
    except FileExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프로젝트 수정 중 오류가 발생했습니다: {str(e)}")



@router.post("/projects", response_model=ResponseDSC)
async def create_project(
    request: CreateProjectRequest,
    service_code_center_project_manager: ServiceCodeCenterProjectManager = Depends(get_service_code_center_project_manager)
):
    try:
        await service_code_center_project_manager.create_project(
            name=request.name,
            description=request.description,
            entrypoint=request.entrypoint
        )
        return ResponseDSC(status="success", data={"message": f"프로젝트 '{request.name}'가 생성되었습니다."})
    except FileExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프로젝트 생성 중 오류가 발생했습니다: {str(e)}")
