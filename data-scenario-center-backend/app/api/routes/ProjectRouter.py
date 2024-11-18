from fastapi import FastAPI, Depends, APIRouter, HTTPException
from pydantic import BaseModel
import os
import json

from starlette import status

from app.dto.CamelModel import CamelModel
from app.dto.ResponseDSC import ResponseDSC

router = APIRouter()

# 데이터 모델
class ProjectInfo(CamelModel):
    id: int
    name: str
    description: str = "No description available."
    conda_environment: str
    target_state: str  # "running" 또는 "stopped" 값
    current_state: str # "running" 또는 "stopped" 값

class PatchProjectDto(CamelModel):
    target_state: str

# Mock 데이터
mock_projects = [
    {
        "id": 0,
        "name": "projectA",
        "description": "This is Project A",
        "conda_environment": "development",
        "target_state": "running",
        "current_state": "running",
    },
    {
        "id": 1,
        "name": "projectB",
        "description": "This is Project B",
        "conda_environment": "development",
        "target_state": "running",
        "current_state": "stopped",
    }
]

class CreateProjectDto(CamelModel):
    name: str
    description: str = "No description available."
    conda_environment: str

@router.post("/projects", status_code=status.HTTP_201_CREATED, response_model=ResponseDSC)
def create_projects(create_project_dto: CreateProjectDto):
    global mock_projects
    mock_projects.append({
        "id": len(mock_projects),
        "name": create_project_dto.name,
        "description": create_project_dto.description,
        "conda_environment": create_project_dto.conda_environment,
        "target_state": "stopped",
        "current_state": "stopped",
    })
    return ResponseDSC(
        status="success"
    )


# API 엔드포인트 구현
@router.get("/projects")
def get_all_project_info() -> ResponseDSC[list[ProjectInfo]]:
    """모든 프로젝트 목록 조회"""
    return ResponseDSC(
        data=mock_projects
    )

@router.get("/projects/{project_id}")
def get_project(project_id: int) -> ResponseDSC[ProjectInfo]:
    """프로젝트 조회 """
    if project_id < 0 or project_id >= len(mock_projects):
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = mock_projects[project_id]
    return ResponseDSC(
        status="success",
        data=project_data
    )

@router.patch("/projects/{project_id}")
def update_project_state(project_id: int, patch_project_state: PatchProjectDto) -> ResponseDSC[ProjectInfo]:
    if project_id < 0 or project_id >= len(mock_projects):
        raise HTTPException(status_code=404, detail="Project state not found")
    mock_projects[project_id]["target_state"] = patch_project_state.target_state
    return ResponseDSC(
        data=mock_projects[project_id]
    )

@router.post("/projects/apply")
def apply_project_states() -> dict[str, str]:
    """선언된 상태를 적용하여 시스템 동기화"""
    return {"status": "applied", "message": "System updated to desired states"}

@router.post("/projects/refresh")
def refresh_project_states() -> dict[str, str]:
    return {"status": "refreshed", "message": "System updated to desired states"}

@router.get("/projects/hash")
def get_projects_hash():
    return "HASH-MOCK"
