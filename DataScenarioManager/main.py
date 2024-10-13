import asyncio
import json
import os
import subprocess
import aiofiles

from contextlib import asynccontextmanager

import uvicorn
import yaml
from fastapi import FastAPI, HTTPException
from watchfiles import awatch





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
@app.get("/scenarios")
def list_scenarios():
    scenarios = []

    # 시나리오 폴더 탐색
    for scenario_name in os.listdir(SCENARIO_BASE_PATH):
        scenario_path = os.path.join(SCENARIO_BASE_PATH, scenario_name)
        scenario_json_path = os.path.join(scenario_path, "scenario.json")

        if os.path.isdir(scenario_path) and os.path.exists(scenario_json_path):
            with open(scenario_json_path, "r") as f:
                scenario_data = json.load(f)
                scenarios.append({
                    "name": scenario_data.get("name"),
                    "description": scenario_data.get("description")
                })

    return {"scenarios": scenarios}


# 특정 시나리오 상태 조회
@app.get("/scenarios/{scenario_name}/status")
def get_scenario_status(scenario_name: str):
    scenario_path = os.path.join(SCENARIO_BASE_PATH, scenario_name)
    if not os.path.exists(scenario_path):
        raise HTTPException(status_code=404, detail="Scenario not found")

    # 예를 들어, 시나리오가 실행 중인지 확인하는 방법 (단순 예시)
    pid_file = os.path.join(scenario_path, "pid")
    if os.path.exists(pid_file):
        return {"status": "running"}
    else:
        return {"status": "stopped"}


# 시나리오 시작
@app.post("/scenarios/{scenario_name}/start")
def start_scenario(scenario_name: str):
    scenario_path = os.path.join(SCENARIO_BASE_PATH, scenario_name)
    if not os.path.exists(scenario_path):
        raise HTTPException(status_code=404, detail="Scenario not found")

    # 가상 환경과 start 스크립트 경로
    venv_path = os.path.join(scenario_path, "venv", "bin", "activate")
    start_script_path = os.path.join(scenario_path, "start.sh")

    # 시나리오 실행 (예시로 start.sh 스크립트를 실행)
    command = f"source {venv_path} && bash {start_script_path}"
    process = subprocess.Popen(command, shell=True, cwd=scenario_path)

    # 실행된 프로세스 ID 기록 (단순한 PID 파일 생성 방식 사용)
    pid_file = os.path.join(scenario_path, "pid")
    with open(pid_file, "w") as f:
        f.write(str(process.pid))

    return {"message": "Scenario started", "pid": process.pid}


# 시나리오 정지
@app.post("/scenarios/{scenario_name}/stop")
def stop_scenario(scenario_name: str):
    scenario_path = os.path.join(SCENARIO_BASE_PATH, scenario_name)
    pid_file = os.path.join(scenario_path, "pid")

    if not os.path.exists(pid_file):
        raise HTTPException(status_code=404, detail="Scenario is not running")

    # PID를 읽어서 프로세스 종료
    with open(pid_file, "r") as f:
        pid = int(f.read())

    try:
        os.kill(pid, 9)  # 강제 종료
        os.remove(pid_file)  # PID 파일 삭제
        return {"message": "Scenario stopped"}
    except ProcessLookupError:
        raise HTTPException(status_code=404, detail="Process not found")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
