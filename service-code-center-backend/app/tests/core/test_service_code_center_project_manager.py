import pytest
import tempfile
import os
import pathlib
import yaml
from app.core.ServiceCodeCenterProject import ServiceCodeCenterProject
from app.core.ServiceCodeCenterProjectManager import ServiceCodeCenterProjectManager


@pytest.fixture
def temp_projects_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        projects_dir = pathlib.Path(temp_dir)

        # 프로젝트 1 생성
        project1_dir = projects_dir / "Project1"
        project1_dir.mkdir(parents=True, exist_ok=True)
        project1_yaml = project1_dir / "project.yaml"
        project1_data = {
            "project": {
                "description": "Description for Project 1",
                "entrypoint": "main.py"
            }
        }
        with open(project1_yaml, "w") as f:
            yaml.safe_dump(project1_data, f)

        # 프로젝트 2 생성
        project2_dir = projects_dir / "Project2"
        project2_dir.mkdir(parents=True, exist_ok=True)
        project2_yaml = project2_dir / "project.yaml"
        project2_data = {
            "project": {
                "description": "Description for Project 2",
                "entrypoint": "app.py"
            }
        }
        with open(project2_yaml, "w") as f:
            yaml.safe_dump(project2_data, f)

        yield projects_dir


@pytest.mark.asyncio
async def test_refresh_and_get_project_list(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)
    await manager.refresh()

    projects = list(await manager.get_project_list())
    assert len(projects) == 2

    project1 = projects[0]
    assert project1["name"] == "Project1"
    assert project1["description"] == "Description for Project 1"
    assert project1["entrypoint"] == "main.py"

    project2 = projects[1]
    assert project2["name"] == "Project2"
    assert project2["description"] == "Description for Project 2"
    assert project2["entrypoint"] == "app.py"


@pytest.mark.asyncio
async def test_get_project(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)
    await manager.refresh()

    project = await manager.get_project(0)
    assert project["name"] == "Project1"
    assert project["description"] == "Description for Project 1"
    assert project["entrypoint"] == "main.py"

@pytest.mark.asyncio
async def test_create_project(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)

    # 새 프로젝트 생성
    await manager.create_project("TestProject", "테스트 프로젝트입니다.", "main.py")

    # 프로젝트 디렉토리 및 파일 존재 확인
    project_dir = temp_projects_dir / "TestProject"
    assert project_dir.exists(), "프로젝트 디렉토리가 생성되지 않았습니다."

    project_yaml_path = project_dir / "project.yaml"
    assert project_yaml_path.exists(), "`project.yaml` 파일이 생성되지 않았습니다."

    # YAML 파일 내용 확인
    with open(project_yaml_path, 'r') as file:
        project_data = yaml.safe_load(file)
        assert project_data["project"]["description"] == "테스트 프로젝트입니다."
        assert project_data["project"]["entrypoint"] == "main.py"

    # 생성된 프로젝트 목록 확인
    projects = list(await manager.get_project_list())
    assert len(projects) == 3
    assert projects[2]["name"] == "TestProject"


@pytest.mark.asyncio
async def test_patch_project(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)

    # 프로젝트 생성
    await manager.create_project("PatchProject", "패치 전 설명", "start.py")

    # 생성된 프로젝트 확인
    projects = list(await manager.get_project_list())
    assert len(projects) == 3
    project_id = projects[0]["id"]

    # 프로젝트 정보 수정
    await manager.patch_project(project_id, description="패치 후 설명", entrypoint="run.py")

    # 수정된 YAML 파일 내용 확인
    project_yaml_path = temp_projects_dir / "PatchProject" / "project.yaml"
    with open(project_yaml_path, 'r') as file:
        project_data = yaml.safe_load(file)
        assert project_data["project"]["description"] == "패치 후 설명"
        assert project_data["project"]["entrypoint"] == "run.py"

    # 이름 변경 테스트
    await manager.patch_project(project_id, name="RenamedProject")
    renamed_project_dir = temp_projects_dir / "RenamedProject"
    assert renamed_project_dir.exists(), "프로젝트 이름이 변경되지 않았습니다."

    # 변경된 프로젝트 확인
    projects = list(await manager.get_project_list())
    assert projects[2]["name"] == "RenamedProject"
    assert projects[2]["description"] == "패치 후 설명"


@pytest.mark.asyncio
async def test_create_duplicate_project(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)

    # 동일한 이름의 프로젝트 2개 생성 시도
    await manager.create_project("DuplicateProject", "첫 번째 프로젝트", "main.py")

    with pytest.raises(FileExistsError):
        await manager.create_project("DuplicateProject", "두 번째 프로젝트", "run.py")


@pytest.mark.asyncio
async def test_patch_nonexistent_project(temp_projects_dir):
    manager = ServiceCodeCenterProjectManager(temp_projects_dir)

    # 존재하지 않는 프로젝트 수정 시도
    with pytest.raises(KeyError):
        await manager.patch_project(999, description="없는 프로젝트 수정")