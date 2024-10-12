# main.py

from fastapi import FastAPI

app = FastAPI()

# GET 요청에 대한 경로
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# 실행 명령어 (uvicorn을 통해 실행)
# uvicorn main:app --reload
