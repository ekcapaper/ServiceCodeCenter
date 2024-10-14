import asyncio
from contextlib import asynccontextmanager
from fastapi import HTTPException
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from DataScenarioManager import DataScenarioManager

data_scenario_manager_instance = DataScenarioManager(
    projects_path="./projects"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    asyncio.create_task(data_scenario_manager_instance.load_projects_dsm())
    asyncio.create_task(data_scenario_manager_instance.async_loop())
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

# 시나리오 목록 조회
class DataScenarioDto(BaseModel):
    name: str
    description: str
    conda_environment: str
    script_path: str


class DataScenarioListDto(BaseModel):
    data_scenario_list: List[DataScenarioDto]


def convert_data_scenario_to_data_scenario_dto(data_scenario):
    return DataScenarioDto(
        name=data_scenario.name,
        description=data_scenario.description,
        conda_environment=data_scenario.conda_environment,
        script_path=data_scenario.script_path,
    )


@app.get("/scenarios", response_model=DataScenarioListDto)
def get_data_scenarios():
    data_scenario_dto_list = list(
        map(convert_data_scenario_to_data_scenario_dto, data_scenario_manager_instance.get_data_scenario_list()))
    return {
        "data_scenario_list": data_scenario_dto_list
    }

class MessageDto(BaseModel):
    message: str

# 시나리오 시작
@app.post("/scenarios/{scenario_name}/start")
def start_scenario(scenario_name: str):
    result = data_scenario_manager_instance.run_scenario(scenario_name)
    if result:
        return {
            "message": "Request to start scenario",
        }
    else:
        raise HTTPException(status_code=404, detail="scenario not started")


class DataScenarioExecutorDto(BaseModel):
    name: str
    description: str
    conda_environment: str
    script_path: str
    uid: str


class DataScenarioExecutorListDto(BaseModel):
    data_scenario_executor_list: List[DataScenarioDto]


from DataScenarioExecutor import DataScenarioExecutor


def convert_data_scenario_executor_to_data_scenario_executor_dto(data_scenario_executor: DataScenarioExecutor):
    return DataScenarioExecutorDto(
        name=data_scenario_executor.data_scenario.name,
        description=data_scenario_executor.data_scenario.description,
        conda_environment=data_scenario_executor.data_scenario.conda_environment,
        script_path=data_scenario_executor.data_scenario.script_path,
        uid=data_scenario_executor.uid,
    )


@app.get("/scenarios/running", response_model=DataScenarioExecutorListDto)
def get_data_scenarios_running():
    data_scenario_executor_list = list(
        map(convert_data_scenario_executor_to_data_scenario_executor_dto,
            list(data_scenario_manager_instance.get_data_scenario_executor_dict().values())
        )
    )
    return {
        "data_scenario_executor_list": data_scenario_executor_list
    }

@app.get("/scenarios/running/{running_uid}")
def get_data_scenario_running(running_uid: str):
    try:
        return convert_data_scenario_executor_to_data_scenario_executor_dto(
            data_scenario_manager_instance.get_data_scenario_executor(running_uid)
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="scenario not found")

# 시나리오 정지
@app.post("/scenarios/running/{running_uid}/stop")
def stop_scenario(running_uid: str):
    data_scenario_manager_instance.stop_scenario(running_uid)
    return {"message": "Request to stop scenario"}

@app.post("/scenarios/running/{running_uid}/kill")
def stop_scenario(running_uid: str):
    data_scenario_manager_instance.stop_scenario(running_uid)
    return {"message": "Request to kill scenario"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
