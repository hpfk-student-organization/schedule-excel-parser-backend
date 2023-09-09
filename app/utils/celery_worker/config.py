import os
from pathlib import Path

from celery import Celery, Task

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

if os.path.exists('%s/.env' % PROJECT_DIR):
    load_dotenv('%s/.env' % PROJECT_DIR)

env = os.environ

app = Celery(
    'myapp',
    broker='redis://{host}:{port}/0'.format(
        host=env.get('REDIS_HOST', "127.0.0.1"),
        port=env.get('REDIS_PORT', "6379")
    ))

# Конфігурація Celery
app.conf.update(
    result_backend='redis://{host}:{port}/0'.format(
        host=env.get('REDIS_HOST', "127.0.0.1"),
        port=env.get('REDIS_PORT', "6379")
    ),
)

