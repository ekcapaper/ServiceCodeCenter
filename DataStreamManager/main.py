# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

import asyncio
from watchfiles import awatch
import yaml


async def handle_changes(changes):
    for change in changes:
        action, path = change
        if action in ('added', 'modified'):
            print(f'파일이 {action}되었습니다: {path}')

async def watch_yaml_files(directory):
    async for changes in awatch(directory, filter=lambda p: p.endswith('.yaml')):
        await handle_changes(changes)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)

# GET 요청에 대한 경로
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
