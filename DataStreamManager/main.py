# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

import asyncio
from watchfiles import awatch
import yaml


async def watch_files():
    async for changes in awatch('/path/to/dir'):
        print(changes)

async def background_temp():
    while True:
        print("abcd")
        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    asyncio.create_task(background_temp())
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)

# GET 요청에 대한 경로
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
