"""
Файл налаштування проєкту
"""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import v1
from app.handlers.exception import error_4xx

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists('%s/.env' % BASE_DIR):
    load_dotenv('%s/.env' % BASE_DIR)
env = os.environ

origins = [
    *env['ALLOWED_HOSTS'].split(',')
]
basic_prefix = "/api"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, error_4xx.validation_exception_handler)

app.include_router(v1.routers, prefix=basic_prefix + "/v1")
