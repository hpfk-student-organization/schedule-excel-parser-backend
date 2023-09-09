"""
Файл налаштування проєкту
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import v1
from app.handlers.exception import error_4xx

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

# app.add_exception_handler(RequestValidationError, error_4xx.validation_exception_handler)

app.include_router(v1.routers, prefix=basic_prefix + "/v1")
