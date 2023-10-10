import os

from celery import Celery

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
