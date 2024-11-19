import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.ProjectManager import project_manager_instance

# logging level
logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    asyncio.create_task(project_manager_instance.loop_sync_project_states())
    #await DataScenarioManager.get_instance(DataScenarioCenterSettings()).refresh_data_scenario()

    # asyncio.create_task(data_scenario_manager_instance.load_projects_dsm())
    #asyncio.create_task(data_scenario_manager_instance.async_loop())
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)
# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
