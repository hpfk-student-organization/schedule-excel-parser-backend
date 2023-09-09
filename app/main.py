"""
Файл налаштування проєкту
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import v1

app = FastAPI()

origins = [
    "http://localhost:8080",
]
basic_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.routers, prefix=basic_prefix + "/v1")
