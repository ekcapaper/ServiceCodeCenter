from fastapi import FastAPI, Depends, APIRouter, HTTPException
from pydantic import BaseModel
import os
import json

from app.dto.CamelModel import CamelModel
from app.dto.ResponseDSC import ResponseDSC

router = APIRouter()

# 데이터 모델
class ProjectInfo(CamelModel):
    name: str
    description: str = "No description available."
    conda_environment: str

class ProjectState(CamelModel):
    name: str
    target_state: str  # "running" 또는 "stopped" 값
    current_state: str # "running" 또는 "stopped" 값

class PatchProjectState(CamelModel):
    target_state: str

# Mock 데이터
mock_projects = [
    {
        "name": "projectA",
        "description": "This is Project A",
        "conda_environment": "development",
    },
    {
        "name": "projectB",
        "description": "This is Project B",
        "conda_environment": "development",
    }
]

mock_project_state = [
    {
        "name": "projectA",
        "target_state": "running",
        "current_state": "running",
    },
    {
        "name": "projectB",
        "target_state": "running",
        "current_state": "running",
    }
]





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
    return ResponseDSC(
        data=mock_projects[project_id]
    )

@router.get("/projects/state")
def get_all_project_state() -> ResponseDSC[list[ProjectState]]:
    """모든 프로젝트 상태 조회"""
    return ResponseDSC(
        data=mock_project_state
    )

@router.get("/projects/{project_id}/state")
def get_project_state(project_id: int) -> ResponseDSC[ProjectState]:
    """프로젝트 상태 조회"""
    if project_id < 0 or project_id >= len(mock_project_state):
        raise HTTPException(status_code=404, detail="Project state not found")
    return ResponseDSC(
        data=mock_project_state[project_id]
    )

@router.patch("/projects/{project_id}/state")
def update_project_state(project_id: int, patch_project_state: PatchProjectState) -> ResponseDSC[ProjectState]:
    if project_id < 0 or project_id >= len(mock_project_state):
        raise HTTPException(status_code=404, detail="Project state not found")
    mock_project_state[project_id]["target_state"] = patch_project_state.target_state
    return ResponseDSC(
        data=mock_project_state[project_id]
    )

@router.post("/projects/apply")
def apply_project_states() -> dict[str, str]:
    """선언된 상태를 적용하여 시스템 동기화"""
    return {"status": "applied", "message": "System updated to desired states"}

@router.post("/projects/refresh")
def refresh_project_states() -> dict[str, str]:
    return {"status": "refreshed", "message": "System updated to desired states"}

@router.post("/projects/{project_id}/delete")
def delete_project_states(project_id: int) -> dict[str, str]:
    if project_id < 0 or project_id >= len(mock_project_state):
        raise HTTPException(status_code=404, detail="Project state not found")
    return {"status": "deleted", "message": "Project has been deleted"}

@router.get("/projects/hash")
def get_projects_hash():
    return "HASH-MOCK"
