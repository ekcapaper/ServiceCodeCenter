import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# POST 요청에서 사용할 데이터 모델 정의
class Message(BaseModel):
    text: str


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/message")
async def create_message(message: Message):
    return {"received": message.text}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8005)
