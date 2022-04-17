import os
from typing import Optional
from fastapi import FastAPI
from app.routes.music import router as router

app = FastAPI()  # FastAPI 모듈
app.include_router(router)  # 다른 route파일들을 불러와 포함시킴


@app.get("/")  # Route Path
def index():
    return {
        "Status": "Good",
    }
