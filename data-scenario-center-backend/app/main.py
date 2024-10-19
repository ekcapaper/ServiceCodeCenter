import asyncio
from contextlib import asynccontextmanager
from fastapi import HTTPException
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from app.core.DataScenarioManager import data_scenario_manager_instance
import logging

# logging level
logging.basicConfig(level=logging.DEBUG)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    asyncio.create_task(data_scenario_manager_instance.load_projects_dsm())
    asyncio.create_task(data_scenario_manager_instance.async_loop())
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
