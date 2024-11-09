from fastapi import APIRouter, Depends

from app.dto.CamelModel import CamelModel
from app.dto.ResponseDSC import ResponseDSC
from app.core.DataScenarioManager import DataScenarioManager, get_data_scenario_manager_fastapi

router = APIRouter()

# 시나리오 목록 조회
# 추가된 데이터의 반영 필요
class DataScenarioDto(CamelModel):
    name: str
    description: str
    conda_environment: str
    script_path: str
    is_running: bool = False


@router.get("/scenarios", response_model=ResponseDSC[list[DataScenarioDto]])
async def get_data_scenarios(
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager_fastapi),
):
    data_scenario_dto_list = list(map(
        lambda data_scenario:DataScenarioDto(
            name=data_scenario.name,
            description=data_scenario.description,
            conda_environment=data_scenario.conda_environment,
            script_path=data_scenario.script_path_str
        ), data_scenario_manager.data_scenarios)
    )
    return {
        "success": True,
        "data": data_scenario_dto_list,
        "error": None
    }
@router.get("/scenarios/{scenario_name}", response_model=ResponseDSC[DataScenarioDto])
async def get_data_scenario(
    scenario_name: str,
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager_fastapi),
):
    data_scenario = data_scenario_manager.get_data_scenario(scenario_name).data_scenario
    return {
        "success": True,
        "data": DataScenarioDto(
            name=data_scenario.name,
            description=data_scenario.description,
            conda_environment=data_scenario.conda_environment,
            script_path=data_scenario.script_path_str
        ),
        "error": None
    }


@router.post("/scenarios/{scenario_name}/start")
async def start_scenario(
    scenario_name: str,
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager_fastapi),
):
    data_scenario_manager.start_data_scenario(scenario_name)
    return ResponseDSC(success=True)


# 시나리오 정지
@router.post("/scenarios/{scenario_name}/stop")
async def stop_scenario(
    scenario_name: str,
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager_fastapi),
):
    await data_scenario_manager.stop_data_scenario(scenario_name)
    return ResponseDSC(
        success=True,
    )

@router.post("/scenarios/refresh")
async def refresh_scenario(
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager_fastapi),
):
    await data_scenario_manager.refresh_data_scenario()
    return ResponseDSC(
        success=True,
    )
