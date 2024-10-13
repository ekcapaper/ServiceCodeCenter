import asyncio
import json
import os
import subprocess
from typing import List

import aiofiles

from contextlib import asynccontextmanager

import uvicorn
import yaml
from fastapi import FastAPI, HTTPException
from watchfiles import awatch
from pydantic import BaseModel

from DataScenarioManager import DataScenarioManager

data_scenario_manager_instance = DataScenarioManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    asyncio.create_task(data_scenario_manager_instance.watch_project_dsm())
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

# 시나리오들이 위치한 기본 경로
SCENARIO_BASE_PATH = './scenarios'


# 시나리오 목록 조회
class DataScenarioDto(BaseModel):
    name: str
    description: str

class ResponseGetDataScenarios(BaseModel):
    data_scenarios: List[DataScenarioDto]

@app.get("/scenarios")
def get_data_scenarios():
    data_scenario_dto_list = list(map(lambda data_scenarios:DataScenarioDto(name=data_scenarios.name, description=data_scenarios.description),data_scenario_manager_instance.data_scenario_list))
    return {
        "data_scenarios": data_scenario_dto_list
    }

class RunningDataScenarioDto(BaseModel):
    uuid: str

class ResponseRunningDataScenarios(BaseModel):
    running_data_scenarios: List[RunningDataScenarioDto]

@app.get("/running-scenarios")
def get_running_scenarios():
    running_data_scenarios = list(map(lambda running_data_scenarios:RunningDataScenarioDto(uuid=running_data_scenarios.uuid), data_scenario_manager_instance.running_data_scenario_list))
    return {
        "running_data_scenarios": running_data_scenarios
    }

# 시나리오 시작
@app.post("/scenarios/{scenario_name}/start")
def start_scenario(scenario_name: str):
    data_scenario_manager_instance.run_scenario(scenario_name)
    return {"message": "Scenario started", "uid": "1234"}


# 시나리오 정지
@app.post("/scenarios/{scenario_name}/stop")
def stop_scenario(scenario_uid: str):
    data_scenario_manager_instance.stop_scenario(scenario_uid)
    return {"message": "Scenario stopped", "uid": "1234"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
